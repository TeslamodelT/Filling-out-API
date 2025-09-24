from .schemas import item_schema, items_schema
from flask import request, jsonify
from marshmallow import ValidationError 
from sqlalchemy import select 
from application.models import Item, db
from application.blueprints.items import items_bp




@items_bp.route("/items", methods=['POST'])
def create_item():
    try:
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
       
    new_item = Item(item_name=item_data['item_name'], price=item_data['price'])
    
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item), 201

#GET ALL itemS
@items_bp.route("/items", methods=['GET'])
def get_items():
    query = select(Item)
    items = db.session.execute(query).scalars().all()
    
    return items_schema.jsonify(items), 201

#GET SPECIFIC item
@items_bp.route("/<int:item_id>", methods=['GET'])
def get_item(item_id):
    item = db.session.get(item, item_id)

    if item:
        return item_schema.jsonify(item), 200
    return jsonify({"error": "item not found."}), 404

#UPDATE SPECIFIC USER
@items_bp.route("/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    item = db.session.get(item, item_id)

    if not item:
        return jsonify({"error": "item not found."}), 404
    
    try:
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in item_data.items():
        setattr(item, key, value)

    db.session.commit()
    return item_schema.jsonify(item), 200

#DELETE SPECIFIC item
@items_bp.route("/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    item = db.session.get(item, item_id)

    if not item:
        return jsonify({"error": "item not found."}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f'item id: {item_id}, successfully deleted.'}), 200