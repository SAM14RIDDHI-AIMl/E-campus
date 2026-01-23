from app import db
from datetime import datetime

class Class(db.Model):
    """Class/Section model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., "10A", "12B"
    description = db.Column(db.String(200), nullable=True)
    
    schedules = db.relationship('Schedule', backref='class_obj', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def __repr__(self):
        return f'<Class {self.name}>'


class Subject(db.Model):
    """Subject model"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # e.g., "Maths", "Physics"
    code = db.Column(db.String(20), unique=True, nullable=True)
    
    schedules = db.relationship('Schedule', backref='subject_obj', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class Schedule(db.Model):
    """Class schedule model"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    day_of_week = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.String(10), nullable=False)  # HH:MM
    end_time = db.Column(db.String(10), nullable=False)    # HH:MM
    room_number = db.Column(db.String(20), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teacher = db.relationship('User', backref='scheduled_classes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'class': self.class_obj.name,
            'subject': self.subject_obj.name,
            'teacher': self.teacher.name if self.teacher else 'N/A',
            'day_of_week': self.day_of_week,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'room_number': self.room_number
        }
    
    def __repr__(self):
        return f'<Schedule {self.class_obj.name} - {self.subject_obj.name}>'
