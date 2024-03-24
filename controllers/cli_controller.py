from init import db, ma, bcrypt
from flask import Blueprint
from models.user import User
from models.department import Department
from models.doctor import Doctor
from datetime import date
from models.booking import Booking
from models.transaction import Transaction
db_command = Blueprint("db", __name__)

@db_command.cli.command("create")
def create_table():
    db.create_all()
    print("Tables Created")

@db_command.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Tables Dropped")

@db_command.cli.command("seed")
def seed_table():
    users = [
        User(
            first_name = "Admin f_Name",
            last_name = "Admin l_Name",
            email = "admin@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            phone = 1234567890,
            is_admin = True
        ),User(
            first_name = "User1 First Name",
            last_name = "User1 Last Name",
            email = "user1@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            phone = 1234567890
        ),
        User(
            first_name = "User2 First Name",
            last_name = "User2 Last Name",
            email = "user2@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
            phone = 1234567890
        )
    ]
    db.session.add_all(users)

    departments = [
    Department(
        department_name="Emergency Department (ED)",
        operating_start_hour="00:00:00",
        operating_end_hour="23:59:59",
        created_date = date.today(),
        last_update = date.today()
        
    ),
    Department(
        department_name="Pediatrics",
        operating_start_hour="08:00:00",
        operating_end_hour="20:00:00",
        created_date = date.today(),
        last_update = date.today()
    ),
    Department(
        department_name="Orthopedics",
        operating_start_hour="08:00:00",
        operating_end_hour="18:00:00",
        created_date = date.today(),
        last_update = date.today()
    ),
    Department(
        department_name="Cardiology",
        operating_start_hour="08:00:00",
        operating_end_hour="20:00:00",
        created_date = date.today(),
        last_update = date.today()
    ),
    Department(
        department_name="Oncology",
        operating_start_hour="08:00:00",
        operating_end_hour="17:00:00",
        created_date = date.today(),
        last_update = date.today()
    ),
    Department(
        department_name="Radiology",
        operating_start_hour="08:00:00",
        operating_end_hour="22:00:00",
        created_date = date.today(),
        last_update = date.today()
    )
    ]
    db.session.add_all(departments)
    doctors = [
        Doctor(
            full_name = "doctor1",
            registration_number = "123456",
            registration_expiry = "2026-12-27",
            consultation_fee = 200.99,
            department = departments[0]
        ),
        Doctor(
            full_name = "doctor2",
            registration_number = "1232456",
            registration_expiry = "2028-12-27",
            consultation_fee = 500.99,
            department = departments[1]
        ),
        Doctor(
            full_name = "doctor3",
            registration_number = "1234556",
            registration_expiry = "2023-12-27",
            consultation_fee = 600.00,
            department = departments[2]
        ),
        Doctor(
            full_name = "doctor4",
            registration_number = "125532456",
            registration_expiry = "2028-12-27",
            consultation_fee = 900.99,
            department = departments[1]
        ),
        Doctor(
            full_name = "doctor5",
            registration_number = "1234536",
            registration_expiry = "2024-12-27",
            consultation_fee = 300.99,
            department = departments[3]
        ),
        Doctor(
            full_name = "doctor6",
            registration_number = "12323456",
            registration_expiry = "2023-12-27",
            consultation_fee = 700.99,
            department = departments[4]
        ),
        Doctor(
            full_name = "doctor8",
            registration_number = "11234546",
            registration_expiry = "2024-12-27",
            consultation_fee = 1200.99,
            department = departments[5]
        ),
        Doctor(
            full_name = "doctor7",
            registration_number = "1232312456",
            registration_expiry = "2025-12-27",
            consultation_fee = 1400.99,
            department = departments[5]
        )
    ]
    db.session.add_all(doctors)
    booking = [
        Booking(
            booking_date_time = "2025/03/25 09:00:00",
            user = users[1],
            doctor = doctors[1],
            status = "Confirmed"
        ),
        Booking(
            booking_date_time = "2025/03/25 09:30:00",
            user = users[1],
            doctor = doctors[1],
            status = "Confirmed"
        ),
        Booking(
            booking_date_time = "2025/03/25 14:00:00",
            user = users[1],
            doctor = doctors[1]
        ),              
    ]
    db.session.add_all(booking)

    transaction = [
        Transaction(
            fee = doctors[0].consultation_fee,
            GST = round(doctors[0].consultation_fee * 0.1, 2),
            total_fee = round(((doctors[0].consultation_fee)*0.1)+doctors[0].consultation_fee, 2),
            booking = booking[0],
            status = "Paid"
        ),
        Transaction(
            fee = doctors[1].consultation_fee,
            GST = round(doctors[1].consultation_fee * 0.1, 2),
            total_fee = round(((doctors[0].consultation_fee)*0.1)+doctors[0].consultation_fee, 2),
            booking = booking[1],
            status = "Paid"
        ),
    ]
    db.session.add_all(transaction)
    db.session.commit()
    print("Tables Seeded")