from init import db, ma, bcrypt
from flask import Blueprint, request
from models.user import User, user_schema, users_schema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token
user_bp = Blueprint("user_bp", __name__, url_prefix="/user")
from datetime import timedelta
# read
@user_bp.route("/", methods = ["GET"])
def get_user():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return users_schema.dumps(users)

# create
@user_bp.route("/new", methods = ["POST"])
def create_user():
        body_data = request.get_json()
        if body_data.get("password") is None:
              return{"error":"Password cannot be null"}
        user  = User(
            first_name = body_data.get("first_name"),
            last_name = body_data.get("last_name"),
            phone = body_data.get("phone"),
            email = body_data.get("email"),
            password = bcrypt.generate_password_hash(body_data.get("password"))
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
#login
@user_bp.route("/login", methods = ["POST"])
def user_login():
      body_data = request.get_json()
      stmt = db.select(User).where(User.email == body_data.get("email"))
      user = db.session.scalar(stmt)
      if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
            token = create_access_token(identity=str(user.id),expires_delta=timedelta(days=1))
            return {
                  "email": user.email,
                  "token": token,
                  "is_admin": user.is_admin
                  }
      else:
            return {
                  "error":"Email or Password is incorrect"
            }