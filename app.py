from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from city_images import CITY_IMAGES

# ============================================================
# FAMOUS PLACES / FAMOUS FOR
# ============================================================

CITY_FAMOUS_FOR = {
    "Ahmedabad": "Atal Bridge",
    "Mumbai": "Gateway of India",
    "Delhi": "Red Fort",
    "Jaipur": "Hawa Mahal",
    "Udaipur": "City Palace",
    "Jodhpur": "Mehrangarh Fort",
    "Bengaluru": "Silicon Valley of India",
    "Mysore": "Mysore Palace",
    "Chennai": "Kapaleeshwarar Temple",
    "Kolkata": "Victoria Memorial",
    "Goa": "Beaches & Portuguese Heritage",
    "Agra": "Taj Mahal",
    "Varanasi": "Ghats of the Ganges",
    "Hyderabad": "Charminar",
    "Kochi": "Boat House and Backwaters",
}

import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "globetrotter-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "globetrotter.db")

print("================================")
print("DATABASE BEING USED:")
print(DATABASE)
print("================================")
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")


# ============================================================
# SIGN UP
# ============================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return "All fields are required", 400

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, hashed_password)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return "An account with this email already exists.", 400

        connection.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

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

        return "Invalid email or password", 401

    return render_template("login.html")


# ============================================================
# CITIES
# ============================================================

@app.route("/cities")
def cities():

    search = request.args.get("search", "").strip()

    conn = get_db_connection()

    if search:
        city_list = conn.execute("""
            SELECT
                id,
                name AS city,
                country,
                region AS state,
                cost_index,
                popularity,
                famous_place AS popular_place,
                image_url,
                description
            FROM cities
            WHERE name LIKE ?
               OR region LIKE ?
               OR country LIKE ?
            ORDER BY name
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:
        city_list = conn.execute("""
            SELECT
                id,
                name AS city,
                country,
                region AS state,
                cost_index,
                popularity,
                famous_place AS popular_place,
                image_url,
                description
            FROM cities
            ORDER BY name
        """).fetchall()

    conn.close()

    # --------------------------------------------------------
    # REMOVE DUPLICATE CITY CARDS
    # Prefer the record that has complete information.
    # --------------------------------------------------------

    unique_cities = {}

    for city in city_list:

        city_data = dict(city)

        city_name = (
            city_data.get("city")
            or city_data.get("name")
            or ""
        ).strip()

        key = city_name.lower()

        # If this city hasn't appeared yet, store it.
        if key not in unique_cities:
            unique_cities[key] = city_data

        else:
            existing = unique_cities[key]

            # Prefer the record with description/famous place.
            existing_complete = bool(
                existing.get("description")
                or existing.get("popular_place")
            )

            new_complete = bool(
                city_data.get("description")
                or city_data.get("popular_place")
            )

            if new_complete and not existing_complete:
                unique_cities[key] = city_data

    cities_with_images = []

    for city_data in unique_cities.values():

        city_name = (
            city_data.get("city")
            or city_data.get("name")
            or ""
        ).strip()

        # Custom image
        custom_image = CITY_IMAGES.get(city_name, "")

        if custom_image:
            city_data["image_url"] = custom_image
            city_data["image"] = custom_image

        # Custom "Famous for"
        famous_for = CITY_FAMOUS_FOR.get(city_name)

        if famous_for:
            city_data["popular_place"] = famous_for

        cities_with_images.append(city_data)

    return render_template(
        "cities.html",
        cities=cities_with_images,
        search=search
    )

# ============================================================
# CITY DETAILS
# ============================================================

@app.route("/city/<int:city_id>")
def city_details(city_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    # --------------------------------------------------------
    # GET CITY FROM CITIES TABLE
    # --------------------------------------------------------

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
        return "City not found", 404

    city_data = dict(city)

    # --------------------------------------------------------
    # NORMALIZE CITY NAME
    # --------------------------------------------------------

    city_name = (
        city_data.get("city")
        or city_data.get("name")
        or ""
    )

    city_data["name"] = city_name

    # --------------------------------------------------------
    # ADD CUSTOM IMAGE
    # --------------------------------------------------------

    custom_image = CITY_IMAGES.get(
        city_name,
        ""
    )

    if custom_image:
        city_data["image_url"] = custom_image
        city_data["image"] = custom_image

    # --------------------------------------------------------
    # GET USER'S TRIPS
    # --------------------------------------------------------

    trips_list = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    # --------------------------------------------------------
    # SEND EVERYTHING TO city_details.html
    # --------------------------------------------------------

    return render_template(
        "city_details.html",
        city=city_data,
        trips=trips_list
    )



# ============================================================
# SELECT DESTINATIONS
# ============================================================


# ============================================================
# ADD CITY TO EXISTING TRIP
# ============================================================

@app.route("/add-to-trip", methods=["POST"])
def add_to_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    city_id = request.form.get("city_id", type=int)
    trip_id = request.form.get("trip_id", type=int)

    if not city_id or not trip_id:
        return redirect(url_for("cities"))

    connection = get_db_connection()

    # --------------------------------------------------------
    # Check trip belongs to logged-in user
    # --------------------------------------------------------

    trip = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    ).fetchone()

    if trip is None:
        connection.close()
        return "Trip not found", 404

    # --------------------------------------------------------
    # Check city exists
    # --------------------------------------------------------

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
        return "City not found", 404

    # --------------------------------------------------------
    # Check whether city already exists in this trip
    # --------------------------------------------------------

    existing_stop = connection.execute(
        """
        SELECT *
        FROM trip_stops
        WHERE trip_id = ?
        AND city_id = ?
        """,
        (
            trip_id,
            city_id
        )
    ).fetchone()

    if existing_stop:

        connection.close()

        return redirect(
            url_for(
                "city_details",
                city_id=city_id
            )
        )

    # --------------------------------------------------------
    # Find next stop order
    # --------------------------------------------------------

    result = connection.execute(
        """
        SELECT COALESCE(MAX(stop_order), 0) + 1 AS next_order
        FROM trip_stops
        WHERE trip_id = ?
        """,
        (trip_id,)
    ).fetchone()

    stop_order = result["next_order"]

    # --------------------------------------------------------
    # Add city to trip
    # --------------------------------------------------------

    connection.execute(
        """
        INSERT INTO trip_stops
        (
            trip_id,
            city_id,
            start_date,
            end_date,
            stop_order
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trip_id,
            city_id,
            trip["start_date"],
            trip["end_date"],
            stop_order
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "city_details",
            city_id=city_id
        )
    )


