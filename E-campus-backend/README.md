# E-Campus Backend - Flask API

A comprehensive REST API backend for the E-Campus management system built with Flask, SQLAlchemy, and JWT authentication.

## Features

- **User Authentication**: Secure login/register with JWT tokens
- **Role-Based Access Control**: Admin, Teacher, and Student roles
- **Schedule Management**: Create and manage class schedules
- **Attendance Tracking**: Record and track student attendance
- **Inquiry System**: Students can submit inquiries, admins can approve/reject
- **Student Dashboard**: View attendance statistics and class schedule
- **Admin Dashboard**: Manage users, schedules, and inquiries

## Tech Stack

- Flask 2.3.3
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLite/PostgreSQL (Database)

## Project Structure

```
E-campus-backend/
├── app/
│   ├── __init__.py              # App factory
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── schedule.py          # Schedule, Class, Subject models
│   │   ├── attendance.py        # Attendance model
│   │   └── inquiry.py           # Inquiry model
│   └── routes/
│       ├── auth.py              # Authentication endpoints
│       ├── admin_routes.py       # Admin management endpoints
│       ├── student_routes.py     # Student profile endpoints
│       ├── schedule_routes.py    # Schedule endpoints
│       ├── attendance_routes.py  # Attendance endpoints
│       └── inquiry_routes.py     # Inquiry endpoints
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template
```

## Installation

1. **Clone the repository** and navigate to the backend folder:

```bash
cd E-campus-backend
```

2. **Create a virtual environment**:

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:

```bash
copy .env.example .env
```

Edit `.env` and configure:

- `SECRET_KEY`: Your Flask secret key
- `JWT_SECRET_KEY`: Your JWT secret key
- `DATABASE_URL`: Your database URL

5. **Initialize the database**:

```bash
python run.py
```

The application will automatically create sample data on first run.

## Running the Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint           | Description                     |
| ------ | ------------------ | ------------------------------- |
| POST   | `/login`           | User login                      |
| POST   | `/register`        | User registration               |
| GET    | `/me`              | Get current user (JWT required) |
| POST   | `/change-password` | Change password (JWT required)  |
| POST   | `/logout`          | Logout (JWT required)           |

### Admin Management (`/api/admin`)

| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| GET    | `/users`      | Get all users    |
| GET    | `/users/<id>` | Get user details |
| PUT    | `/users/<id>` | Update user      |
| DELETE | `/users/<id>` | Delete user      |
| GET    | `/classes`    | Get all classes  |
| POST   | `/classes`    | Create class     |
| GET    | `/subjects`   | Get all subjects |
| POST   | `/subjects`   | Create subject   |

### Schedule Management (`/api/schedule`)

| Method | Endpoint        | Description                    |
| ------ | --------------- | ------------------------------ |
| GET    | `/classes`      | Get all classes                |
| GET    | `/subjects`     | Get all subjects               |
| GET    | `/all`          | Get all schedules with filters |
| GET    | `/student/<id>` | Get student's schedule         |
| POST   | `/create`       | Create schedule                |
| PUT    | `/<id>`         | Update schedule                |
| DELETE | `/<id>`         | Delete schedule                |

### Attendance (`/api/attendance`)

| Method | Endpoint                                 | Description            |
| ------ | ---------------------------------------- | ---------------------- |
| POST   | `/submit`                                | Submit attendance      |
| GET    | `/student/<id>`                          | Get student attendance |
| GET    | `/class/<class_id>/subject/<subject_id>` | Get class attendance   |
| GET    | `/statistics/<student_id>`               | Get attendance stats   |

### Inquiry (`/api/inquiry`)

| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| POST   | `/submit`       | Submit inquiry        |
| GET    | `/all`          | Get all inquiries     |
| GET    | `/student/<id>` | Get student inquiries |
| GET    | `/<id>`         | Get inquiry details   |
| POST   | `/<id>/approve` | Approve inquiry       |
| POST   | `/<id>/reject`  | Reject inquiry        |

### Student (`/api/student`)

| Method | Endpoint     | Description          |
| ------ | ------------ | -------------------- |
| GET    | `/profile`   | Get student profile  |
| PUT    | `/profile`   | Update profile       |
| GET    | `/schedule`  | Get student schedule |
| GET    | `/dashboard` | Get dashboard data   |

## Sample Credentials

```
Admin:
  Username: admin
  Password: admin123

Student:
  Username: student1 / student2
  Password: 1234

Teacher:
  Username: teacher1
  Password: teacher123
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

To get a token, call `/api/auth/login` with credentials.

## Response Format

All API responses follow this format:

**Success:**

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

**Error:**

```json
{
  "error": "Error message"
}
```

## CORS Configuration

The API is configured to accept requests from:

- `http://localhost:5000`
- `http://localhost:3000`
- `http://127.0.0.1:5000`

Update `config.py` to allow additional origins for production.

## Database Models

### User

- username, name, email, phone
- password_hash, role, is_active
- Relationships: attendances, inquiries

### Class

- name, description
- Relationships: schedules, attendances, inquiries

### Subject

- name, code
- Relationships: schedules, attendances, inquiries

### Schedule

- class_id, subject_id, teacher_id
- day_of_week, start_time, end_time, room_number

### Attendance

- student_id, subject_id, class_id
- status (P/A), date, marked_by

### Inquiry

- student_id, subject_id, class_id
- title, description, status
- response, responded_by, responded_at

## Development Tips

- Use Flask shell for database manipulation:

  ```bash
  python
  >>> from run import app, db
  >>> with app.app_context():
  ...     # Database operations
  ```

- Check database schema:
  ```bash
  python
  >>> from app.models import *
  >>> db.create_all()
  ```

## Future Enhancements

- [ ] Email notifications
- [ ] File uploads (assignments, documents)
- [ ] Real-time notifications using WebSockets
- [ ] Advanced analytics and reporting
- [ ] Mobile app API versioning
- [ ] Rate limiting and throttling

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.
