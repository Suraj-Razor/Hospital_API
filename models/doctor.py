from init import db, ma
from marshmallow import fields
class Doctor(db.Model):
    __tablename_ = "doctor"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable = False)
    registration_number = db.Column(db.Integer, nullable = False, unique = True)
    registration_expiry = db.Column(db.Date, nullable = False)
    consultation_fee = db.Column(db.Float, nullable = False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)

    department = db.relationship("Department", back_populates = "doctor")
    booking = db.relationship("Booking", back_populates = "doctor", cascade = ["all","delete"])

class DoctorSchema(ma.Schema):
    department = fields.Nested("DepartmentSchema", only=["department_name"])
    class Meta:
        fields = ("id","full_name","registration_number", "registration_expiry", "consultation_fees", "department")

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)