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
def cities():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    cities = connection.execute("""
        SELECT *
        FROM cities
        ORDER BY name
    """).fetchall()

    connection.close()

    return render_template(
        "cities.html",
        cities=cities
    )

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

@app.route("/trips/<int:trip_id>/stops", methods=["POST"])
def add_trip_stop(trip_id):

    if "user_id" not in session:
        return {
            "error": "Login required"
        }, 401

    city_id = request.form.get("city_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not city_id or not start_date or not end_date:
        return {
            "error": "city_id, start_date and end_date are required"
        }, 400

    connection = get_db_connection()

    # Check that this trip belongs to the logged-in user
    trip = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (trip_id, session["user_id"])
    ).fetchone()

    if trip is None:
        connection.close()

        return {
            "error": "Trip not found"
        }, 404

    # Check that the city exists
    city = connection.execute(
        """
        SELECT *
        FROM cities
        WHERE id = ?
        """,
        (city_id,)
    ).fetchone()

    if city is None:
        connection.close()

        return {
            "error": "City not found"
        }, 404

    # Find the next stop order
    result = connection.execute(
        """
        SELECT COALESCE(MAX(stop_order), 0) + 1 AS next_order
        FROM trip_stops
        WHERE trip_id = ?
        """,
        (trip_id,)
    ).fetchone()

    stop_order = result["next_order"]

    # Add the city to the trip
    connection.execute(
        """
        INSERT INTO trip_stops
        (trip_id, city_id, start_date, end_date, stop_order)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trip_id,
            city_id,
            start_date,
            end_date,
            stop_order
        )
    )

    connection.executescript("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS trip_cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER NOT NULL,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
        FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
        UNIQUE(trip_id, city_id)
    );
""")

    connection.commit()
    connection.close()

    return {
        "message": "City added to trip successfully",
        "trip_id": trip_id,
        "city_id": int(city_id),
        "stop_order": stop_order
    }, 201

@app.route("/city/<int:city_id>")
def city_details(city_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    city = connection.execute("""
        SELECT *
        FROM cities
        WHERE id = ?
    """, (city_id,)).fetchone()

    trips = connection.execute("""
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()

    connection.close()

    if city is None:
        return "City not found", 404

    return render_template(
        "city_details.html",
        city=city,
        trips=trips
    )

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
    return redirect(url_for("select_destinations"))
        

    return render_template("create_trip.html")

@app.route("/trips")
def trips():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    trips = connection.execute("""
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()

    connection.close()

    return render_template(
        "trips.html",
        trips=trips
    )

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
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    cities = connection.execute(
        """
        SELECT *
        FROM cities
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        trips=trips,
        cities=cities
    )

@app.route("/add-to-trip", methods=["POST"])
def add_to_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    city_id = request.form.get("city_id")
    trip_id = request.form.get("trip_id")

    if not city_id or not trip_id:
        return redirect(url_for("cities"))

    connection = get_db_connection()

    trip = connection.execute("""
        SELECT *
        FROM trips
        WHERE id = ? AND user_id = ?
    """, (trip_id, session["user_id"])).fetchone()

    if trip is None:
        connection.close()
        return "Trip not found", 404

    connection.execute("""
        INSERT OR IGNORE INTO trip_cities (trip_id, city_id)
        VALUES (?, ?)
    """, (trip_id, city_id))

    connection.commit()
    connection.close()

    return redirect(url_for("city_details", city_id=city_id))

@app.route("/plan-trip")
def plan_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("plan_trip.html")


@app.route("/explore")
def explore():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("explore.html")


@app.route("/experiences")
def experiences():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("experiences.html")


@app.route("/quick-plan", methods=["GET", "POST"])
def quick_plan():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        destination = request.form["destination"]
        start_date = request.form["start_date"]
        days = request.form["days"]
        trip_type = request.form["trip_type"]

        return render_template(
            "quick_plan.html",
            destination=destination,
            start_date=start_date,
            days=days,
            trip_type=trip_type
        )

    return render_template("quick_plan.html")

@app.route("/select-destinations", methods=["GET", "POST"])
def select_destinations():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    cities = connection.execute(
        """
        SELECT *
        FROM cities
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    if request.method == "POST":

        city_ids = request.form.getlist("city_ids")

        if not city_ids:
            return render_template(
                "select_destinations.html",
                cities=cities,
                error="Please select at least one destination."
            )

        session["selected_city_ids"] = city_ids

        return redirect(url_for("dashboard"))

    return render_template(
        "select_destinations.html",
        cities=cities
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)