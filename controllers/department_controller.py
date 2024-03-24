from init import db, ma, jwt
from models.department import Department, department_schema, departments_schema
from flask import Blueprint, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from admin import authorise_as_admin
import functools

def check_date_time(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        body_data = request.get_json()
        start_hour_str = body_data.get("operating_start_hour")
        end_hour_str = body_data.get("operating_end_hour")
        if start_hour_str is None or end_hour_str is None:
            return {"error": "Operating start hour and end hour are required."}, 400
        try:
            start_hour = datetime.strptime(start_hour_str, "%H:%M").time()
            end_hour = datetime.strptime(end_hour_str, "%H:%M").time()
        except ValueError:
            return {"error": "Invalid time format. Please provide time in HH:MM format."}, 400

        if end_hour < start_hour:
            return {"error": "Operating end hour cannot be less than operating start hour."}, 400

        return fn(*args, **kwargs)

    return wrapper


department_bp = Blueprint("department_bp",__name__, url_prefix="/department")

@department_bp.route("/", methods = ["GET"])
def list_all_department():
    stmt = db.select(Department)
    department = db.session.scalars(stmt)
    return departments_schema.dumps(department)

@department_bp.route("/new", methods= ["POST"])
@jwt_required()
@check_date_time
@authorise_as_admin
def add_new_department():
    body_data = request.get_json()
    department = Department(
        department_name = body_data.get("department_name"),
        operating_start_hour = body_data.get("operating_start_hour"),
        operating_end_hour = body_data.get("operating_end_hour"),
        created_date = datetime.now(),
        last_update = datetime.now()
    )
    db.session.add(department)
    db.session.commit()
    return department_schema.dump(department)

@department_bp.route("/<int:department_id>", methods= ["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
@check_date_time
def edit_department(department_id):
    body_data = request.get_json()
    stmt = db.select(Department).where(Department.id == department_id)
    department = db.session.scalar(stmt)
    if department:
        department.department_name= body_data.get("department_name") or department.department_name,
        department.operating_start_hour=  body_data.get("operating_start_hour") or department.operating_start_hour,
        department.operating_end_hour=  body_data.get("operating_end_hour") or department.operating_end_hour,
        department.last_update = datetime.now()
        db.session.commit()
        return department_schema.dump(department)
    else:
        return {"error":f"Department id {department_id} does not exist"}, 404


@department_bp.route("/<int:department_id>", methods= ["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_department(department_id):
    stmt = db.select(Department).where(Department.id == department_id)
    department = db.session.scalar(stmt)
    if department:
        db.session.delete(department)
        db.session.commit()
        return {"msg":f"Department {department.department_name} has been deleted"}
    else:
        return {"error":f"Department id {department_id} does not exist"}, 404
