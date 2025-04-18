from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.utils.error_handlers import APIError
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        raise APIError('Missing username or password', status_code=400)
        
    if User.query.filter_by(username=data['username']).first():
        raise APIError('Username already exists', status_code=409)
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'User registered successfully'
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        raise APIError('Missing username or password', status_code=400)
        
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        raise APIError('Invalid username or password', status_code=401)
        
    # Create token with user ID as identity
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'status': 'success',
        'access_token': access_token
    }) 