import traceback
from flask import jsonify, Response
from database import db
from models.item import Item
from schemas import ItemSchema


def list_items():
    """
    if the request method is get and the path is /items the function home will return the list of items
    """
    all_items = get_items()
    if all_items is not None:
        return all_items, 200
    return {"Error": "no items found"}, 404


def get_items() -> Response:
    """
    get_items will return all the item records stored in the items table
    Returns:
        Response: a json response of all the item records
    """
    item_schema = ItemSchema(many=True)
    menu = Item.query.all()
    return jsonify(item_schema.dump(menu))


def item_details(id: int):
    """
    if the request method is get and the path is /items/itemid the function will return the item with the
    item id specified in path
    """
    item = Item.query.get_or_404(id)
    item_schema = ItemSchema()
    return jsonify(item_schema.dump(item))


def add_item(*args, **kwargs):
    """
    if the request method is POST and the path is /items the function add_item will add the item in the request body to
    the items table, and it returns its id
    """
    item_data = kwargs.get("body")
    print(item_data)
    exists = check_exist_item(item_data)
    if exists:
        return {"Error": "The item you're are trying to add already exists"}, 500

    else:
        item = Item(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except Exception:
            return 'There was an issue adding the Item'

    return {"Item ID": item_data['id']}, 201


def check_exist_item(dictionary_of_item: dict) -> bool:
    """
    The check_exist function reads the item dictionary and checks if the item passed in the post body exits or
    not
    Args:
      dictionary_of_item(dict): the dictionary containing the item information
    Returns:
         boolean: if the item exits or not
    """
    items = Item.query.all()
    if items is None:
        return False
    for item in items:
        if item.id == dictionary_of_item['id']:
            return True


def update_item(*args, **kwargs):
    """
    if the request method is PUT and the path is /items/itemid the function will update the item data in
    the request body
    """
    item_id_update = kwargs.get("id")
    item_data = kwargs.get("body")
    exists = check_exist_item(item_data)
    if exists:
        update_item_data(item_data, item_id_update)
        updated_item = item_details(item_id_update)
        return updated_item, 201


def update_item_data(item_data: dict, id: int) -> None:
    """
    The update_item_data function reads the request body data to be updated and updates that item
    information
    Args:
      item_data(dict): the dictionary containing the new information of the item
      id(int): the id of the item to be updated
    Returns:
        None
    """
    item = Item.query.get_or_404(id)
    item.name = item_data['name']
    item.price = item_data['price']
    db.session.commit()


def delete_item(*args, **kwargs):
    """
    if the request method is DELETE and the path is /items/itemid the function will delete the item data
    from the items table
    """
    item_id_delete = kwargs.get("id")
    try:
        item = Item.query.get_or_404(item_id_delete)
        db.session.delete(item)
        db.session.commit()
        return {"Message": "Item Has been Deleted successfully"}, 200
    except Exception:
        return {"Error": f"The item you are trying to delete isn't found: {traceback.format_exc()}"}, 404

