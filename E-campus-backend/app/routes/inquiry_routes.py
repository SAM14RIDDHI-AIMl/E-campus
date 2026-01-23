from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Inquiry, User, Subject, Class
from . import inquiry_bp

@inquiry_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_inquiry():
    """Submit an inquiry (Student only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    required_fields = ['subject_id', 'class_id', 'title', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    inquiry = Inquiry(
        student_id=user_id,
        subject_id=data['subject_id'],
        class_id=data['class_id'],
        title=data['title'],
        description=data['description'],
        status='pending'
    )
    
    db.session.add(inquiry)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Inquiry submitted successfully',
        'inquiry': inquiry.to_dict()
    }), 201


@inquiry_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_inquiries():
    """Get all inquiries (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Optional filters
    status_filter = request.args.get('status')
    class_filter = request.args.get('class')
    subject_filter = request.args.get('subject')
    
    query = Inquiry.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if class_filter:
        cls = Class.query.filter_by(name=class_filter).first()
        if cls:
            query = query.filter_by(class_id=cls.id)
    
    if subject_filter:
        sub = Subject.query.filter_by(name=subject_filter).first()
        if sub:
            query = query.filter_by(subject_id=sub.id)
    
    inquiries = query.all()
    
    return jsonify({
        'success': True,
        'inquiries': [inq.to_dict() for inq in inquiries]
    }), 200


@inquiry_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_inquiries(student_id):
    """Get inquiries for a specific student"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Student can only view their own inquiries
    if user.role == 'student' and user_id != student_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    student = User.query.get(student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    inquiries = Inquiry.query.filter_by(student_id=student_id).all()
    
    return jsonify({
        'success': True,
        'inquiries': [inq.to_dict() for inq in inquiries]
    }), 200


@inquiry_bp.route('/<int:inquiry_id>/approve', methods=['POST'])
@jwt_required()
def approve_inquiry(inquiry_id):
    """Approve an inquiry (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    inquiry = Inquiry.query.get(inquiry_id)
    
    if not inquiry:
        return jsonify({'error': 'Inquiry not found'}), 404
    
    data = request.get_json()
    
    inquiry.status = 'approved'
    inquiry.response = data.get('response', '')
    inquiry.responded_by = user_id
    inquiry.responded_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Inquiry approved',
        'inquiry': inquiry.to_dict()
    }), 200


@inquiry_bp.route('/<int:inquiry_id>/reject', methods=['POST'])
@jwt_required()
def reject_inquiry(inquiry_id):
    """Reject an inquiry (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    inquiry = Inquiry.query.get(inquiry_id)
    
    if not inquiry:
        return jsonify({'error': 'Inquiry not found'}), 404
    
    data = request.get_json()
    
    inquiry.status = 'rejected'
    inquiry.response = data.get('response', '')
    inquiry.responded_by = user_id
    inquiry.responded_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Inquiry rejected',
        'inquiry': inquiry.to_dict()
    }), 200


@inquiry_bp.route('/<int:inquiry_id>', methods=['GET'])
@jwt_required()
def get_inquiry(inquiry_id):
    """Get a specific inquiry"""
    inquiry = Inquiry.query.get(inquiry_id)
    
    if not inquiry:
        return jsonify({'error': 'Inquiry not found'}), 404
    
    return jsonify({
        'success': True,
        'inquiry': inquiry.to_dict()
    }), 200
