# app/models/admin.py
from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'admin'

    user_name = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    create = db.Column(db.Boolean, nullable=True)
    update = db.Column(db.Boolean, nullable=True)
    read = db.Column(db.Boolean, nullable=True)
    delete = db.Column(db.Boolean, nullable=True)
