import os
from app import create_app, db
from app.models import User, Schedule, Subject, Class, Attendance, Inquiry

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Schedule': Schedule,
        'Subject': Subject,
        'Class': Class,
        'Attendance': Attendance,
        'Inquiry': Inquiry
    }

@app.before_request
def initialize_database():
    """Initialize sample data if database is empty"""
    if User.query.first() is None:
        create_sample_data()

def create_sample_data():
    """Create sample data for development"""
    # Create default admin
    admin = User(
        username='admin',
        name='Admin User',
        email='admin@ecampus.com',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    
    # Create sample students
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
    
    # Create sample teacher
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
    
    # Create classes
    class_10a = Class(name='10A', description='Class 10 Section A')
    class_10b = Class(name='10B', description='Class 10 Section B')
    class_12a = Class(name='12A', description='Class 12 Section A')
    
    # Create subjects
    math = Subject(name='Maths', code='MAT101')
    physics = Subject(name='Physics', code='PHY101')
    chemistry = Subject(name='Chemistry', code='CHE101')
    computer = Subject(name='Computer', code='CSC101')
    
    # Create schedules
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
    
    # Add all to session
    db.session.add_all([
        admin, student1, student2, teacher,
        class_10a, class_10b, class_12a,
        math, physics, chemistry, computer
    ])
    db.session.commit()
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
