from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from . import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'User account is inactive'}), 403
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'name', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        role=data['role'],
        student_id=data.get('student_id'),
        class_assigned=data.get('class_assigned')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Missing password fields'}), 400
    
    user = User.query.get(user_id)
    
    if not user.check_password(data['old_password']):
        return jsonify({'error': 'Invalid old password'}), 401
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password changed successfully'}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout endpoint"""
    # JWT tokens are stateless, so logout is mainly for frontend cleanup
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
