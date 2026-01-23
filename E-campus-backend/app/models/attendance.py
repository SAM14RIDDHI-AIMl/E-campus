from app import db
from datetime import datetime

class Attendance(db.Model):
    """Attendance model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    
    status = db.Column(db.String(1), nullable=False)  # 'P' for Present, 'A' for Absent
    date = db.Column(db.Date, default=datetime.utcnow)
    
    marked_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Teacher/Admin who marked
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subject = db.relationship('Subject', backref='attendances')
    class_obj = db.relationship('Class', backref='attendances')
    teacher = db.relationship('User', backref='marked_attendances', foreign_keys=[marked_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject.name,
            'class': self.class_obj.name,
            'status': self.status,
            'date': self.date.isoformat(),
            'marked_by': self.teacher.name if self.teacher else 'N/A'
        }
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.subject.name} - {self.status}>'
