from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(
        db.Integer, primary_key=True
    )  # id is an INTEGER and it MUST BE UNIQUE

    name = db.Column(
        db.String(80), nullable=False
    )  # name is a STRING(80 chars max) and you CAN'T CREATE an item that doesn't have a name

    description = db.Column(db.String)

    price = db.Column(
        db.Float(precision=2), unique=False, nullable=False
    )  # price is a FLOAT(x,xx), it is possible for many items to have the SAME PRICE and you CAN'T CREATE an item that doesn't have a price attached

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )  # this value has to MATCH the ID value in the store.py so it's a FOREIGN KEY meaning that it's a MAPPING from this table to a different one (from the items table to the stores table)

    store = db.relationship("StoreModel", back_populates="items")
    items = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
