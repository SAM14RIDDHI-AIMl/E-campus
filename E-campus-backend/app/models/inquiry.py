from app import db
from datetime import datetime

class Inquiry(db.Model):
    """Student Inquiry model"""
    __tablename__ = 'inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    response = db.Column(db.Text, nullable=True)
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    subject = db.relationship('Subject', backref='inquiries')
    class_obj = db.relationship('Class', backref='inquiries')
    admin = db.relationship('User', backref='responded_inquiries', foreign_keys=[responded_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'student': self.student.name,
            'student_id': self.student_id,
            'subject': self.subject.name,
            'class': self.class_obj.name,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'response': self.response,
            'responded_by': self.admin.name if self.admin else None,
            'created_at': self.created_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }
    
    def __repr__(self):
        return f'<Inquiry {self.id} - {self.title}>'
