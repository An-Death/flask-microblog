# coding: utf8

__all__ = ['User', 'Post']

from datetime import datetime

from app import db


class MetaModel:
    def __repr__(self, **kwargs):
        class_name = self.__class__.__name__
        return f'<{class_name}: {"|".join(map(":".join, kwargs.items()))}>'


class Model(MetaModel):
    id = db.Column(db.Integer, primary_key=True)

    class Meta:
        repr_fields = ['id']

    def __repr__(self):
        kwargs = {field: str(getattr(self, field)) for field in self.Meta.repr_fields}
        return super().__repr__(**kwargs)

    def __str__(self):
        return f'"{getattr(self, self.Meta.repr_fields[0])}"'


class User(Model, db.Model):
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    class Meta:
        repr_fields = ['username']


class Post(Model, db.Model):
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    class Meta:
        repr_fields = ['author', 'body']
