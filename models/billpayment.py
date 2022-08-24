from database import db


class BillPayment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    price = db.Column(db.Float)
    date_time = db.Column(db.DateTime)
    orders = db.relationship('Order', backref='bill', cascade='all,delete')

    def __repr__(self):
        return f' Bill : {self.price}'


