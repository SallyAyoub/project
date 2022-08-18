from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Float()


class OrderItemsSchema(Schema):
    item_id = fields.Integer()
    quantity = fields.Integer()
    description = fields.String()


class OrderSchema(Schema):
    id = fields.Integer()
    employee_id = fields.Integer()
    customer_id = fields.Integer()
    order_status = fields.String()
    customer_notes = fields.String()
    order_items = fields.Nested(OrderItemsSchema, many=True)


class BillSchema(Schema):
    order_id = fields.Integer()
    customer_id = fields.Integer()
    employee_id = fields.Integer()
    price = fields.Float()
    date_time = fields.DateTime()
    orders = fields.Nested(OrderSchema)


class CustomerSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    phoneNumber = fields.String()
    orders = fields.Nested(OrderSchema, many=True)


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    phoneNumber = fields.String()
    role = fields.String()
    work_status = fields.String()
    orders = fields.Nested(OrderSchema, many=True)

    
