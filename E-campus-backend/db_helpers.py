"""
Database helper script for common operations
"""

from app import create_app, db
from app.models import User, Class, Subject, Schedule
from datetime import datetime

app = create_app()

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")

def drop_db():
    """Drop all tables"""
    with app.app_context():
        db.drop_all()
        print("✓ Database dropped")

def seed_db():
    """Seed database with sample data"""
    with app.app_context():
        if User.query.first():
            print("! Database already has data, skipping seed")
            return
        
        # Create users
        admin = User(
            username='admin',
            name='Admin User',
            role='admin'
        )
        admin.set_password('admin123')
        
        teacher = User(
            username='teacher1',
            name='Mr. Sharma',
            role='teacher',
            subject_teaching='Maths'
        )
        teacher.set_password('teacher123')
        
        student1 = User(
            username='student1',
            name='Raj Kumar',
            role='student',
            student_id='STU001',
            class_assigned='10A'
        )
        student1.set_password('1234')
        
        student2 = User(
            username='student2',
            name='Priya Singh',
            role='student',
            student_id='STU002',
            class_assigned='10A'
        )
        student2.set_password('1234')
        
        # Create classes
        classes = [
            Class(name='10A', description='Class 10 Section A'),
            Class(name='10B', description='Class 10 Section B'),
            Class(name='12A', description='Class 12 Section A'),
        ]
        
        # Create subjects
        subjects = [
            Subject(name='Maths', code='MAT101'),
            Subject(name='Physics', code='PHY101'),
            Subject(name='Chemistry', code='CHE101'),
            Subject(name='Computer', code='CSC101'),
        ]
        
        # Add to session
        db.session.add_all([admin, teacher, student1, student2])
        db.session.add_all(classes)
        db.session.add_all(subjects)
        db.session.commit()
        
        # Create schedules
        schedules = [
            Schedule(class_id=1, subject_id=1, teacher_id=2, day_of_week='Monday', start_time='09:00', end_time='10:00'),
            Schedule(class_id=1, subject_id=2, teacher_id=2, day_of_week='Tuesday', start_time='10:00', end_time='11:00'),
            Schedule(class_id=1, subject_id=3, teacher_id=2, day_of_week='Wednesday', start_time='11:00', end_time='12:00'),
        ]
        db.session.add_all(schedules)
        db.session.commit()
        
        print("✓ Database seeded with sample data")

def reset_db():
    """Reset database (drop and recreate)"""
    with app.app_context():
        drop_db()
        init_db()
        seed_db()
        print("✓ Database reset complete")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python db_helpers.py [init|drop|seed|reset]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'drop':
        drop_db()
    elif command == 'seed':
        seed_db()
    elif command == 'reset':
        reset_db()
    else:
        print("Invalid command. Use: init, drop, seed, or reset")
