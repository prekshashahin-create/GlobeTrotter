from database import get_db_connection


cities = [
    ("Ahmedabad", "India", "Gujarat", 30, 70),
    ("Mumbai", "India", "Maharashtra", 60, 90),
    ("Goa", "India", "Goa", 50, 95),
    ("Jaipur", "India", "Rajasthan", 40, 85),
    ("Delhi", "India", "Delhi", 55, 90),
    ("Dubai", "UAE", "Dubai", 80, 95),
    ("Singapore", "Singapore", "Southeast Asia", 85, 90),
    ("Tokyo", "Japan", "East Asia", 90, 95),
    ("Paris", "France", "Europe", 90, 100),
    ("London", "United Kingdom", "Europe", 95, 100)
]


connection = get_db_connection()

connection.executemany(
    """
    INSERT INTO cities
    (name, country, region, cost_index, popularity)
    VALUES (?, ?, ?, ?, ?)
    """,
    cities
)

connection.commit()
connection.close()

print("Cities added successfully!")