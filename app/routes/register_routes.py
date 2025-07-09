from flask_mail import Message
from app.extensions import db, mail
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from app.models.client import Client
import jwt
from datetime import datetime, timedelta

register_bp = Blueprint('userregister', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['user_name', 'name', 'email', 'password', 'phone', 'address']

    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400

    # Check if user already exists
    existing_user = Client.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'])

    new_user = Client(
        user_name=data['user_name'],
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        phone=data['phone'],
        # vehicle_number=data['vehicle_number'],
        address=data['address']
    )

    token = jwt.encode({
        'user': new_user.user_name,
        'role': 'client',
        'exp': datetime.utcnow() + timedelta(days=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    db.session.add(new_user)
    db.session.commit()

    # Send welcome email
    try:
        msg = Message(
            subject="Welcome to W Square!",
            recipients=[new_user.email],
            body=f"""Hello {new_user.name},

Your account has been created successfully.

Username: {new_user.user_name}
Password: {new_user.password}

We recommend changing your password after logging in for the first time.

Thank you for registering with W Square!

Regards,
W Square Team"""
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

    return jsonify({
        "success": True,
        "message": "Registration successful",
        "token": token,
        "role": "client",
        "user": {
            "user_name": new_user.user_name,
            "name": new_user.name,
            "email": new_user.email
        }
    }), 201
