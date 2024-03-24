from init import db, ma, bcrypt, jwt
from marshmallow import fields
from marshmallow.validate import Length
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.Integer)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default= False)

    booking = db.relationship("Booking", back_populates = "user", cascade= "all, delete")
class UserSchema(ma.Schema):
    booking = fields.List(fields.Nested("BookingSchema", only=["booking_date_time","status"], exclude=["user"]))
    class Meta:
        fields = ("id","first_name", "last_name", "email", "password", "phone", "is_admin", "booking")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])