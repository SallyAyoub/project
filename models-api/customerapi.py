from flask import jsonify, Response
from database import db
from models.customer import Customer
from models.order import Order
from schemas import CustomerSchema, OrderSchema


def list_customers():
    """
    if the request method is get and the path is /customers the function will return the list of customers
    """
    all_customers = get_customers()
    if all_customers is not None:
        return all_customers, 200
    return {"Error": "no customers found"}, 404


def get_customers() -> Response:
    """
    get_customers will return all the customer records stored in the customer table
    Returns:
        Response: a json response of all the customer records
    """
    customer_schema = CustomerSchema(many=True)
    all_customers = Customer.query.all()
    return jsonify(customer_schema.dump(all_customers))


def customer_details(id: int):
    """
    if the request method is get and the path is /customers/customerid the function will return the customer
    with the customer id specified in path
    """
    customer = Customer.query.get_or_404(id)
    customer_schema = CustomerSchema()
    return jsonify(customer_schema.dump(customer))


def add_customer(*args, **kwargs):
    """
    if the request method is POST and the path is /customers the function will add the customer in the request
     body to the customers table, and it returns its id
    """
    customer_data = kwargs.get("body")
    print(customer_data)
    exists = check_exist_customer(customer_data)
    if exists:
        return {"Error": "The customer you're are trying to add already exists"}, 500

    else:
        customer = Customer(**customer_data)
        try:
            db.session.add(customer)
            db.session.commit()
        except Exception:
            return 'There was an issue adding the customer'

    return {"Customer ID": customer_data['id']}, 201


def check_exist_customer(dictionary_of_customer: dict) -> bool:
    """
    The check_exist function reads the employee dictionary and checks if the employee passed in the post body exits or
    not
    Args:
      dictionary_of_customer(dict): the dictionary containing the employee information
    Returns:
         boolean: if the employee exits or not
    """
    customers = Customer.query.all()
    if customers is None:
        return False
    for customer in customers:
        if customer.id == dictionary_of_customer['id']:
            return True


def update_customer(*args, **kwargs):
    """
    if the request method is PUT and the path is /customers/customerid the function update_user will update the customer
     data in the request body
    """
    customer_id = kwargs.get("id")
    customer_data = kwargs.get("body")
    exists = check_exist_customer(customer_data)
    if exists:
        update_customer_data(customer_data, customer_id)
        updated_order = customer_details(customer_data)
        return updated_order, 201


def update_customer_data(customer_data: dict, id: int) -> None:
    """
    The update_customer_data function reads the request body data to be updated and updates that customer
    information
    Args:
      customer_data(dict): the dictionary containing the new information of the customer
      id(int): the id of the customer to be updated
    Returns:
        None
    """
    customer = Customer.query.get_or_404(id)
    customer.name = customer_data['name']
    customer.phoneNumber = customer_data['phoneNumber']
    db.session.commit()


def get_orders(*args, **kwargs):
    """
    get_orders will return all the order records stored in the orders table
    """
    id = kwargs.get("id")
    order_schema = OrderSchema(many=True)
    orders = Order.query.filter_by(customer_id=id).all()
    return jsonify(order_schema.dump(orders))
