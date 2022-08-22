from database import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(300), nullable=False)
    orders = db.relationship('Order', backref='customer', cascade="all,delete", lazy=True)
    bill = db.relationship('BillPayment', backref='customer', cascade="all,delete", lazy=True, uselist=False)

    def __repr__(self):
        return f' Customer: {self.name}'


