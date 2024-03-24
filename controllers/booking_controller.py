from init import db, ma, jwt, bcrypt
from flask_bcrypt import check_password_hash, generate_password_hash
from flask import Blueprint, request
from models.booking import Booking, booking_schema, bookings_schema
from models.doctor import Doctor, doctor_schema
from datetime import timedelta, datetime, date
from admin import authorise_as_admin
from flask_jwt_extended import jwt_required, get_jwt_identity

booking_bp = Blueprint("booking_bp",__name__, url_prefix="/booking")

@booking_bp.route("/user",methods = ["GET"])
@jwt_required()
def user_bookings():

    stmt = db.select(Booking).where(Booking.user_id == get_jwt_identity())
    bookings = db.session.scalars(stmt)
    data = bookings_schema.dumps(bookings)
    if bookings:
        if data is None:
            return {"msg":"no booking found"}
        else:
            return data
    else:
        return {"error":"Login error"}

@booking_bp.route("/<int:doctor_id>", methods = ["POST"])
@jwt_required()
def book_appointment(doctor_id):
    try:
        body_data = request.get_json()
        user_id = get_jwt_identity()
        booking_date_time = body_data.get("booking_date_time")
        converted = datetime.strptime(booking_date_time, '%d/%m/%Y %H:%M:%S')

        date_time_now =  str(datetime.now().strftime('%d/%m/%y %H:%M:%S'))
        date_time_now_changed = datetime.strptime(date_time_now, '%d/%m/%y %H:%M:%S')
        
        if converted < date_time_now_changed or (converted - date_time_now_changed)> timedelta(days=30):
            return {"error":f"Booking date time should be within {date_time_now_changed} and {date_time_now_changed+timedelta(days=30)}"}, 404
        else:
            stmt = db.select(Doctor).where(Doctor.id == doctor_id)
            doctor = db.session.scalar(stmt)
            if doctor:
                booking = Booking(
                    booking_date_time = converted,
                    doctor_id = doctor_id,
                    user_id = user_id
                )
                db.session.add(booking)
                db.session.commit()
                return booking_schema.dumps(booking)
            else:
                return {"error":f"Doctor with id {doctor_id} does not exists"}, 404
    except ValueError as Error:
        return {"Format error":"Date time format should be passed as '01/06/2006 16:30:00'"}, 404

@booking_bp.route("/",methods = ["GET"])
def all_bookings():
    stmt = db.select(Booking)
    bookings = db.session.scalars(stmt)
    return bookings_schema.dump(bookings)

@booking_bp.route("/<int:booking_id>",methods = ["PUT","PATCH"])
@jwt_required()
def edit_bookings(booking_id):
    body_data = request.get_json()
    stmt = db.select(Booking).where((Booking.id == booking_id) & (Booking.user_id == get_jwt_identity()))
    bookings = db.session.scalar(stmt)
    if bookings and body_data.get("status").lower() == "cancelled":
        bookings.status = "Cancelled" 
        db.session.commit()
        return {"msg":"booking status has been sucessfully edited"}
    else:
        return {"error":"Either booking does not exist or invalid status passed. Only 'Cancelled is accepted as a valid status'"}, 400

@booking_bp.route("/<int:booking_id>",methods = ["DELETE"])
@jwt_required()
def delete_bookings(booking_id):
    stmt = db.select(Booking).where((Booking.id == booking_id) & (Booking.user_id == get_jwt_identity()))
    bookings = db.session.scalar(stmt)
    if bookings:
        db.session.delete(bookings)
        db.session.commit()
        return {"msg":"booking has been sucessfully deleted"}
    else:
        return {"error":"booking not found"}, 400