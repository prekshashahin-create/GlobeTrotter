import sqlite3


DATABASE = "globetrotter.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db():

    connection = get_db_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,

    UNIQUE(user_id, city_id),

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (city_id)
        REFERENCES cities(id)
        ON DELETE CASCADE
);

        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            cover_photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users (id)
                ON DELETE CASCADE
        );


        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT,
            cost_index REAL DEFAULT 0,
            popularity REAL DEFAULT 0
        );


        CREATE TABLE IF NOT EXISTS trip_stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            stop_order INTEGER NOT NULL,

            FOREIGN KEY (trip_id)
                REFERENCES trips (id)
                ON DELETE CASCADE,

            FOREIGN KEY (city_id)
                REFERENCES cities (id)
        );


        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            activity_type TEXT,
            cost REAL DEFAULT 0,
            duration REAL DEFAULT 0,

            FOREIGN KEY (city_id)
                REFERENCES cities (id)
        );


        CREATE TABLE IF NOT EXISTS trip_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_stop_id INTEGER NOT NULL,
            activity_id INTEGER NOT NULL,
            activity_date TEXT NOT NULL,
            start_time TEXT,
            cost REAL DEFAULT 0,

            FOREIGN KEY (trip_stop_id)
                REFERENCES trip_stops (id)
                ON DELETE CASCADE,

            FOREIGN KEY (activity_id)
                REFERENCES activities (id)
        );


        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,

            FOREIGN KEY (trip_id)
                REFERENCES trips (id)
                ON DELETE CASCADE
        );
    """)


    # ========================================================
    # ADD NEW CITY COLUMNS
    # ========================================================
    #
    # These ALTER statements make the code compatible with
    # an existing globetrotter.db.
    #

    columns = connection.execute(
        "PRAGMA table_info(cities)"
    ).fetchall()

    existing_columns = {
        column["name"]
        for column in columns
    }


    if "image_url" not in existing_columns:

        connection.execute(
            """
            ALTER TABLE cities
            ADD COLUMN image_url TEXT
            """
        )


    if "famous_place" not in existing_columns:

        connection.execute(
            """
            ALTER TABLE cities
            ADD COLUMN famous_place TEXT
            """
        )


    if "description" not in existing_columns:

        connection.execute(
            """
            ALTER TABLE cities
            ADD COLUMN description TEXT
            """
        )


    connection.commit()


    # ========================================================
    # INSERT CITY DATA
    # ========================================================

    seed_cities(connection)


    # ========================================================
    # INSERT ACTIVITY DATA
    # ========================================================

    seed_activities(connection)


    connection.commit()

    connection.close()


# ============================================================
# CITY SEED DATA
# ============================================================

def seed_cities(connection):

    cities = [

        # ====================================================
        # INDIA
        # ====================================================

        (
            "Ahmedabad",
            "India",
            "Gujarat",
            2.5,
            8.5,
            "Sabarmati Ashram",
            "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
            "A vibrant Gujarati city known for heritage architecture, food and culture."
        ),

        (
            "Mumbai",
            "India",
            "Maharashtra",
            4.0,
            9.5,
            "Gateway of India",
            "https://images.unsplash.com/photo-1566552881560-0be862a7c445?auto=format&fit=crop&w=1200&q=80",
            "India's bustling financial capital with beaches, heritage sites and nightlife."
        ),

        (
            "Delhi",
            "India",
            "Delhi",
            3.5,
            9.5,
            "India Gate",
            "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
            "A historic capital filled with monuments, museums and cultural experiences."
        ),

        (
            "Jaipur",
            "India",
            "Rajasthan",
            3.0,
            9.2,
            "Hawa Mahal",
            "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1200&q=80",
            "The Pink City famous for royal palaces, forts and colorful markets."
        ),

        (
            "Udaipur",
            "India",
            "Rajasthan",
            3.2,
            8.8,
            "Lake Pichola",
            "https://www.tourmyindia.com/states/rajasthan/image/udaipur-banner.webp",
            "A romantic lake city surrounded by beautiful palaces and Aravalli landscapes."
        ),

        (
            "Jodhpur",
            "India",
            "Rajasthan",
            2.8,
            8.4,
            "Mehrangarh Fort",
            "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1200&q=80",
            "The Blue City dominated by the magnificent Mehrangarh Fort."
        ),

        (
            "Goa",
            "India",
            "Goa",
            4.0,
            9.6,
            "Baga Beach",
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
            "A coastal destination known for beaches, Portuguese heritage and relaxed travel."
        ),

        (
            "Surat",
            "India",
            "Gujarat",
            2.5,
            7.8,
            "Dumas Beach",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
            "A major Gujarat city known for food, textiles and nearby coastal attractions."
        ),

        (
            "Vadodara",
            "India",
            "Gujarat",
            2.5,
            7.7,
            "Laxmi Vilas Palace",
            "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
            "A cultural city with grand palaces, museums and Gujarati heritage."
        ),

        (
            "Rajkot",
            "India",
            "Gujarat",
            2.3,
            7.0,
            "Kaba Gandhi No Delo",
            "https://images.unsplash.com/photo-1532664189809-02133fee698d?auto=format&fit=crop&w=1200&q=80",
            "A lively Saurashtra city with cultural and historical attractions."
        ),

        (
            "Bengaluru",
            "India",
            "Karnataka",
            3.5,
            9.2,
            "Lalbagh Botanical Garden",
            "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1200&q=80",
            "India's technology hub with gardens, cafes and a vibrant modern culture."
        ),

        (
            "Hyderabad",
            "India",
            "Telangana",
            3.0,
            8.9,
            "Charminar",
            "https://s7ap1.scene7.com/is/image/incredibleindia/charminar-hyderabad-1-attr-nearby?qlt=82&ts=1742177359837",
            "A historic city famous for Charminar, biryani and its blend of cultures."
        ),

        (
            "Chennai",
            "India",
            "Tamil Nadu",
            3.0,
            8.5,
            "Marina Beach",
            "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80",
            "A coastal South Indian city known for temples, beaches and classical culture."
        ),

        (
            "Kolkata",
            "India",
            "West Bengal",
            2.8,
            8.7,
            "Victoria Memorial",
            "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1200&q=80",
            "The City of Joy, known for literature, food, art and colonial architecture."
        ),

        (
            "Kochi",
            "India",
            "Kerala",
            3.0,
            8.6,
            "Chinese Fishing Nets",
            "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
            "A beautiful Kerala destination combining coastal scenery and historic streets."
        ),

        (
            "Mysore",
            "India",
            "Karnataka",
            2.6,
            8.2,
            "Mysore Palace",
            "https://travelogyindia.b-cdn.net/blog/wp-content/uploads/2015/10/Mysore.jpg",
            "A heritage city famous for its royal palace and cultural traditions."
        ),

        (
            "Varanasi",
            "India",
            "Uttar Pradesh",
            2.5,
            9.4,
            "Dashashwamedh Ghat",
            "https://images.unsplash.com/photo-1561361058-c24cecae35ca?auto=format&fit=crop&w=1200&q=80",
            "One of India's oldest cities, famous for its ghats and spiritual heritage."
        ),

        (
            "Agra",
            "India",
            "Uttar Pradesh",
            2.7,
            9.3,
            "Taj Mahal",
            "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
            "A historic destination best known for the iconic Taj Mahal."
        ),

        (
            "Amritsar",
            "India",
            "Punjab",
            2.7,
            8.8,
            "Golden Temple",
            "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?auto=format&fit=crop&w=1200&q=80",
            "A culturally rich city centered around the magnificent Golden Temple."
        ),

        (
            "Srinagar",
            "India",
            "Jammu and Kashmir",
            3.5,
            9.3,
            "Dal Lake",
            "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=1200&q=80",
            "A scenic Himalayan destination famous for Dal Lake and houseboats."
        ),

        (
            "Manali",
            "India",
            "Himachal Pradesh",
            3.5,
            9.0,
            "Solang Valley",
            "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
            "A mountain getaway surrounded by snow-capped peaks and valleys."
        ),

        (
            "Rishikesh",
            "India",
            "Uttarakhand",
            2.8,
            8.8,
            "Laxman Jhula",
            "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80",
            "A riverside destination known for yoga, adventure and Himalayan scenery."
        ),

        (
            "Darjeeling",
            "India",
            "West Bengal",
            3.0,
            8.5,
            "Tiger Hill",
            "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80",
            "A Himalayan hill station famous for tea gardens and mountain views."
        ),

        (
            "Shimla",
            "India",
            "Himachal Pradesh",
            3.2,
            8.7,
            "The Ridge",
            "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80",
            "A classic Himalayan hill station filled with colonial architecture."
        ),


        # ====================================================
        # INTERNATIONAL
        # ====================================================

        (
            "Paris",
            "France",
            "Île-de-France",
            8.5,
            10.0,
            "Eiffel Tower",
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
            "The French capital known for art, fashion, architecture and cuisine."
        ),

        (
            "London",
            "United Kingdom",
            "England",
            8.5,
            9.8,
            "Big Ben",
            "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80",
            "A global city filled with history, museums, parks and iconic landmarks."
        ),

        (
            "Dubai",
            "United Arab Emirates",
            "Dubai",
            8.0,
            9.8,
            "Burj Khalifa",
            "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
            "A futuristic destination known for skyscrapers, luxury and desert experiences."
        ),

        (
            "Singapore",
            "Singapore",
            "Singapore",
            7.5,
            9.6,
            "Marina Bay Sands",
            "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80",
            "A modern island city known for gardens, food and futuristic architecture."
        ),

        (
            "Tokyo",
            "Japan",
            "Kanto",
            7.0,
            9.7,
            "Shibuya Crossing",
            "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=80",
            "Japan's energetic capital blending traditional culture with advanced technology."
        ),

        (
            "Seoul",
            "South Korea",
            "Seoul",
            6.0,
            9.4,
            "Gyeongbokgung Palace",
            "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=1200&q=80",
            "South Korea's modern capital blending palaces, technology and pop culture."
        ),

        (
            "New York",
            "United States",
            "New York",
            9.0,
            10.0,
            "Statue of Liberty",
            "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
            "A global metropolis known for skyscrapers, museums and diverse neighborhoods."
        ),

        (
            "Rome",
            "Italy",
            "Lazio",
            6.5,
            9.8,
            "Colosseum",
            "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80",
            "An ancient city filled with Roman landmarks, art and Italian cuisine."
        ),

        (
            "Barcelona",
            "Spain",
            "Catalonia",
            6.0,
            9.4,
            "Sagrada Familia",
            "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1200&q=80",
            "A Mediterranean city known for Gaudi architecture, beaches and food."
        ),

        (
            "Bali",
            "Indonesia",
            "Bali",
            4.5,
            9.6,
            "Tanah Lot",
            "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
            "A tropical island known for temples, rice terraces and beaches."
        ),

        (
            "Bangkok",
            "Thailand",
            "Bangkok",
            4.0,
            9.4,
            "Grand Palace",
            "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=80",
            "Thailand's energetic capital known for temples, markets and street food."
        ),

        (
            "Sydney",
            "Australia",
            "New South Wales",
            7.5,
            9.2,
            "Sydney Opera House",
            "https://images.unsplash.com/photo-1524293581917-878a6d017c71?auto=format&fit=crop&w=1200&q=80",
            "An iconic Australian harbor city with beaches and vibrant culture."
        ),

        (
            "Cairo",
            "Egypt",
            "Cairo",
            3.5,
            9.2,
            "Pyramids of Giza",
            "https://images.unsplash.com/photo-1568322445389-f64ac2515020?auto=format&fit=crop&w=1200&q=80",
            "A historic Egyptian city offering ancient monuments and rich culture."
        ),

        (
            "Istanbul",
            "Turkey",
            "Istanbul",
            4.5,
            9.3,
            "Hagia Sophia",
            "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=80",
            "A fascinating city connecting Europe and Asia through centuries of history."
        ),

        (
            "Cape Town",
            "South Africa",
            "Western Cape",
            4.5,
            8.9,
            "Table Mountain",
            "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=1200&q=80",
            "A scenic coastal city surrounded by mountains, beaches and vineyards."
        ),

        (
            "Amsterdam",
            "Netherlands",
            "North Holland",
            7.0,
            9.1,
            "Canal Ring",
            "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?auto=format&fit=crop&w=1200&q=80",
            "A charming European city known for canals, cycling and museums."
        ),

        (
            "Maldives",
            "Maldives",
            "Kaafu Atoll",
            8.0,
            9.7,
            "Malé",
            "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
            "A tropical paradise famous for turquoise water, coral reefs and islands."
        ),

        (
            "Kathmandu",
            "Nepal",
            "Bagmati",
            2.5,
            8.7,
            "Swayambhunath",
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80",
            "Nepal's cultural capital and a gateway to Himalayan adventures."
        ),

        (
            "Zurich",
            "Switzerland",
            "Zurich",
            9.0,
            8.9,
            "Lake Zurich",
            "https://images.unsplash.com/photo-1527668752968-14dc70a27c95?auto=format&fit=crop&w=1200&q=80",
            "A beautiful Swiss city surrounded by lakes and Alpine scenery."
        ),

        (
            "Hong Kong",
            "Hong Kong",
            "Hong Kong",
            7.5,
            9.2,
            "Victoria Harbour",
            "https://images.unsplash.com/photo-1536599018102-9f803c140fc1?auto=format&fit=crop&w=1200&q=80",
            "A spectacular city known for its skyline, harbor and food culture."
        )
    ]


    # ========================================================
    # INSERT / UPDATE CITIES
    # ========================================================

    for city in cities:

        (
            name,
            country,
            region,
            cost_index,
            popularity,
            famous_place,
            image_url,
            description
        ) = city


        existing = connection.execute(
            """
            SELECT id
            FROM cities
            WHERE name = ?
            AND country = ?
            """,
            (
                name,
                country
            )
        ).fetchone()


        if existing:

            connection.execute(
                """
                UPDATE cities
                SET
                    region = ?,
                    cost_index = ?,
                    popularity = ?,
                    famous_place = ?,
                    image_url = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description,
                    existing["id"]
                )
            )

        else:

            connection.execute(
                """
                INSERT INTO cities
                (
                    name,
                    country,
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    country,
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description
                )
            )


    # ========================================================
    # INSERT / UPDATE CITIES
    # ========================================================

    for city in cities:

        (
            name,
            country,
            region,
            cost_index,
            popularity,
            famous_place,
            image_url,
            description
        ) = city


        existing = connection.execute(
            """
            SELECT id
            FROM cities
            WHERE name = ?
            AND country = ?
            """,
            (
                name,
                country
            )
        ).fetchone()


        if existing:

            connection.execute(
                """
                UPDATE cities
                SET
                    region = ?,
                    cost_index = ?,
                    popularity = ?,
                    famous_place = ?,
                    image_url = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description,
                    existing["id"]
                )
            )

        else:

            connection.execute(
                """
                INSERT INTO cities
                (
                    name,
                    country,
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    country,
                    region,
                    cost_index,
                    popularity,
                    famous_place,
                    image_url,
                    description
                )
            )


# ============================================================
# ACTIVITY SEED DATA
# ============================================================

def seed_activities(connection):

    activities = [

        # Ahmedabad
        (
            "Ahmedabad",
            "Sabarmati Ashram Visit",
            "Explore the historic ashram and learn about India's freedom movement.",
            "Culture",
            0,
            2
        ),

        (
            "Ahmedabad",
            "Gujarati Food Walk",
            "Experience traditional Gujarati snacks and local cuisine.",
            "Food",
            500,
            3
        ),

        # Mumbai
        (
            "Mumbai",
            "Gateway of India",
            "Visit one of Mumbai's most recognizable landmarks.",
            "Sightseeing",
            0,
            1
        ),

        (
            "Mumbai",
            "Marine Drive",
            "Enjoy a relaxing walk along Mumbai's famous coastline.",
            "Nature",
            0,
            2
        ),

        # Delhi
        (
            "Delhi",
            "India Gate",
            "Visit the iconic war memorial in central Delhi.",
            "Sightseeing",
            0,
            1
        ),

        (
            "Delhi",
            "Red Fort",
            "Explore one of India's most important historic forts.",
            "History",
            50,
            2
        ),

        # Jaipur
        (
            "Jaipur",
            "Hawa Mahal",
            "Explore Jaipur's famous Palace of Winds.",
            "History",
            50,
            1.5
        ),

        (
            "Jaipur",
            "Amber Fort",
            "Visit the magnificent hilltop fort near Jaipur.",
            "History",
            100,
            3
        ),

        # Goa
        (
            "Goa",
            "Baga Beach",
            "Spend time along one of Goa's most popular beaches.",
            "Beach",
            0,
            3
        ),

        (
            "Goa",
            "Old Goa Heritage Tour",
            "Explore historic churches and Portuguese-era architecture.",
            "Culture",
            200,
            3
        ),

        # Udaipur
        (
            "Udaipur",
            "Lake Pichola Boat Ride",
            "Enjoy scenic views across Lake Pichola.",
            "Nature",
            500,
            2
        ),

        # Varanasi
        (
            "Varanasi",
            "Ganga Ghat Experience",
            "Explore the historic ghats along the Ganges.",
            "Culture",
            0,
            3
        ),

        # Manali
        (
            "Manali",
            "Solang Valley",
            "Enjoy mountain scenery and outdoor activities.",
            "Adventure",
            500,
            4
        ),

        # Srinagar
        (
            "Srinagar",
            "Dal Lake Shikara Ride",
            "Enjoy a traditional boat ride across Dal Lake.",
            "Nature",
            800,
            2
        ),

        # Paris
        (
            "Paris",
            "Eiffel Tower",
            "Visit one of the world's most famous landmarks.",
            "Sightseeing",
            2500,
            3
        ),

        # London
        (
            "London",
            "Big Ben",
            "Explore the famous Westminster area.",
            "Sightseeing",
            0,
            2
        ),

        # Dubai
        (
            "Dubai",
            "Burj Khalifa",
            "Experience spectacular views from the world's tallest building.",
            "Sightseeing",
            4000,
            3
        ),

        # Tokyo
        (
            "Tokyo",
            "Shibuya Crossing",
            "Experience one of Tokyo's most famous city intersections.",
            "Sightseeing",
            0,
            2
        ),

        # Singapore
        (
            "Singapore",
            "Gardens by the Bay",
            "Explore Singapore's futuristic botanical gardens.",
            "Nature",
            2000,
            3
        ),

        # New York
        (
            "New York",
            "Statue of Liberty",
            "Visit the iconic symbol of New York Harbor.",
            "Sightseeing",
            2500,
            4
        ),

        # Rome
        (
            "Rome",
            "Colosseum",
            "Explore one of the world's most famous ancient monuments.",
            "History",
            3000,
            3
        ),

        # Bali
        (
            "Bali",
            "Tanah Lot",
            "Visit the famous temple located beside the ocean.",
            "Culture",
            500,
            3
        ),

        # Bangkok
        (
            "Bangkok",
            "Grand Palace",
            "Explore Bangkok's historic royal complex.",
            "History",
            700,
            3
        ),

        # Sydney
        (
            "Sydney",
            "Sydney Opera House",
            "See the iconic architectural landmark on Sydney Harbour.",
            "Culture",
            2500,
            2
        ),

        # Cairo
        (
            "Cairo",
            "Pyramids of Giza",
            "Explore the ancient pyramids outside Cairo.",
            "History",
            1000,
            4
        )
    ]


    for activity in activities:

        (
            city_name,
            activity_name,
            description,
            activity_type,
            cost,
            duration
        ) = activity


        city = connection.execute(
            """
            SELECT id
            FROM cities
            WHERE name = ?
            LIMIT 1
            """,
            (city_name,)
        ).fetchone()


        if city is None:
            continue


        existing = connection.execute(
            """
            SELECT id
            FROM activities
            WHERE city_id = ?
            AND name = ?
            """,
            (
                city["id"],
                activity_name
            )
        ).fetchone()


        if existing:

            connection.execute(
                """
                UPDATE activities
                SET
                    description = ?,
                    activity_type = ?,
                    cost = ?,
                    duration = ?
                WHERE id = ?
                """,
                (
                    description,
                    activity_type,
                    cost,
                    duration,
                    existing["id"]
                )
            )

        else:

            connection.execute(
                """
                INSERT INTO activities
                (
                    city_id,
                    name,
                    description,
                    activity_type,
                    cost,
                    duration
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    city["id"],
                    activity_name,
                    description,
                    activity_type,
                    cost,
                    duration
                )
            )