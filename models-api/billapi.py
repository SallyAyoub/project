from flask import jsonify

from database import db
from models.billpayment import BillPayment
from models.item import Item
from models.order import Order
from models.orderitems import OrderItems
from datetime import datetime, timezone

from schemas import BillSchema


def bill_details(id: int):
    """
    if the request method is get and the path is /bills/billid the function will return the bill with the
    id specified in path
    """
    bill = BillPayment.query.get_or_404(id)
    bill_schema = BillSchema()
    return jsonify(bill_schema.dump(bill))


def create_bill(order: Order):
    """
    if the request method is POST and the path is /bills the function add_bill will add the bill in the request body
     to the bills table, and it returns its id
    """

    local_time = datetime.now(timezone.utc).astimezone()
    local_time.isoformat()
    total_price = 0
    order_items = OrderItems.query.filter_by(order_id=order.id).all()
    for order_item in order_items:
        id = order_item.item_id
        item = Item.query.filter_by(id=id).first()
        total_price += (item.price * order_item.quantity)
    bill = BillPayment(order_id=order.id, customer_id=order.customer_id, employee_id=order.employee_id,
                       price=total_price, date_time=local_time)

    try:
        db.session.add(bill)
        db.session.commit()

    except Exception:
        return 'There was an issue adding the bill'
