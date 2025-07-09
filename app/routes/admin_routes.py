# app/routes/admin_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.admin import Admin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create', methods=['POST'])
def create_admin():
    data = request.get_json()

    required_fields = ['user_name', 'email', 'password', 'create', 'update', 'read', 'delete']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f"'{field}' is required"}), 400

    # Check if username already exists
    existing_admin = Admin.query.filter_by(user_name=data['user_name']).first()
    if existing_admin:
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'])

    new_admin = Admin(
        user_name=data['user_name'],
        email=data['email'],
        password=hashed_password,
        create=bool(data['create']),
        update=bool(data['update']),
        read=bool(data['read']),
        delete=bool(data['delete'])
    )

    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': 'Admin user created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
