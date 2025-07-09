from app.extensions import db

class Claim(db.Model):
    __tablename__ = 'claim'

    vehicle_number = db.Column(db.String(100))
    client_name = db.Column(db.String(100))
    insurance_company = db.Column(db.String(100))
    claim_number = db.Column(db.String(100), primary_key=True)
    accident_date = db.Column(db.Date)
    surveyor_name = db.Column(db.String(100))
    surveyor_contact = db.Column(db.String(100))
    garage_name = db.Column(db.String(255))
    garage_location = db.Column(db.String(255))
    remarks = db.Column(db.Text)  # Store as JSON string