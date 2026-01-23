from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model for both Admin and Student"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    is_active = db.Column(db.Boolean, default=True)
    
    # Student-specific fields
    student_id = db.Column(db.String(50), unique=True, nullable=True)
    class_assigned = db.Column(db.String(50), nullable=True)
    
    # Teacher-specific fields
    subject_teaching = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='student', lazy=True, foreign_keys='Attendance.student_id')
    inquiries = db.relationship('Inquiry', backref='student', lazy=True, foreign_keys='Inquiry.student_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'student_id': self.student_id,
            'class_assigned': self.class_assigned,
            'subject_teaching': self.subject_teaching,
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
