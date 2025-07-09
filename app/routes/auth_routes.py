# === app/routes/auth_routes.py ===
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.client import Client
from app.models.admin import Admin
from app.extensions import db, mail
from flask_mail import Message
import random
import os
from dotenv import load_dotenv

load_dotenv()

MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check admin
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        access_token = create_access_token(
            identity={"role": "admin", "user": admin.user_name},
            expires_delta=timedelta(days=1)
        )
        print(access_token)
        return jsonify(access_token=access_token), 200

    # Check client
    client = Client.query.filter_by(email=email).first()
    if client and check_password_hash(client.password, password):
        access_token = create_access_token(
            identity={"role": "client", "user": client.user_name},
            expires_delta=timedelta(days=1)
        )
        
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    return jsonify({"profile": identity}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = Client.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Email not found'}), 404

    otp = str(random.randint(100000, 999999))
    user.otp = otp
    db.session.commit()

    msg = Message(subject='Your OTP Code',
                  sender= MAIL_DEFAULT_SENDER,
                  recipients=[email])
    msg.body = f'Your OTP for password reset is: {otp}'
    mail.send(msg)

    return jsonify({'message': 'OTP sent to your email'}), 200

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    user = Client.query.filter_by(email=email, otp=otp).first()
    if user:
        return jsonify({'message': 'OTP verified'}), 200
    else:
        return jsonify({'message': 'Invalid OTP'}), 401


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = Client.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.password = generate_password_hash(new_password)
    user.otp = None  # clear OTP
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200
