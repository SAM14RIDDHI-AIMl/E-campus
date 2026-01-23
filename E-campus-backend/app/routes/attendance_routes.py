from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
from app import db
from app.models import Attendance, User, Subject, Class
from . import attendance_bp

@attendance_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_attendance():
    """Submit attendance (Teacher/Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data.get('subject_id') or not data.get('class_id') or not data.get('attendance'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    attendance_list = data['attendance']  # List of {student_id, status}
    
    try:
        for att in attendance_list:
            attendance_record = Attendance(
                student_id=att['student_id'],
                subject_id=data['subject_id'],
                class_id=data['class_id'],
                status=att['status'],  # 'P' or 'A'
                date=datetime.utcnow(),
                marked_by=user_id
            )
            db.session.add(attendance_record)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Attendance submitted for {len(attendance_list)} students'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@attendance_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    """Get attendance for a specific student"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Student can only view their own attendance
    if user.role == 'student' and user_id != student_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    student = User.query.get(student_id)
    
    if not student or student.role != 'student':
        return jsonify({'error': 'Student not found'}), 404
    
    # Get attendance grouped by subject
    attendances = Attendance.query.filter_by(student_id=student_id).all()
    
    # Aggregate by subject
    attendance_summary = {}
    for att in attendances:
        subject = att.subject.name
        if subject not in attendance_summary:
            attendance_summary[subject] = {'present': 0, 'total': 0}
        
        attendance_summary[subject]['total'] += 1
        if att.status == 'P':
            attendance_summary[subject]['present'] += 1
    
    result = []
    for subject, data in attendance_summary.items():
        percent = round((data['present'] / data['total']) * 100) if data['total'] > 0 else 0
        result.append({
            'subject': subject,
            'present': data['present'],
            'total': data['total'],
            'percentage': percent
        })
    
    return jsonify({
        'success': True,
        'attendance': result
    }), 200


@attendance_bp.route('/class/<int:class_id>/subject/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_class_attendance(class_id, subject_id):
    """Get attendance for a class and subject"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    attendances = Attendance.query.filter_by(
        class_id=class_id,
        subject_id=subject_id
    ).all()
    
    return jsonify({
        'success': True,
        'attendance': [att.to_dict() for att in attendances]
    }), 200


@attendance_bp.route('/statistics/<int:student_id>', methods=['GET'])
@jwt_required()
def get_attendance_stats(student_id):
    """Get overall attendance statistics for a student"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Student can only view their own stats
    if user.role == 'student' and user_id != student_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    student = User.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    total_classes = Attendance.query.filter_by(student_id=student_id).count()
    present_classes = Attendance.query.filter_by(
        student_id=student_id,
        status='P'
    ).count()
    
    percent = round((present_classes / total_classes) * 100) if total_classes > 0 else 0
    
    return jsonify({
        'success': True,
        'statistics': {
            'present': present_classes,
            'total': total_classes,
            'percentage': percent
        }
    }), 200
