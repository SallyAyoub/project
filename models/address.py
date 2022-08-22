from database import db


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    streetAddress = db.Column(db.String(400), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    postalCode = db.Column(db.String(200), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)


def __repr__(self):
    return f' Address: {self.streetAddress}'
