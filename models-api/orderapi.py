import traceback

from flask import jsonify, Response

from database import db
from models.billpayment import BillPayment
from models.item import Item
from models.order import Order
from models.orderitems import OrderItems
from schemas import OrderSchema


def list_orders():
    """
    if the request method is get and the path is /orders the function home will return the list of orders
    """
    all_orders = get_orders()
    if all_orders is not None:
        return all_orders, 200
    return {"Error": "no orders found"}, 404


def get_orders() -> Response:
    """
    get_orders will return all the order records stored in the orders table
    Returns:
        Response: a json response of all the order records
    """
    order_schema = OrderSchema(many=True)
    all_orders = Order.query.all()
    return jsonify(order_schema.dump(all_orders))


def order_details(id: int):
    """
    if the request method is get and the path is /orders/orderid the function will return the order with the
    order id specified in path
    """
    order = Order.query.get_or_404(id)
    order_schema = OrderSchema()
    return jsonify(order_schema.dump(order))


def add_order(*args, **kwargs):
    """
    if the request method is POST and the path is /orders the function will add the order in the request body
     to the orders table, and it returns its id
    """
    order_data = kwargs.get("body")
    print(order_data)
    exists = check_exist_order(order_data)
    if exists:
        return {"Error": "The order you're are trying to add already exists"}, 500

    else:
        items = order_data['order_items']
        order_data.pop('order_items')
        order = Order(**order_data)
        for item in items:
            orderItem = OrderItems(order_id=order_data['id'], **item)
            order.order_items.append(orderItem)
            db.session.add(orderItem)
        try:
            db.session.add(order)
            db.session.commit()
        except Exception:
            return 'There was an issue adding the order'
    BillPayment.create_bill(order)
    return {"Order ID": order.id}, 201


def check_exist_order(dictionary_of_order: dict) -> bool:
    """
    The check_exist function reads the order dictionary and checks if the order passed in the post body exits or
    not
    Args:
      dictionary_of_order(dict): the dictionary containing the order information
    Returns:
         boolean: if the order exits or not
    """
    orders = Order.query.all()
    if orders is None:
        return False
    for order in orders:
        if order.id == dictionary_of_order['id']:
            return True


def update_order(*args, **kwargs):
    """
    if the request method is PUT and the path is /orders/orderid the function will update the order data in
    the request body
    """
    order_id = kwargs.get("id")
    order_data = kwargs.get("body")
    exists = check_exist_order(order_data)
    if exists:
        update_order_data(order_data, order_id)
        updated_order = order_details(order_id)
        return updated_order, 201


def update_order_data(order_data: dict, id: int) -> None:
    """
    The update_order_data function reads the request body data to be updated and updates that order
    information
    Args:
      order_data(dict): the dictionary containing the new information of the order
      id(int): the id of the order to be updated
    Returns:
        None
    """
    order = Order.query.get_or_404(id)
    order.employee_id = order_data['employee_id']
    order.customer_id = order_data['customer_id']
    order.order_status = order_data['order_status']
    order.customer_notes = order_data['customer_notes']

    orderItems = OrderItems.query.filter_by(order_id=id)
    bill = BillPayment.query.filter_by(order_id=id).first()
    modified_total = 0
    items_list = order_data['order_items']
    for order_item, item_data in zip(orderItems, items_list):
        order_item.item_id = item_data['item_id']
        order_item.quantity = item_data['quantity']
        order_item.description = item_data['description']
        item = Item.query.filter_by(id=order_item.item_id).first()
        added_price = item.price * order_item.quantity
        modified_total += added_price
    bill.price = modified_total
    db.session.commit()


def delete_order(*args, **kwargs):
    """
    if the request method is DELETE and the path is /orders/orderid the function will cancel the order
    """
    order_id = kwargs.get("id")
    try:
        order = Order.query.get_or_404(order_id)
        bill = BillPayment.query.filter_by(order_id=order_id).first()
        db.session.delete(order)
        db.session.delete(bill)
        db.session.commit()
        return {"Message": "Order Has been Cancelled successfully"}, 200
    except Exception:
        return {"Error": f"The order you are trying to cancel isn't found: {traceback.format_exc()}"}, 404


def add_item_to_order(*args, **kwargs):
    """
       if the request method is Post and the path is /orders/orderid/item the function  will add an item to the order
   """
    orderID = kwargs.get("id")
    item_data = kwargs.get("body")
    order = Order.query.get_or_404(orderID)
    bill = BillPayment.query.filter_by(order_id=orderID).first()
    item = Item.query.filter_by(id=item_data['item_id']).first()
    OrderItem = OrderItems(order_id=orderID, **item_data)
    order.order_items.append(OrderItem)
    bill.price += (item.price * OrderItem.quantity)
    db.session.commit()
    order_schema = OrderSchema()
    return jsonify(order_schema.dump(order))


def delete_item_from_order(*args, **kwargs):
    """
        if the request method is delete and the path is /orders/orderId/item/itemId the function  will delete the item
        from the order
    """
    order_id = kwargs.get("id")
    item_id = kwargs.get("item_id")
    order_item = OrderItems.query.filter_by(order_id=order_id, item_id=item_id).first()
    bill = BillPayment.query.filter_by(order_id=order_id).first()
    item = Item.query.filter_by(id=item_id).first()
    bill.price -= (order_item.quantity * item.price)
    db.session.delete(order_item)
    db.session.commit()
    return order_details(order_id)