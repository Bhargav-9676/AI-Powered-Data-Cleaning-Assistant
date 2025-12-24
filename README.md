# AI Data Cleaning Assistant

An end-to-end **AI-powered data cleaning platform** that automates CSV analysis, cleaning, and quality scoring with secure authentication and activity logging.

---

## Overview

The **AI Data Cleaning Assistant** helps users upload raw CSV datasets and automatically:

- Detect missing values and duplicate records  
- Clean and standardize data  
- Generate a cleaned output file  
- Track all user activities (login, upload, clean, logout)  
- Provide clear quality metrics in a user-friendly interface  

The system is designed to handle **large, real-world datasets** and follows **industry-style backend architecture**.

---

## Key Features

- Secure user registration and login (JWT authentication)
- One-click CSV upload and automated cleaning pipeline
- Detection and removal of duplicate records
- Automatic handling of missing values
- Data quality scoring (0–100)
- Clean, non-JSON UI for easy understanding
- Activity logs stored in PostgreSQL
- Scalable backend using FastAPI

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pandas

### Frontend
- Streamlit
- REST API integration

### Database
- PostgreSQL
- Activity Logs
- User Management
- Cleaning History

---

## Project Structure

```
ai-data-cleaning-assistant/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── user_routes.py
│   │   └── pipeline_routes.py
│   ├── services/
│   │   └── data_cleaning.py
│
├── frontend/
│   └── streamlit_app.py
│
├── uploads/
│
├── requirements.txt
└── README.md
```

---

## Application Workflow

1. User registers and logs in  
2. JWT token is generated and stored in session  
3. User uploads a CSV file  
4. Backend analyzes the dataset  
5. Data cleaning is applied automatically  
6. Quality metrics are calculated  
7. Cleaned CSV file is generated  
8. All actions are logged in the database  

---

## Activity Logging

Every major action is recorded in PostgreSQL:
- User registration
- User login
- File upload
- Data cleaning execution
- User logout

This provides **auditability and traceability**, similar to enterprise systems.

---

## Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/ai-data-cleaning-assistant.git
cd ai-data-cleaning-assistant
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Database Configuration

Create a `.env` file:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_data_cleaning

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

---

## Running the Application

### Start Backend
```bash
uvicorn app.main:app --reload
```

Backend:
```
http://127.0.0.1:8000
```

Swagger Docs:
```
http://127.0.0.1:8000/docs
```

---

### Start Frontend
```bash
streamlit run frontend/streamlit_app.py
```

Frontend:
```
http://localhost:8501
```

---

## How to Use

1. Register a new user  
2. Login with credentials  
3. Upload a CSV dataset  
4. Run the data cleaning pipeline  
5. View data quality metrics  
6. Download the cleaned CSV file  

---

## Resume One-Liner

**Built an AI-powered data cleaning platform using FastAPI, PostgreSQL, and Streamlit that automates CSV analysis, cleaning, quality scoring, and activity logging.**
