from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(
        db.Integer, primary_key=True
    )  # id is an INTEGER, it MUST BE UNIQUE and it MUST MATCH the store_id in the item.py

    name = db.Column(
        db.String(80), nullable=False
    )  # name is a STRING(80 chars max) and you CAN'T CREATE a store that doesn't have a name

    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )  # lazy=dynamic means that the ITEMS variable aren't going to be fetched from the database until I tell it to
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
