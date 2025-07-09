# app/models/client.py
from app.extensions import db

class Client(db.Model):
    __tablename__ = 'CLIENT'
    user_name = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))
    # vehicle_number = db.Column(db.String(255))