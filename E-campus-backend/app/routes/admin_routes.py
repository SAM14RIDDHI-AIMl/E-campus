from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Class, Subject
from . import admin_bp

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    role_filter = request.args.get('role')
    
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    users = query.all()
    
    return jsonify({
        'success': True,
        'users': [u.to_dict() for u in users]
    }), 200


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user details"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details (Admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'class_assigned' in data and user.role == 'student':
        user.class_assigned = data['class_assigned']
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user (Admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Prevent self-deletion
    if current_user_id == user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User deleted successfully'}), 200


@admin_bp.route('/classes', methods=['GET'])
@jwt_required()
def get_classes():
    """Get all classes"""
    classes = Class.query.all()
    return jsonify({
        'success': True,
        'classes': [cls.to_dict() for cls in classes]
    }), 200


@admin_bp.route('/classes', methods=['POST'])
@jwt_required()
def create_class():
    """Create a new class (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Class name is required'}), 400
    
    if Class.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Class already exists'}), 409
    
    cls = Class(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(cls)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Class created successfully',
        'class': cls.to_dict()
    }), 201


@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    """Get all subjects"""
    subjects = Subject.query.all()
    return jsonify({
        'success': True,
        'subjects': [sub.to_dict() for sub in subjects]
    }), 200


@admin_bp.route('/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    """Create a new subject (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Subject name is required'}), 400
    
    if Subject.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Subject already exists'}), 409
    
    subject = Subject(
        name=data['name'],
        code=data.get('code')
    )
    
    db.session.add(subject)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Subject created successfully',
        'subject': subject.to_dict()
    }), 201
