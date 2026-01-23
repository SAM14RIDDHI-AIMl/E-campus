# E-Campus Backend Setup Guide

## Quick Start

### 1. Install Python (if not already installed)

- Download from [python.org](https://www.python.org)
- Ensure Python 3.8+ is installed

### 2. Navigate to Backend Directory

```bash
cd "e:\Ritu project\E-campus-backend"
```

### 3. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables

```bash
# Copy example file
copy .env.example .env

# Edit .env with your settings (optional for development)
```

### 6. Run the Server

```bash
python run.py
```

Server will start at: **http://localhost:5000**

---

## Database Management

### Initialize Database

```bash
python db_helpers.py init
```

### Seed Sample Data

```bash
python db_helpers.py seed
```

### Reset Database (Drop + Recreate)

```bash
python db_helpers.py reset
```

### Access Flask Shell

```bash
python
>>> from run import app, db
>>> with app.app_context():
...     # Your database operations
```

---

## API Testing

### Using cURL

**Login:**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

**Get Current User (replace TOKEN):**

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/auth/me
```

### Using Postman

1. Import the API endpoints from the README
2. Create environment variable: `{{token}}`
3. Use login response to extract token
4. Add `Authorization: Bearer {{token}}` to headers

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "username": "admin",
    "password": "admin123"
})

token = response.json()['token']

# Get current user
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
print(response.json())
```

---

## Frontend Integration

### Update API Base URL in Frontend

In your frontend files, update the API endpoints:

**Before (Frontend only):**

```javascript
const API = "/api/admin/schedule";
fetch(API).then(...);
```

**After (With Backend):**

```javascript
const API = "http://localhost:5000/api/schedule/all";
fetch(API, {
    headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
}).then(...);
```

### Update Frontend to Use JWT Token

**studentlogin.js:**

```javascript
// Replace hardcoded login
fetch("http://localhost:5000/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username, password }),
})
  .then((res) => res.json())
  .then((data) => {
    if (data.success) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      window.location.href = "/page/student/studenthome.html";
    } else {
      alert("Invalid credentials");
    }
  });
```

### Sample Frontend Integration Code

**Make API calls with authentication:**

```javascript
// Get token from localStorage
const getToken = () => localStorage.getItem("token");

// Fetch with auth header
async function apiCall(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
  };

  if (body) options.body = JSON.stringify(body);

  return fetch(`http://localhost:5000${endpoint}`, options).then((res) =>
    res.json()
  );
}

// Usage
apiCall("/api/student/profile").then((data) => {
  console.log(data);
});
```

---

## Project Structure Details

```
E-campus-backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py         # Model imports
│   │   ├── user.py             # User model
│   │   ├── schedule.py          # Schedule, Class, Subject
│   │   ├── attendance.py        # Attendance model
│   │   └── inquiry.py           # Inquiry model
│   └── routes/
│       ├── __init__.py          # Blueprint registration
│       ├── auth.py              # Authentication
│       ├── admin_routes.py       # Admin endpoints
│       ├── student_routes.py     # Student endpoints
│       ├── schedule_routes.py    # Schedule endpoints
│       ├── attendance_routes.py  # Attendance endpoints
│       └── inquiry_routes.py     # Inquiry endpoints
├── config.py                    # Configuration
├── run.py                       # Entry point
├── db_helpers.py                # Database utilities
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore
└── README.md                    # Full documentation
```

---

## Common Issues & Solutions

### Issue: "No module named 'flask'"

**Solution:**

```bash
# Ensure venv is activated
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Database locked"

**Solution:**

```bash
# Delete the database and recreate
rm ecampus.db  # or del ecampus.db on Windows
python db_helpers.py reset
```

### Issue: "Port 5000 already in use"

**Solution:**
Edit `run.py` and change port:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Issue: CORS errors in frontend

**Solution:**
The backend already has CORS enabled. If you get CORS errors:

1. Ensure frontend URL is in `config.py` CORS_ORIGINS
2. Add header: `"Access-Control-Allow-Origin": "*"` in requests

---

## Development Tips

### Create Sample Test Data

```python
from run import app
from app.models import *

with app.app_context():
    # Check what's in database
    students = User.query.filter_by(role='student').all()
    for s in students:
        print(s.to_dict())
```

### Debug SQL Queries

In `config.py`, add:

```python
app.config['SQLALCHEMY_ECHO'] = True
```

This prints all SQL queries to console.

### View Database

Install DB viewer:

```bash
pip install db-sqlite3
```

Or use online viewer: https://sqliteonline.com

---

## Deployment Checklist

Before deploying to production:

- [ ] Change `FLASK_ENV` to `production`
- [ ] Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Set up PostgreSQL or MySQL (not SQLite)
- [ ] Configure CORS for production domain
- [ ] Set up HTTPS/SSL
- [ ] Configure proper logging
- [ ] Set up environment variables securely
- [ ] Enable CSRF protection if needed
- [ ] Set up database backups
- [ ] Use production WSGI server (Gunicorn, uWSGI)

---

## Next Steps

1. **Start the backend server** using `python run.py`
2. **Test API endpoints** using Postman or cURL
3. **Update frontend** to use the backend API endpoints
4. **Connect frontend login** to backend authentication
5. **Test full workflow** end-to-end

For detailed API documentation, see [README.md](README.md)

---

## Support

For issues or questions:

1. Check error message in console
2. Review API response in Network tab
3. Check database state using db_helpers.py
4. Review logs in Flask console
