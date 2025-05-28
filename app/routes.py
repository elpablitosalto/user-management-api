from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from functools import wraps

from app.models import User, Role
from app.schemas import UserSchema, UserResponseSchema, LoginSchema, TokenSchema

# Initialize schemas
user_schema = UserSchema()
user_response_schema = UserResponseSchema()
login_schema = LoginSchema()
token_schema = TokenSchema()

# Create blueprints
auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.role.name != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = user_schema.load(request.get_json())
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role_id=data['role_id']
        )
        
        from app import db
        db.session.add(user)
        db.session.commit()
        
        return user_response_schema.dump(user), 201
    
    except ValidationError as err:
        return jsonify(err.messages), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.get_json())
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'User account is disabled'}), 401
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return token_schema.dump({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    except ValidationError as err:
        return jsonify(err.messages), 400

@users_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify(user_response_schema.dump(users, many=True)), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    if current_user.id != user_id and current_user.role.name != 'admin':
        return jsonify({'message': 'Access denied'}), 403
    
    return user_response_schema.dump(user), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    
    if current_user.id != user_id and current_user.role.name != 'admin':
        return jsonify({'message': 'Access denied'}), 403
    
    try:
        data = user_schema.load(request.get_json(), partial=True)
        
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'message': 'Username already exists'}), 400
            user.username = data['username']
        
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'message': 'Email already exists'}), 400
            user.email = data['email']
        
        if 'password' in data:
            user.set_password(data['password'])
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        if 'role_id' in data and current_user.role.name == 'admin':
            user.role_id = data['role_id']
        
        from app import db
        db.session.commit()
        return user_response_schema.dump(user), 200
    
    except ValidationError as err:
        return jsonify(err.messages), 400

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    from app import db
    db.session.delete(user)
    db.session.commit()
    return '', 204 