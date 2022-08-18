from database import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_status = db.Column(db.String(200), nullable=False)
    customer_notes = db.Column(db.String(1000))
    order_items = db.relationship('OrderItems', cascade='all,delete')

    def __repr__(self):
        return f'order {self.description}'
