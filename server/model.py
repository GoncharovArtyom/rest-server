from . import db
from sqlalchemy.dialects.postgresql import JSON


class Message(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    value = db.Column(JSON)

