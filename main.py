import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error":error.orig.diag.table_name}, 400
    
    @app.errorhandler(DataError)
    def data_error(error):
            return {"error":error.orig.diag.message_primary}, 400
   
    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error":f"Missing Required field: {err.orig.diag.column_name}"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error":err.orig.diag.message_detail}, 409

    from controllers.cli_controller import db_command
    app.register_blueprint(db_command) 

    from controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from controllers.department_controller import department_bp
    app.register_blueprint(department_bp)

    from controllers.doctor_controller import doctor_bp
    app.register_blueprint(doctor_bp)

    from controllers.booking_controller import booking_bp
    app.register_blueprint(booking_bp)

    from controllers.transaction_controller import transaction_bp
    app.register_blueprint(transaction_bp)

    return app