from init import db, ma
from marshmallow import fields

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key= True)
    booking_date_time = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String, default = "Booked")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable = False)
    
    user = db.relationship("User", back_populates = "booking")
    doctor = db.relationship("Doctor", back_populates = "booking")
    transaction = db.relationship("Transaction", back_populates = "booking", cascade= ["all","delete"])

class BookingSchema(ma.Schema):
    doctor = fields.Nested("DoctorSchema",only=["full_name"])
    user = fields.Nested("UserSchema", only=["first_name","last_name"])
    transaction = fields.List(fields.Nested("TransactionSchema", only=["total_fee","status"]))
    class Meta:
        fields = ("id","booking_date_time","status","user","doctor","transaction")

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)