from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Float()


class OrderItemsSchema(Schema):
    id = fields.Integer()
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
    price = fields.Float()
    date_time = fields.DateTime()


class CustomerSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    phoneNumber = fields.String()


class AddressSchema(Schema):
    streetAddress = fields.String()
    city = fields.String()
    state = fields.String()
    postalCode = fields.String()


class EmployeeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    phoneNumber = fields.String()
    role = fields.String()
    work_status = fields.String()
    address = fields.Nested(AddressSchema)



