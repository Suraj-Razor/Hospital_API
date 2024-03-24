from init import db, ma, jwt
from models.doctor import Doctor, doctor_schema, doctors_schema
from models.department import Department
from flask import Blueprint, request
from admin import authorise_as_admin
from flask_jwt_extended import jwt_required

doctor_bp = Blueprint("doctor_bp",__name__, url_prefix="/doctor")

@doctor_bp.route("/", methods=["GET"])
def get_all_doctors():
    stmt = db.select(Doctor)
    doctor = db.session.scalars(stmt)
    return doctors_schema.dumps(doctor)

@doctor_bp.route("/<int:department_id>/register", methods=["POST"])
@jwt_required()
@authorise_as_admin
def register_doctor(department_id):
    stmt = db.select(Department).where(Department.id == department_id)
    department = db.session.scalar(stmt)
    body_data = request.get_json()
    if department:
        doctor = Doctor(
            full_name = body_data.get("full_name"),
            registration_number = body_data.get("registration_number"),
            registration_expiry = body_data.get("registration_expiry"),
            consultation_fee = body_data.get("consultation_fee"),
            department_id = department.id
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor_schema.dump(doctor)
    else:
        return {"error":f"Department with id {department_id} does not exist."}, 404
    
@doctor_bp.route("/<int:doctor_id>", methods = ["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_doctor_profile(doctor_id):
    stmt = db.select(Doctor).where(Doctor.id == doctor_id)
    doctor = db.session.scalar(stmt)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return {"msg":f"Dr. {doctor.full_name} profile has been deleted"}
    else:
        return {"error":f"Doctor with ID {doctor_id} does not exist"}, 404
    
@doctor_bp.route("/<int:doctor_id>", methods=["PUT","PATCH"])
@jwt_required()
@authorise_as_admin
def edit_doctor_profile(doctor_id):
    body_data = request.get_json()
    department_id = body_data.get("department_id")
    stmt = db.select(Department).where(Department.id == department_id)
    department = db.session.scalar(stmt)
    if department:
        stmt = db.select(Doctor).where(Doctor.id == doctor_id)
        doctor = db.session.scalar(stmt)
        if doctor:
            doctor.full_name = body_data.get("full_name") or doctor.full_name
            doctor.registration_number = body_data.get("registration_number") or doctor.registration_number
            registration_expiry = body_data.get("registration_expiry") or doctor.registration_expiry
            consultation_fee = body_data.get("consultation_fee") or doctor.consultation_fee
            doctor.department_id = department_id or doctor.department_id 
            db.session.commit()
            return doctor_schema.dump(doctor)
        else:
            return {"error":f"Doctor with ID {doctor_id} does not exist"}, 404
    else:
        return{"error":f"Department with id {department_id} does not exist"}, 404