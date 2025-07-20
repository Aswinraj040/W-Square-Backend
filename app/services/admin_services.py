#app/services/admin_services.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from app.models.admin import Admin
from app.models.vehicle import Vehicle
from app.extensions import db
from datetime import datetime, timedelta
import json
from app.models.claim import Claim 
from sqlalchemy import text, func, extract
from app.models.vehicle import Vehicle
from app.models.claim import Claim
from calendar import month_name

# Mapping month number to name (you can use calendar.month_name too)
MONTH_MAP = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

admin_services_bp = Blueprint('admin_services_bp', __name__)

@admin_services_bp.route('/admincount', methods=['GET'])
def get_admin_count():
    try:
        count = db.session.query(Admin).count()
        return jsonify({"admin_count": count}), 200
    except Exception as e:
        return jsonify({"message": "Error fetching admin count", "error": str(e)}), 500
    


@admin_services_bp.route('/typecount', methods=['GET'])
def get_type_count():
    try:
        type_count = db.session.query(Vehicle.Type).distinct().count()
        return jsonify({'type_count': type_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_services_bp.route('/claimcount', methods=['GET'])
def get_claim_count():
    try:
        claim_count = db.session.query(Claim).count()
        return jsonify({'claim_count': claim_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@admin_services_bp.route('/submitclaim', methods=['POST'])
def submit_claim():
    data = request.get_json()

    try:
        new_claim = Claim(
            vehicle_number=data['vehicle_number'],
            client_name=data['client_name'],
            insurance_company=data['insurance_company'],
            claim_number=data['claim_number'],
            accident_date=datetime.strptime(data['accident_date'], '%Y-%m-%d').date(),
            surveyor_name=data['surveyor_name'],
            surveyor_contact=data['surveyor_contact'],
            garage_location=data['garage_location'],
            remarks=json.dumps(data['remarks'])  # Store as JSON string
        )

        db.session.add(new_claim)
        db.session.commit()
        return jsonify({'message': 'Claim submitted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@admin_services_bp.route('/users', methods=['GET'])
def get_users():
    try:
        result = db.session.execute(text("SELECT DISTINCT UserName FROM vehicle WHERE UserName IS NOT NULL"))
        users = [row[0] for row in result]
        return jsonify(users), 200
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({'error': str(e)}), 500

@admin_services_bp.route('/vehicles/<username>', methods=['GET'])
def get_vehicles(username):
    try:
        query = text("SELECT RegNo FROM vehicle WHERE UserName = :username")
        result = db.session.execute(query, {'username': username})
        vehicles = [row[0] for row in result]
        return jsonify(vehicles), 200
    except Exception as e:
        print(f"Error fetching vehicles for {username}: {e}")
        return jsonify({'error': str(e)}), 500

@admin_services_bp.route('/claim-users', methods=['GET'])
def get_claim_users():
    try:
        query = text("""
            SELECT 
                c.Client_Name AS client_name,
                COUNT(DISTINCT c.Vehicle_number) AS vehicle_count
            FROM claim c
            GROUP BY c.Client_Name
            ORDER BY c.Client_Name;
        """)
        result = db.session.execute(query)
        users = [
            {
                "client_name": row.client_name,
                "vehicle_count": row.vehicle_count
            }
            for row in result
        ]
        return jsonify(users), 200
    
    except Exception as e:
        print(f"Error fetching claim users: {e}")
        return jsonify({'error': str(e)}), 500
    
@admin_services_bp.route('/claims/<client_name>', methods=['GET'])
def get_claims_by_client(client_name):
    try:
        claims = Claim.query.filter_by(client_name=client_name).all()
        result = []
        for c in claims:
            result.append({
                'vehicle_number': c.vehicle_number,
                'client_name': c.client_name,
                'insurance_company': c.insurance_company,
                'claim_number': c.claim_number,
                'accident_date': c.accident_date.strftime('%Y-%m-%d'),
                'surveyor_name': c.surveyor_name,
                'surveyor_contact': c.surveyor_contact,
                'garage_name': c.garage_name,
                'garage_location': c.garage_location,
                'remarks': c.remarks
            })
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching claims for client {client_name}: {e}")
        return jsonify({'error': str(e)}), 500
    
@admin_services_bp.route('/claims/<claim_number>', methods=['PUT'])
def update_claim(claim_number):
    try:
        data = request.get_json()
        claim = Claim.query.filter_by(claim_number=claim_number).first()
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404

        claim.vehicle_number = data.get('regNo', claim.vehicle_number)
        claim.client_name = data.get('clientName', claim.client_name)
        claim.insurance_company = data.get('insuranceCompany', claim.insurance_company)

        acc_date_str = data.get('accidentDate')
        if acc_date_str:
            from datetime import datetime
            claim.accident_date = datetime.strptime(acc_date_str, '%Y-%m-%d').date()

        claim.surveyor_name = data.get('surveyorName', claim.surveyor_name)
        claim.surveyor_contact = data.get('surveyorContact', claim.surveyor_contact)
        claim.garage_location = data.get('garageLocation', claim.garage_location)
        claim.remarks = data.get('remarks', claim.remarks)
        claim.garage_name = data.get('garageName', claim.garage_name)  # add this line

        print(f"Updating claim: {claim.claim_number} with data: {data}")
        db.session.commit()
        return jsonify({'message': 'Claim updated successfully'}), 200
    except Exception as e:
        print(f"Error updating claim {claim_number}: {e}")
        return jsonify({'error': str(e)}), 500
    
@admin_services_bp.route('/monthlyclaimdata', methods=['GET'])
def get_monthly_claims():
    print("Hello this is Admin claim data")

    results = (
        db.session.query(
            func.strftime('%m', Claim.accident_date).label('month_number'),
            func.count().label('count')
        )
        .group_by(func.strftime('%m', Claim.accident_date))
        .order_by(func.strftime('%m', Claim.accident_date))
        .all()
    )

    monthly_claims = [
        {
            'month': MONTH_MAP.get(row.month_number, 'Unknown'),
            'count': row.count
        }
        for row in results
    ]

    return jsonify({'monthly_claims': monthly_claims})

@admin_services_bp.route('/insurancerenewaldata', methods=['GET'])
def get_insurance_renewal_data():
    results = (
        db.session.query(
            extract('month', Vehicle.InsuranceExpiryDate).label('month'),
            func.count().label('count')
        )
        .filter(Vehicle.InsuranceExpiryDate.isnot(None))
        .group_by(extract('month', Vehicle.InsuranceExpiryDate))
        .order_by(extract('month', Vehicle.InsuranceExpiryDate))
        .all()
    )

    # Convert numeric month to English month name using Python's calendar module
    data = [
        {'month': month_name[int(row.month)], 'count': row.count}
        for row in results
    ]

    return jsonify({'insurance_renewals': data})
@admin_services_bp.route('/insuranceexpirycount', methods=['GET'])
def get_insurance_expiry_count():
    today = datetime.today().date()
    day_7 = today + timedelta(days=7)
    day_30 = today + timedelta(days=30)
    day_60 = today + timedelta(days=60)

    def count_expiring_before(end):
        return db.session.query(func.count()).filter(
            Vehicle.InsuranceExpiryDate <= end,
            Vehicle.InsuranceExpiryDate >= today
        ).scalar()

    counts = {
        "7_days": count_expiring_before(day_7),
        "30_days": count_expiring_before(day_30),
        "60_days": count_expiring_before(day_60)
    }

    return jsonify(counts)

@admin_services_bp.route('/vehicletypecount', methods=['GET'])
def get_vehicle_type_count():
    try:
        results = db.session.query(
            Vehicle.Type,
            func.count(Vehicle.Type)
        ).group_by(Vehicle.Type).all()

        type_counts = [{'type': type_, 'count': count} for type_, count in results]

        return jsonify({'type_counts': type_counts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_services_bp.route('/useremail/<username>', methods=['GET'])
def get_user_email(username):
    try:
        email = db.session.query(Admin.email).filter(Admin.user_name == username).scalar() 
        if email:
            return jsonify({'email': email}), 200
        else:
            return jsonify({'error': 'Email not found for this user'}), 404
    except Exception as e:
        print(f"Error fetching email for {username}: {e}")
        return jsonify({'error': str(e)}), 500