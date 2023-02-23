from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, ForeignKey
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    surname = Column(String(200))
    password = Column(String(200))
    email = Column(String(200))
    favorite_genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = db.relationship("Genre")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    surname = fields.Str()
    password = fields.Str()
    email = fields.Str()
    favorite_genre_id = fields.Int()