 Flask + React Investment App

This is a **full-stack CRUD application** built with **Flask (backend)** and **React (frontend)**.  
The app lets users **Create, Read, Update, and Delete (CRUD)** investment records.


##  Features

- Add new investments with:
  - User Name
  - Amount
  - Gold Quantity
- View all investments
- Update investment details
- Delete investments
- Backend API built with **Flask + SQLAlchemy + Flask-Migrate**
- Frontend built with **React + Axios**
- **CORS enabled** for smooth frontend-backend communication

---

## 🛠️ Tech Stack

### Backend
- Python (Flask)
- SQLAlchemy (ORM)
- Flask-Migrate (DB migrations)
- Flask-CORS

### Frontend
- React
- Axios

### Database
- SQLite (default, configurable)

---

## 📂 Project Structure

flask-app_react-app-invest/
│── app/
│   ├── **init**.py        # Flask app factory
│   ├── app.py             # Routes (CRUD APIs)
│   ├── models.py          # Database Models
│── migrations/            # Flask-Migrate folder
│── frontend/              # React frontend
│── config.py              # DB config
│── run.py                 # App entry point
│── requirements.txt       # Backend dependencies


## ⚙️ Setup Guide

### 1️⃣ Backend Setup
bash
# Clone the repo
git clone https://github.com/your-username/flask-app_react-app-invest.git
cd flask-app_react-app-invest

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# Install backend dependencies
pip install -r requirements.txt

# Setup Database
flask db init
flask db migrate -m "init"
flask db upgrade

# Run backend
python run.py

Backend runs at: **[http://localhost:5000](http://localhost:5000)**

---

### 2️⃣ Frontend Setup

bash
cd frontend
npm install
npm start

Frontend runs at: **[http://localhost:3000](http://localhost:3000)**

---
## 📡 API Endpoints

### Create Investment

http
POST /investments


json
{
  "user_name": "Dharmesh",
  "amount": 5000,
  "gold_quantity": 10
}

### Get All Investments
http
GET /investments

### Get Investment by ID
http
GET /investments/{id}

### Update Investment

http
PUT /investments/{id}

### Delete Investment

http
DELETE /investments/{id}

---

## ✅ Project Status

* [x] Backend CRUD (Flask + SQLAlchemy)
* [x] Database migrations (Flask-Migrate)
* [x] Frontend setup (React + Axios)
* [x] CORS configured
* [ ] Frontend UI for CRUD operations (in progress)

---

