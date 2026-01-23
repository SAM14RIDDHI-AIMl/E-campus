from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Schedule, Class, Subject, User
from . import schedule_bp

@schedule_bp.route('/classes', methods=['GET'])
@jwt_required()
def get_classes():
    """Get all classes"""
    classes = Class.query.all()
    return jsonify({
        'success': True,
        'classes': [cls.to_dict() for cls in classes]
    }), 200


@schedule_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    """Get all subjects"""
    subjects = Subject.query.all()
    return jsonify({
        'success': True,
        'subjects': [sub.to_dict() for sub in subjects]
    }), 200


@schedule_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_schedules():
    """Get all schedules with optional filters"""
    class_filter = request.args.get('class')
    subject_filter = request.args.get('subject')
    
    query = Schedule.query
    
    if class_filter:
        cls = Class.query.filter_by(name=class_filter).first()
        if cls:
            query = query.filter_by(class_id=cls.id)
    
    if subject_filter:
        sub = Subject.query.filter_by(name=subject_filter).first()
        if sub:
            query = query.filter_by(subject_id=sub.id)
    
    schedules = query.all()
    
    return jsonify({
        'success': True,
        'schedule': [sch.to_dict() for sch in schedules]
    }), 200


@schedule_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_schedule(student_id):
    """Get schedule for a specific student's class"""
    user = User.query.get(student_id)
    
    if not user or user.role != 'student':
        return jsonify({'error': 'Student not found'}), 404
    
    cls = Class.query.filter_by(name=user.class_assigned).first()
    
    if not cls:
        return jsonify({'schedule': []}), 200
    
    schedules = Schedule.query.filter_by(class_id=cls.id).all()
    
    return jsonify({
        'success': True,
        'schedule': [sch.to_dict() for sch in schedules]
    }), 200


@schedule_bp.route('/create', methods=['POST'])
@jwt_required()
def create_schedule():
    """Create a new schedule (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    required_fields = ['class_id', 'subject_id', 'day_of_week', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    schedule = Schedule(
        class_id=data['class_id'],
        subject_id=data['subject_id'],
        teacher_id=data.get('teacher_id'),
        day_of_week=data['day_of_week'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        room_number=data.get('room_number')
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Schedule created successfully',
        'schedule': schedule.to_dict()
    }), 201


@schedule_bp.route('/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id):
    """Update a schedule (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    schedule = Schedule.query.get(schedule_id)
    
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
    
    data = request.get_json()
    
    if 'start_time' in data:
        schedule.start_time = data['start_time']
    if 'end_time' in data:
        schedule.end_time = data['end_time']
    if 'day_of_week' in data:
        schedule.day_of_week = data['day_of_week']
    if 'teacher_id' in data:
        schedule.teacher_id = data['teacher_id']
    if 'room_number' in data:
        schedule.room_number = data['room_number']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Schedule updated successfully',
        'schedule': schedule.to_dict()
    }), 200


@schedule_bp.route('/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(schedule_id):
    """Delete a schedule (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    schedule = Schedule.query.get(schedule_id)
    
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
    
    db.session.delete(schedule)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Schedule deleted successfully'}), 200
