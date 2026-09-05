# 🌍 GlobeTrotter

> **Plan less. Travel more. ✈️**

GlobeTrotter is a travel planning web application built to make discovering destinations and organizing trips simple, interactive, and enjoyable.

The platform allows users to explore cities, discover famous destinations, create personalized trips, and manage their travel plans through a clean and user-friendly interface.

---

## ✨ Features

### 🏠 Home Page
- Attractive landing page
- Introduction to GlobeTrotter
- Easy access to travel exploration and planning

### 🔐 User Authentication
- User Sign Up
- User Login
- Secure password hashing
- Session-based authentication
- Logout functionality

### 🌎 Explore Cities
Users can explore different destinations and discover:

- 🏙️ City information
- 🌍 Country and region
- 📍 Famous places
- 📝 Destination descriptions
- 🖼️ Destination images
- 🔎 City search
- 🧭 Detailed city exploration

### 🗺️ Trip Planning
GlobeTrotter provides different ways to plan a trip.

Users can:
- Explore destinations before planning
- Create their own travel plan
- Select destinations
- Add trip stops
- Organize activities
- View trip details

### ⚡ Quick Planning
A simpler way to start planning a journey quickly.

### 🧳 My Trips
Users can view their created trips and access their trip details.

### 🎯 Trip Details
Users can view the details of individual trips, including destinations and planned activities.

### 💰 Expense Management
The database supports storing and managing trip-related expenses.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Backend programming |
| 🌶️ Flask | Web framework |
| 🗄️ SQLite | Database |
| 🌐 HTML5 | Web page structure |
| 🎨 CSS3 | Website styling |
| 🧩 Jinja2 | Dynamic HTML templates |
| 🔧 Git | Version control |
| 🐙 GitHub | Code hosting |

---

## 📁 Project Structure

```text
GlobeTrotter/
│
├── Static/
│   └── Style.css
│
├── Templates/
│   ├── cities.html
│   ├── city_details.html
│   ├── city_images.py
│   ├── create_trip.html
│   ├── dashboard.html
│   ├── experiences.html
│   ├── home.html
│   ├── login.html
│   ├── plan_trip.html
│   ├── select_destinations.html
│   ├── signup.html
│   ├── trip_details.html
│   └── trips.html
│
├── venv/
│
├── app.py
├── city_images.py
├── database.py
├── globetrotter.db
├── logic.py
├── README.md
├── requirements.txt
├── seed.py
└── test_logic.py