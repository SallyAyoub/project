from database import db


class OrderItems(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(1000))  # details about the order itself
    item = db.relationship('Item')

    def __repr__(self):
        return f'Items in Order {self.quantity}'


    

