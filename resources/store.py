from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel


blueprint = Blueprint("stores", __name__, description="Operations on stores")


@blueprint.route("/store")
class StoreList(MethodView):
    @blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blueprint.arguments(StoreSchema)
    @blueprint.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store, 201


@blueprint.route("/store/<int:store_id>")
class Store(MethodView):
    @blueprint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted."}
