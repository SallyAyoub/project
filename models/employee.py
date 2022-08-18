from database import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phoneNumber = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    work_status = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order', backref='employee', cascade="all,delete", lazy=True)
    bill = db.relationship('BillPayment', backref='employee', cascade="all,delete", lazy=True, uselist=False)

    def __repr__(self):
        return f' Employee: {self.name}'
    
