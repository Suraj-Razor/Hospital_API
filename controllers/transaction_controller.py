from init import db, ma, jwt, bcrypt
from flask import Blueprint, request
from admin import authorise_as_admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import Transaction, transaction_schema, transactions_schema
from models.booking import Booking
from sqlalchemy import desc

transaction_bp = Blueprint("transaction_bp",__name__, url_prefix="/transactions")


@transaction_bp.route("/", methods = ["GET"])
@jwt_required()
def all_user_transactions():
    user_id = get_jwt_identity()
    stmt = db.select(Transaction).join(Booking, Booking.id == Transaction.booking_id).where(Booking.user_id == user_id)
    transactions = db.session.scalars(stmt)
    return transactions_schema.dumps(transactions)

@transaction_bp.route("/<int:booking_id>", methods = ["POST"])
@jwt_required()
def pay_booking(booking_id):
    user_id = get_jwt_identity()
    stmt = db.select(Booking).where((Booking.id == booking_id) & (Booking.user_id == user_id))
    bookings = db.session.scalar(stmt)
    if bookings:
        print(bookings.id)
        stmt = db.select(Transaction).where(Transaction.booking_id == bookings.id).order_by(desc(Transaction.id)).limit(1)
        transactions = db.session.scalar(stmt)
        if transactions and transactions.status.lower() == "refund":
            return {"error":"This booking cannot be paid, already refunded. Please create a new booking"}
        else:
            new_transaction = Transaction(
                booking_id = bookings.id,
                fee = bookings.doctor.consultation_fee,
                GST = round(bookings.doctor.consultation_fee*0.1,2),
                status = "Paid"
            )
            new_transaction.total_fee = round(new_transaction.fee + new_transaction.GST,2)
            db.session.add(new_transaction)
            bookings.status = "Confirmed"
            db.session.commit()
            return transaction_schema.dump(new_transaction)

    else:
        return {"error":f"Booking with id {booking_id} does not exist."}, 404
    
@transaction_bp.route("/<int:transaction_id>", methods = ["PUT","PATCH"])
def booking_refund(transaction_id):
    stmt = db.select(Transaction).where(Transaction.id == transaction_id)
    transactions = db.session.scalar(stmt)
    if transactions and transactions.status.lower() == "refund":
        return{"error":"this transaction has already been refunded"}, 404
    elif transactions:
        transactions.status = "refund"
        transactions.booking.status = "cancelled"
        db.session.commit()
        return transaction_schema.dump(transactions)
    else:
        return{"error":f"transaction with id {transaction_id} does not exist."},404

@transaction_bp.route("/<int:transaction_id>", methods = ["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_transactions(transaction_id):
    stmt = db.select(Transaction).where(Transaction.id == transaction_id)
    transactions = db.session.scalar(stmt)
    if transactions:
        db.session.delete(transactions)
        db.session.commit()
        return {"msg":f"Transaction with id {transaction_id} has been deleted"}
    else:
        return {"error":f"Transaction with id {transaction_id} does not exist"},404