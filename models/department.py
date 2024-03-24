from init import db, ma
from datetime import date
from marshmallow import fields

SPECIALTIES = [""]

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key = True)
    department_name = db.Column(db.String, nullable = False, unique = True)
    operating_start_hour = db.Column(db.Time, nullable = False)
    operating_end_hour = db.Column(db.Time, nullable = False)
    created_date = db.Column(db.Date)
    last_update = db.Column(db.Date)
    
    doctor = db.relationship("Doctor", back_populates = "department", cascade= "all, delete")

class DepartmentSchema(ma.Schema):
    doctor = fields.List(fields.Nested("DoctorSchema", exclude=["department","id"]))
    class Meta:
        fields = ("id","department_name","operating_start_hour","operating_end_hour","created_date","last_update", "doctor")

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)