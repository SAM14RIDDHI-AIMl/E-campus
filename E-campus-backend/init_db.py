#!/usr/bin/env python
"""
Database initialization script
Resets and populates the database with sample data
"""

import os
from datetime import datetime, date
from app import create_app, db
from app.models import User, Class, Subject, Schedule, Attendance, Inquiry

def init_database():
    """Initialize database with sample data"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Drop all tables
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        # Create admin
        print("Creating admin user...")
        admin = User(
            username='admin',
            name='Admin User',
            email='admin@ecampus.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create students
        print("Creating student users...")
        student1 = User(
            username='student1',
            name='Raj Kumar',
            email='raj@ecampus.com',
            phone='9876543210',
            role='student',
            student_id='STU001',
            class_assigned='10A',
            is_active=True
        )
        student1.set_password('1234')
        db.session.add(student1)
        
        student2 = User(
            username='student2',
            name='Priya Singh',
            email='priya@ecampus.com',
            phone='9876543211',
            role='student',
            student_id='STU002',
            class_assigned='10A',
            is_active=True
        )
        student2.set_password('1234')
        db.session.add(student2)
        
        # Create teacher
        print("Creating teacher user...")
        teacher = User(
            username='teacher1',
            name='Mr. Sharma',
            email='sharma@ecampus.com',
            phone='9876543212',
            role='teacher',
            subject_teaching='Maths',
            is_active=True
        )
        teacher.set_password('teacher123')
        db.session.add(teacher)
        
        db.session.commit()
        
        # Create classes
        print("Creating classes...")
        class_10a = Class(name='10A', description='Class 10 Section A')
        class_10b = Class(name='10B', description='Class 10 Section B')
        class_12a = Class(name='12A', description='Class 12 Section A')
        db.session.add_all([class_10a, class_10b, class_12a])
        db.session.commit()
        
        # Create subjects
        print("Creating subjects...")
        math = Subject(name='Maths', code='MAT101')
        physics = Subject(name='Physics', code='PHY101')
        chemistry = Subject(name='Chemistry', code='CHE101')
        computer = Subject(name='Computer', code='CSC101')
        db.session.add_all([math, physics, chemistry, computer])
        db.session.commit()
        
        # Create schedules
        print("Creating schedules...")
        schedule1 = Schedule(
            class_id=1,
            subject_id=1,
            teacher_id=4,
            day_of_week='Monday',
            start_time='09:00',
            end_time='10:00',
            room_number='101'
        )
        schedule2 = Schedule(
            class_id=1,
            subject_id=2,
            teacher_id=4,
            day_of_week='Tuesday',
            start_time='10:00',
            end_time='11:00',
            room_number='102'
        )
        schedule3 = Schedule(
            class_id=1,
            subject_id=3,
            teacher_id=4,
            day_of_week='Wednesday',
            start_time='11:00',
            end_time='12:00',
            room_number='103'
        )
        db.session.add_all([schedule1, schedule2, schedule3])
        db.session.commit()
        
        # Create attendance records
        print("Creating attendance records...")
        attendance1 = Attendance(
            student_id=2,
            class_id=1,
            subject_id=1,
            date=date(2024, 1, 10),
            status='Present'
        )
        attendance2 = Attendance(
            student_id=2,
            class_id=1,
            subject_id=1,
            date=date(2024, 1, 11),
            status='Present'
        )
        attendance3 = Attendance(
            student_id=2,
            class_id=1,
            subject_id=1,
            date=date(2024, 1, 12),
            status='Absent'
        )
        db.session.add_all([attendance1, attendance2, attendance3])
        db.session.commit()
        
        print("\n✅ Database initialized successfully!")
        print("\nTest Credentials:")
        print("  Admin:    admin / admin123")
        print("  Student1: student1 / 1234")
        print("  Student2: student2 / 1234")
        print("  Teacher:  teacher1 / teacher123")

if __name__ == '__main__':
    init_database()
