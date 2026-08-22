from flask import Flask, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import init_db, get_db_connection


app = Flask(__name__)

app.secret_key = "globetrotter-development-secret-key"

init_db()


@app.route("/")
def home():
    return "GlobeTrotter backend is running!"


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password_hash)
            )

            connection.commit()

        except Exception as error:
            connection.close()
            return f"Signup failed: {error}"

        connection.close()

        return redirect(url_for("login"))

    return """
        <h1>GlobeTrotter Signup</h1>

        <form method="POST">

            <input
                type="text"
                name="name"
                placeholder="Name"
                required
            >

            <br><br>

            <input
                type="email"
                name="email"
                placeholder="Email"
                required
            >

            <br><br>

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <br><br>

            <button type="submit">
                Sign Up
            </button>

        </form>
    """


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password"

    return """
        <h1>GlobeTrotter Login</h1>

        <form method="POST">

            <input
                type="email"
                name="email"
                placeholder="Email"
                required
            >

            <br><br>

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <br><br>

            <button type="submit">
                Login
            </button>

        </form>
    """
@app.route("/trips/create", methods=["GET", "POST"])
def create_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        description = request.form.get("description")
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO trips
            (user_id, name, description, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                name,
                description,
                start_date,
                end_date
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("dashboard"))

    return """
        <h1>Create New Trip</h1>

        <form method="POST">

            <input
                type="text"
                name="name"
                placeholder="Trip Name"
                required
            >

            <br><br>

            <textarea
                name="description"
                placeholder="Trip Description"
            ></textarea>

            <br><br>

            <label>Start Date</label>
            <input
                type="date"
                name="start_date"
                required
            >

            <br><br>

            <label>End Date</label>
            <input
                type="date"
                name="end_date"
                required
            >

            <br><br>

            <button type="submit">
                Create Trip
            </button>

        </form>
    """

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    trips = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY start_date
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    trip_list = ""

    for trip in trips:
        trip_list += f"""
            <div>
                <h2>{trip["name"]}</h2>

                <p>
                    {trip["start_date"]}
                    →
                    {trip["end_date"]}
                </p>

                <p>
                    {trip["description"] or "No description"}
                </p>
            </div>

            <hr>
        """

    if not trips:
        trip_list = "<p>You haven't created any trips yet.</p>"

    return f"""
        <h1>Welcome, {session["user_name"]}!</h1>

        <h2>My Trips</h2>

        <a href="{url_for("create_trip")}">
            Create New Trip
        </a>

        <br><br>

        {trip_list}

        <br>

        <a href="{url_for("logout")}">
            Logout
        </a>
    """


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)