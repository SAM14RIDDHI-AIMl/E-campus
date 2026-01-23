from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
student_bp = Blueprint('student', __name__, url_prefix='/api/student')
schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/schedule')
attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')
inquiry_bp = Blueprint('inquiry', __name__, url_prefix='/api/inquiry')

# Import routes to register them
from . import auth, admin_routes, student_routes, schedule_routes, attendance_routes, inquiry_routes
