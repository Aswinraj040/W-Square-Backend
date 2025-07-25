#app/services/client_services.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from app.models.client import Client
from app.models.vehicle import Vehicle
import os
import json
from werkzeug.utils import secure_filename
from app.extensions import db
from datetime import datetime, timedelta
from sqlalchemy import text, func, extract
from calendar import month_name
from app.models.claim import Claim
import calendar
from flask import send_from_directory


MONTH_MAP = {f"{i:02}": calendar.month_name[i] for i in range(1, 13)}

# This gets the absolute path to the 'app' folder, regardless of where this file lives
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'files')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client_services_bp = Blueprint('client_services_bp', __name__)


import os
from flask import send_from_directory, Blueprint

client_services_bp = Blueprint('client_services_bp', __name__)

# Absolute path to the 'files' directory one level above the 'app' folder
FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'files'))

@client_services_bp.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(FILES_DIR, filename)




@client_services_bp.route('/clientcount', methods=['GET'])
def get_client_count():
    try:
        count = db.session.query(Client).count()
        return jsonify({"client_count": count}), 200
    except Exception as e:
        print("ERROR in /clientcount:", e)
        return jsonify({"message": "Error fetching client count", "error": str(e)}), 500
    
@client_services_bp.route('/vehiclecount/<username>', methods=['GET'])
def get_vehicle_count(username):
    try:
        count = db.session.query(Vehicle).filter(Vehicle.UserName == username).count()
        return jsonify({"vehicle_count": count}), 200
    except Exception as e:
        print("ERROR in /vehiclecount:", e)
        return jsonify({"message": "Error fetching vehicle count", "error": str(e)}), 500
    
@client_services_bp.route('/claimcount/<username>', methods=['GET'])
def get_claim_count(username):
    try:
        count = db.session.query(Claim).filter(Claim.client_name == username).count()
        return jsonify({"claim_count": count}), 200
    except Exception as e:
        print("ERROR in /claimcount:", e)
        return jsonify({"message": "Error fetching claim count", "error": str(e)}), 500
    
@client_services_bp.route('/activeinsurancecount/<username>', methods=['GET'])
def get_active_insurance_count(username):
    try:
        # Get today's date
        today = datetime.now().date()
        
        # Query for active insurance policies
        count = db.session.query(Vehicle).filter(
            Vehicle.UserName == username,
            Vehicle.InsuranceExpiryDate >= today
        ).count()
        
        return jsonify({"active_insurance_count": count}), 200
    except Exception as e:
        print("ERROR in /activeinsurancecount:", e)
        return jsonify({"message": "Error fetching active insurance count", "error": str(e)}), 500
    
@client_services_bp.route('/expiredinsurancecount/<username>', methods=['GET'])
def get_expired_insurance_count(username):
    try:
        # Get today's date
        today = datetime.now().date()
        
        # Query for expired insurance policies
        count = db.session.query(Vehicle).filter(
            Vehicle.UserName == username,
            Vehicle.InsuranceExpiryDate < today
        ).count()
        
        return jsonify({"expired_insurance_count": count}), 200
    except Exception as e:
        print("ERROR in /expairedinsurancecount:", e)
        return jsonify({"message": "Error fetching expired insurance count", "error": str(e)}), 500


@client_services_bp.route('/addvehicles', methods=['POST'])
def add_vehicle():
    try:
        data = request.form
        insurance_expiry_date = None
        if data.get('InsuranceExpiryDate'):
            insurance_expiry_date = datetime.strptime(data['InsuranceExpiryDate'], '%Y-%m-%d').date()

        files_metadata = json.loads(data.get('files', '{}'))

        files_with_paths = {
            "Insurance": {},
            "RC": {},
            "Permit": {}
        }

        for category, year_map in files_metadata.items():
            for year, file_info in year_map.items():
                field_name = f"{category}-{year}"
                if field_name in request.files:
                    file = request.files[field_name]
                    filename = secure_filename(file.filename)
                    save_path = os.path.join(UPLOAD_FOLDER, category, year)
                    os.makedirs(save_path, exist_ok=True)
                    full_path = os.path.join(save_path, filename)
                    file.save(full_path)

                    # Update metadata with relative path
                    relative_path = os.path.relpath(full_path, BASE_DIR)
                    files_with_paths[category][year] = {
                        "filename": filename,
                        "path": f"/files/{category}/{year}/{filename}"
                    }

        vehicle = Vehicle(
            UserName=data.get('UserName'),
            RegNo=data.get('RegNo'),
            Type=data.get('Type'),
            InsuranceExpiryDate=insurance_expiry_date,
            Fuel=data.get('Fuel'),
            ChassisNumber=data.get('ChassisNumber'),
            EngineNumber=data.get('EngineNumber'),
            InsuranceNumber=data.get('InsuranceNumber'),
            files=json.dumps(files_with_paths)
        )

        existing = Vehicle.query.get(vehicle.RegNo)
        if existing:
            return jsonify({'message': 'Vehicle already exists.'}), 400

        db.session.add(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle added successfully.'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing request.'}), 500