# ============================================================
# ADD TRIP STOP
# ============================================================

@app.route("/trips/<int:trip_id>/stops", methods=["POST"])
def add_trip_stop(trip_id):

    if "user_id" not in session:
        return {
            "error": "Login required"
        }, 401

    city_id = request.form.get("city_id", type=int)
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not city_id or not start_date or not end_date:
        return {
            "error": "city_id, start_date and end_date are required"
        }, 400

    connection = get_db_connection()

    # --------------------------------------------------------
    # Check trip ownership
    # --------------------------------------------------------

    trip = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    ).fetchone()

    if trip is None:
        connection.close()

        return {
            "error": "Trip not found"
        }, 404

    # --------------------------------------------------------
    # Check city
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Check duplicate
    # --------------------------------------------------------

    existing = connection.execute(
        """
        SELECT *
        FROM trip_stops
        WHERE trip_id = ?
        AND city_id = ?
        """,
        (
            trip_id,
            city_id
        )
    ).fetchone()

    if existing:

        connection.close()

        return {
            "error": "This city is already part of the trip."
        }, 400

    # --------------------------------------------------------
    # Find next order
    # --------------------------------------------------------

    result = connection.execute(
        """
        SELECT COALESCE(MAX(stop_order), 0) + 1 AS next_order
        FROM trip_stops
        WHERE trip_id = ?
        """,
        (trip_id,)
    ).fetchone()

    stop_order = result["next_order"]

    # --------------------------------------------------------
    # Insert stop
    # --------------------------------------------------------

    connection.execute(
        """
        INSERT INTO trip_stops
        (
            trip_id,
            city_id,
            start_date,
            end_date,
            stop_order
        )
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

    connection.commit()
    connection.close()

    return {
        "message": "City added to trip successfully",
        "trip_id": trip_id,
        "city_id": city_id,
        "stop_order": stop_order
    }, 201

# ============================================================
# CREATE TRIP
# ============================================================

@app.route("/trips/create", methods=["GET", "POST"])
def create_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")

        if not name:
            return "Trip name is required", 400

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO trips
            (
                user_id,
                name,
                description,
                start_date,
                end_date
            )
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

        return redirect(url_for("trips"))

    return render_template("create_trip.html")

# ============================================================
# TRIPS LIST
# ============================================================

@app.route("/trips")
def trips():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    trips_list = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "trips.html",
        trips=trips_list
    )


# ============================================================
# TRIP DETAILS
# ============================================================

@app.route("/trip/<int:trip_id>")
def trip_details(trip_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    # --------------------------------------------------------
    # Get trip
    # --------------------------------------------------------

    trip = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    ).fetchone()

    if trip is None:
        connection.close()
        return "Trip not found", 404

    # --------------------------------------------------------
    # Get trip stops + city information
    # --------------------------------------------------------

    stops = connection.execute(
        """
        SELECT
            trip_stops.*,
            cities.name AS city_name,
            cities.country AS country,
            cities.region AS region,
            cities.cost_index AS cost_index,
            cities.popularity AS popularity
        FROM trip_stops

        JOIN cities
            ON trip_stops.city_id = cities.id

        WHERE trip_stops.trip_id = ?

        ORDER BY trip_stops.stop_order
        """,
        (trip_id,)
    ).fetchall()

    # --------------------------------------------------------
    # Get expenses
    # --------------------------------------------------------

    expenses = connection.execute(
        """
        SELECT *
        FROM expenses
        WHERE trip_id = ?
        ORDER BY id DESC
        """,
        (trip_id,)
    ).fetchall()

    # --------------------------------------------------------
    # Calculate total expenses
    # --------------------------------------------------------

    total_expenses = connection.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE trip_id = ?
        """,
        (trip_id,)
    ).fetchone()["total"]

    connection.close()

    return render_template(
        "trip_details.html",
        trip=trip,
        stops=stops,
        expenses=expenses,
        total_expenses=total_expenses
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    # --------------------------------------------------------
    # USER TRIPS
    # --------------------------------------------------------

    trips_list = connection.execute(
        """
        SELECT *
        FROM trips
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    # --------------------------------------------------------
    # ALL CITIES
    # --------------------------------------------------------

    cities_list_raw = connection.execute(
        """
        SELECT *
        FROM cities
        ORDER BY popularity DESC, name
        """
    ).fetchall()

    cities_list = []

    for city in cities_list_raw:

        city_data = dict(city)

        city_name = city_data.get("name", "")

        custom_image = CITY_IMAGES.get(city_name, "")

        if custom_image:
            city_data["image_url"] = custom_image
            city_data["image"] = custom_image

        cities_list.append(city_data)

    # --------------------------------------------------------
    # TRIP COUNT
    # --------------------------------------------------------

    trip_count = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM trips
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()["count"]

    # --------------------------------------------------------
    # FAVORITES
    # --------------------------------------------------------

    favorite_rows = connection.execute(
        """
        SELECT city_id
        FROM favorites
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchall()

    favorite_ids = {
        row["city_id"]
        for row in favorite_rows
    }

    connection.close()

    return render_template(
        "dashboard.html",
        trips=trips_list,
        cities=cities_list,
        trip_count=trip_count,
        favorite_ids=favorite_ids,
        user_name=session.get(
            "user_name",
            "Traveler"
        )
    )


# ============================================================
# PLAN TRIP
# ============================================================

@app.route("/plan-trip")
def plan_trip():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("plan_trip.html")

# ============================================================
# EXPLORE
# ============================================================

@app.route("/explore")
def explore():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("explore.html")


# ============================================================
# EXPERIENCES
# ============================================================

@app.route("/experiences")
def experiences():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("experiences.html")


# ============================================================
# QUICK PLAN
# ============================================================

@app.route("/quick-plan", methods=["GET", "POST"])
def quick_plan():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        destination = request.form.get("destination", "").strip()
        start_date = request.form.get("start_date", "")
        days = request.form.get("days", "")
        trip_type = request.form.get("trip_type", "")

        return render_template(
            "quick_plan.html",
            destination=destination,
            start_date=start_date,
            days=days,
            trip_type=trip_type
        )

    return render_template("quick_plan.html")

# ============================================================
# FAVORITES
# ============================================================

@app.route("/favorites")
def favorites():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    favorite_cities = connection.execute(
        """
        SELECT cities.*
        FROM favorites
        JOIN cities
            ON favorites.city_id = cities.id
        WHERE favorites.user_id = ?
        ORDER BY favorites.id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "favorites.html",
        cities=favorite_cities
    )


# ============================================================
# ADD FAVORITE
# ============================================================

@app.route("/favorite/<int:city_id>", methods=["POST"])
def add_favorite(city_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

        # --------------------------------------------------------
    # Find destination
    # --------------------------------------------------------

    destination = connection.execute(
        """
        SELECT *
        FROM destinations
        WHERE id = ?
        """,
        (city_id,)
    ).fetchone()

    if destination is None:
        connection.close()
        return "City not found", 404

    destination_name = (
        destination["city"]
        if "city" in destination.keys()
        else destination["name"]
    )

    destination_country = destination["country"]

    # --------------------------------------------------------
    # Find matching city in cities table
    # --------------------------------------------------------

    city = connection.execute(
        """
        SELECT *
        FROM cities
        WHERE name = ?
        AND country = ?
        """,
        (
            destination_name,
            destination_country
        )
    ).fetchone()

    if city is None:
        connection.close()
        return "City is not available in the trip database", 404

    real_city_id = city["id"]

    connection.execute(
        """
        INSERT OR IGNORE INTO favorites
        (user_id, city_id)
        VALUES (?, ?)
        """,
        (
            session["user_id"],
            city_id
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        request.referrer or
        url_for("dashboard")
    )


# ============================================================
# REMOVE FAVORITE
# ============================================================

@app.route("/favorite/<int:city_id>/remove", methods=["POST"])
def remove_favorite(city_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM favorites
        WHERE user_id = ?
        AND city_id = ?
        """,
        (
            session["user_id"],
            city_id
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        request.referrer or
        url_for("dashboard")
    )


# ============================================================
# DELETE TRIP
# ============================================================

@app.route("/trip/<int:trip_id>/delete", methods=["POST"])
def delete_trip(trip_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    trip = connection.execute(
        """
        SELECT id
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    ).fetchone()

    if trip is None:
        connection.close()
        return "Trip not found", 404

    connection.execute(
        """
        DELETE FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    )

    connection.commit()
    connection.close()

    if session.get("current_trip_id") == trip_id:
        session.pop("current_trip_id", None)

    return redirect(
        url_for("trips")
    )


# ============================================================
# ADD EXPENSE
# ============================================================

@app.route("/trip/<int:trip_id>/expense", methods=["POST"])
def add_expense(trip_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    category = request.form.get(
        "category",
        "Other"
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    amount = request.form.get(
        "amount",
        type=float
    )

    if not category or amount is None or amount < 0:
        return "Invalid expense information", 400

    connection = get_db_connection()

    trip = connection.execute(
        """
        SELECT id
        FROM trips
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trip_id,
            session["user_id"]
        )
    ).fetchone()

    if trip is None:
        connection.close()
        return "Trip not found", 404

    connection.execute(
        """
        INSERT INTO expenses
        (
            trip_id,
            category,
            description,
            amount
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            trip_id,
            category,
            description,
            amount
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "trip_details",
            trip_id=trip_id
        )
    )


# ============================================================
# DELETE EXPENSE
# ============================================================

@app.route(
    "/expense/<int:expense_id>/delete",
    methods=["POST"]
)
def delete_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    expense = connection.execute(
        """
        SELECT expenses.id
        FROM expenses

        JOIN trips
            ON expenses.trip_id = trips.id

        WHERE expenses.id = ?
        AND trips.user_id = ?
        """,
        (
            expense_id,
            session["user_id"]
        )
    ).fetchone()

    if expense is None:
        connection.close()
        return "Expense not found", 404

    connection.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    connection.commit()
    connection.close()

    return redirect(
        request.referrer or
        url_for("dashboard")
    )

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "home.html"
    ), 404


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )