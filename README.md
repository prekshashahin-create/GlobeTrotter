# 🌍 GlobeTrotter

> Plan less. Travel more. ✈️

GlobeTrotter is a travel planning web application that helps users discover destinations, create trips, organize itineraries, and explore travel experiences — all from one place.

---

## ✨ Features

### 🔐 User Authentication
- User signup and login
- Secure password hashing
- Session-based authentication
- Logout functionality

### 🗺️ Destination Explorer
- Browse available cities and destinations
- View detailed information about destinations
- Explore different travel possibilities

### ✈️ Trip Planning
GlobeTrotter provides multiple ways to start planning a trip:

- **I know where I want to go**
- **Help me choose a destination**
- **Explore and get inspired**

Users can select destinations and build their own travel plans.

### 🧳 Trip Management
- Create personal trips
- Add descriptions and travel dates
- Add destinations to trips
- View planned trips
- View individual trip details

### 🎨 Modern UI
- Premium travel-inspired design
- Responsive layout
- Animated interactions
- Glassmorphism effects
- Interactive destination and trip cards
- Clean and aesthetic dashboard

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- Jinja2 Templates
- Google Fonts

### Backend
- Python
- Flask

### Database
- SQLite

### Authentication
- Werkzeug password hashing
- Flask sessions

### Development Tools
- Visual Studio Code
- Git
- GitHub

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
│   ├── create_trip.html
│   ├── dashboard.html
│   ├── experiences.html
│   ├── explore.html
│   ├── login.html
│   ├── plan_trip.html
│   ├── quick_plan.html
│   ├── quick_plan_result.html
│   ├── select_destinations.html
│   ├── signup.html
│   ├── trip_details.html
│   └── trips.html
│
├── app.py
├── database.py
├── logic.py
├── seed.py
├── globetrotter.db
├── requirements.txt
└── README.md