@client_services_bp.route('/update_vehicle', methods=['POST'])
def update_vehicle():
    try:
        data = request.form
        vehicle_number = data.get('regNo')

        # Fetch the existing vehicle
        vehicle = Vehicle.query.get(vehicle_number)
        if not vehicle:
            return jsonify({'message': 'Vehicle not found'}), 404

        # Update simple fields
        vehicle.UserName = data.get('UserName')
        vehicle.RegNo = data.get('RegNo')
        vehicle.Type = data.get('Type')
        vehicle.InsuranceExpiryDate = datetime.strptime(data.get('InsuranceExpiryDate'), '%Y-%m-%d').date()
        vehicle.Fuel = data.get('Fuel')
        vehicle.ChassisNumber = data.get('ChassisNumber')
        vehicle.EngineNumber = data.get('EngineNumber')
        vehicle.InsuranceNumber = data.get('InsuranceNumber')

        # Load incoming file structure
        new_metadata = json.loads(data.get('files', '{}'))

        # Load old file structure from DB
        try:
            old_metadata = json.loads(vehicle.files or '{}')
        except Exception:
            old_metadata = {}

        # Ensure all categories exist in both
        for cat in ["Insurance", "RC", "Permit"]:
            new_metadata.setdefault(cat, {})
            old_metadata.setdefault(cat, {})

        # STEP 1: Remove deleted files
        for category in old_metadata:
            for year in list(old_metadata[category].keys()):
                if year not in new_metadata[category]:
                    # File deleted by user
                    old_file_info = old_metadata[category][year]
                    if "path" in old_file_info:
                        abs_path = os.path.join(BASE_DIR, old_file_info["path"].lstrip("/"))
                        if os.path.exists(abs_path):
                            os.remove(abs_path)
                    # Remove from old metadata
                    del old_metadata[category][year]

        # STEP 2: Add newly uploaded files
        for category, year_map in new_metadata.items():
            for year, file_info in year_map.items():
                if year not in old_metadata[category]:
                    # This is a new file
                    field_name = f"{category}-{year}"
                    if field_name in request.files:
                        file = request.files[field_name]
                        filename = secure_filename(file.filename)

                        save_path = os.path.join(UPLOAD_FOLDER, category, year)
                        os.makedirs(save_path, exist_ok=True)

                        full_path = os.path.join(save_path, filename)
                        file.save(full_path)

                        # Save relative path
                        relative_path = f"/files/{category}/{year}/{filename}"
                        old_metadata[category][year] = {
                            "filename": filename,
                            "path": relative_path
                        }

        # Save final merged file metadata
        vehicle.files = json.dumps(old_metadata)

        db.session.commit()
        return jsonify({'message': 'Vehicle updated successfully'}), 200

    except Exception as e:
        print(f"Update error: {e}")
        return jsonify({'message': 'Server error during update'}), 500



@client_services_bp.route('/get_vehicles', methods=['POST'])
def get_vehicles():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        vehicles = Vehicle.query.filter_by(UserName=username).all()

        vehicle_list = []
        for v in vehicles:
            vehicle_list.append({
                'vehicleType': v.Type,
                'fuelType': v.Fuel,
                'registrationNumber': v.RegNo,
                'insuranceExpiry': v.InsuranceExpiryDate.strftime('%Y-%m-%d') if v.InsuranceExpiryDate else '',
                'chassisNumber': v.ChassisNumber,
                'engineNumber': v.EngineNumber,
                'insuranceNumber': v.InsuranceNumber,
                'files': v.files if v.files else {}
            })

        return jsonify(vehicle_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client_services_bp.route('/monthlyclaimdata/<username>', methods=['GET'])
def get_monthly_claims(username):
    results = (
        db.session.query(
            func.strftime('%m', Claim.accident_date).label('month_number'),
            func.count().label('count')
        )
        .filter(Claim.client_name == username)
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

@client_services_bp.route('/insurancerenewaldata/<username>', methods=['GET'])
def get_insurance_renewal_data(username):
    results = (
        db.session.query(
            extract('month', Vehicle.InsuranceExpiryDate).label('month'),
            func.count().label('count')
        )
        .filter(
            Vehicle.UserName == username,
            Vehicle.InsuranceExpiryDate.isnot(None)
        )
        .group_by(extract('month', Vehicle.InsuranceExpiryDate))
        .order_by(extract('month', Vehicle.InsuranceExpiryDate))
        .all()
    )

    data = [
        {'month': month_name[int(row.month)], 'count': row.count}
        for row in results
    ]

    return jsonify({'insurance_renewals': data})

@client_services_bp.route('/insuranceexpirycount/<username>', methods=['GET'])
def get_insurance_expiry_count(username):
    today = datetime.today().date()
    day_7 = today + timedelta(days=7)
    day_30 = today + timedelta(days=30)
    day_60 = today + timedelta(days=60)

    def count_expiring_before(end):
        return db.session.query(func.count()).filter(
            Vehicle.UserName == username,
            Vehicle.InsuranceExpiryDate <= end,
            Vehicle.InsuranceExpiryDate >= today
        ).scalar()

    counts = {
        "7_days": count_expiring_before(day_7),
        "30_days": count_expiring_before(day_30),
        "60_days": count_expiring_before(day_60)
    }

    return jsonify(counts)

@client_services_bp.route('/vehicletypecount/<username>', methods=['GET'])
def get_vehicle_type_count(username):
    try:
        results = db.session.query(
            Vehicle.Type,
            func.count(Vehicle.Type)
        ).filter_by(UserName=username).group_by(Vehicle.Type).all()

        type_counts = [{'type': type_, 'count': count} for type_, count in results]

        return jsonify({'type_counts': type_counts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_services_bp.route('/useremail/<username>', methods=['GET'])
def get_user_email(username):
    try:
        email = db.session.query(Client.email).filter(Client.user_name == username).scalar() 
        if email:
            return jsonify({'email': email}), 200
        else:
            return jsonify({'error': 'Email not found for this user'}), 404
    except Exception as e:
        print(f"Error fetching email for {username}: {e}")
        return jsonify({'error': str(e)}), 500
