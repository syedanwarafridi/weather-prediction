# Weather Prediction App

A Django-based web application that provides weather predictions using the Open-Meteo API. Features user registration, authentication, and weather prediction tracking.

## 🚀 Features

- User Registration & Authentication
- Weather Prediction using Open-Meteo API
- PostgreSQL Database Integration
- Session-based Authentication
- Prediction History Tracking
- RESTful API Endpoints

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: HTML, JavaScript, CSS
- **Weather API**: Open-Meteo
- **Authentication**: Session-based

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## 🏗️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd unrealpays
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Configure PostgreSQL:
```sql
CREATE DATABASE weather_db;
CREATE USER weather_user WITH PASSWORD 'weather_pass123';
GRANT ALL PRIVILEGES ON DATABASE weather_db TO weather_user;
```

#### Update config.json:
```json
{
    "db_name": "weather_db",
    "db_user": "weather_user",
    "db_password": "weather_pass123",
    "db_host": "localhost",
    "db_port": "5432"
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

## 📊 API Endpoints

### Authentication Endpoints

#### User Registration
**POST** `/register/`
```json
{
    "email": "user@example.com",
    "username": "testuser",
    "password": "testpass123"
}
```

**Response:**
```json
{
    "message": "User created successfully"
}
```

#### User Login
**POST** `/login/`
```json
{
    "email": "user@example.com",
    "password": "testpass123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {
        "email": "user@example.com",
        "username": "testuser"
    }
}
```

#### User Logout
**POST** `/logout/`

**Response:**
```json
{
    "message": "Logout successful"
}
```

### Weather Endpoints

#### Get Weather Prediction
**POST** `/predict/`
```json
{
    "location": "London,UK"
}
```

**Response:**
```json
{
    "location": "London,UK",
    "coordinates": "51.5074, -0.1278",
    "current_weather": {
        "time": "2024-01-15T14:00",
        "temperature": "12.5°C",
        "humidity": "75%",
        "precipitation_probability": "40%"
    },
    "today_max_precipitation": "60%"
}
```

#### Get Prediction History
**GET** `/predict/`

**Response:**
```json
{
    "message": "Welcome testuser",
    "prediction_history": [
        {
            "location": "London,UK",
            "date_requested": "2024-01-15 14:30:25"
        }
    ],
    "instructions": "Send POST request with 'location' parameter to get weather prediction"
}
```

#### User Profile
**GET** `/profile/`

**Response:**
```json
{
    "user": {
        "email": "user@example.com",
        "username": "testuser",
        "is_active": true
    }
}
```

## 🔧 CURL Commands

### User Registration
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "test