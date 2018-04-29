# coding: utf8

__all__ = ['User']

from app import db


class MetaModel:
    def __repr__(self, class_name=None, **kwargs):
        class_name = class_name or self.__class__.__name__
        return f'<{class_name}: {" ".join(map(":".join, kwargs.items()))}>'


class User(db.Model, MetaModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self, **kwargs):
        return super().__repr__(class_name='User', id=self.id, username=self.username)
