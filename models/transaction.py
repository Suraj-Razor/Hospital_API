from init import db, ma
from marshmallow import fields

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key = True)
    fee = db.Column(db.Float, nullable = False)
    GST = db.Column(db.Float, nullable = False)
    status = db.Column(db.String)
    total_fee = db.Column(db.Float, nullable = False)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable = False)

    booking = db.relationship("Booking", back_populates = "transaction")

class TransactionSchema(ma.Schema):
    booking = fields.Nested("BookingSchema", exclude=["transaction","doctor","user"])
    class Meta:
        fields = ("id","fee","GST","total_fee","status","booking")

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)