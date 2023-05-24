from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel


blueprint = Blueprint("items", "items", description="Operation on items")


@blueprint.route("/item")
class ItemList(MethodView):
    @blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blueprint.arguments(ItemSchema)
    @blueprint.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(
                item
            )  # this adds the data somewhere(not in the database just yet)
            db.session.commit()  # this adds all the data saved from the add method to the database ALL AT ONCE
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item, 201


@blueprint.route("/item/<int:item_id>")
class Item(MethodView):
    @blueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted."}

    @jwt_required(fresh=True)
    @blueprint.arguments(ItemUpdateSchema)
    @blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()

        return item
