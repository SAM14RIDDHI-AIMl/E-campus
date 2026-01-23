from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Schedule, Class
from . import student_bp

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_student_profile():
    """Get student profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify({
        'success': True,
        'profile': user.to_dict()
    }), 200


@student_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_student_profile():
    """Update student profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully',
        'profile': user.to_dict()
    }), 200


@student_bp.route('/schedule', methods=['GET'])
@jwt_required()
def get_student_schedule():
    """Get schedule for logged-in student"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
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


@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_student_dashboard():
    """Get student dashboard data"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'student':
        return jsonify({'error': 'Student not found'}), 404
    
    from app.models import Attendance
    
    # Get attendance statistics
    total_classes = Attendance.query.filter_by(student_id=user_id).count()
    present_classes = Attendance.query.filter_by(
        student_id=user_id,
        status='P'
    ).count()
    
    percent = round((present_classes / total_classes) * 100) if total_classes > 0 else 0
    
    # Get schedule
    cls = Class.query.filter_by(name=user.class_assigned).first()
    schedules = Schedule.query.filter_by(class_id=cls.id).all() if cls else []
    
    return jsonify({
        'success': True,
        'dashboard': {
            'student_info': user.to_dict(),
            'attendance': {
                'present': present_classes,
                'total': total_classes,
                'percentage': percent
            },
            'schedule_count': len(schedules)
        }
    }), 200
