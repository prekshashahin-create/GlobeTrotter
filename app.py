if __name__ == "__main__":

 from flask import Flask, request, redirect, url_for, session, render_template
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

@app.route("/cities")
def get_cities():

    connection = get_db_connection()

    cities = connection.execute(
        """
        SELECT *
        FROM cities
        ORDER BY popularity DESC
        """
    ).fetchall()

    connection.close()

    return {
        "cities": [dict(city) for city in cities]
    }


@app.route("/cities/<int:city_id>")
def get_city(city_id):

    connection = get_db_connection()

    city = connection.execute(
        """
        SELECT *
        FROM cities
        WHERE id = ?
        """,
        (city_id,)
    ).fetchone()

    connection.close()

    if city is None:
        return {
            "error": "City not found"
        }, 404

    return {
        "city": dict(city)
    }


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

    return render_template("create_trip.html")

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

    total_trips = len(trips)

    return render_template(
        "dashboard.html",
        trips=trips,
        user_name=session["user_name"],
        total_trips=total_trips
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)