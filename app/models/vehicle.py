# app/models/vehicle.py
from app.extensions import db

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    VehicleNumber = db.Column(db.String(100), primary_key=True, nullable=False)
    UserName = db.Column(db.String(100), nullable=True)
    RegNo = db.Column(db.String(100), nullable=True)
    Type = db.Column(db.String(100), nullable=True)
    InsuranceExpiryDate = db.Column(db.Date, nullable=True)
    Fuel = db.Column(db.String(50), nullable=True)
    ChassisNumber = db.Column(db.String(100), nullable=True)
    EngineNumber = db.Column(db.String(100), nullable=True)
    InsuranceNumber = db.Column(db.String(100), nullable=True)

    