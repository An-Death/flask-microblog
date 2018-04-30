# coding: utf8

__all__ = ['User', 'Post']

from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class MetaModel:
    def __repr__(self, **kwargs):
        class_name = self.__class__.__name__
        return f'<{class_name}: {" ".join(map(":".join, kwargs.items()))}>'


class Model(MetaModel, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    class Meta:
        repr_fields = ['id']

    def __repr__(self):
        kwargs = {field: str(getattr(self, field)) for field in self.Meta.repr_fields}
        return super().__repr__(**kwargs)

    def __str__(self):
        return f'"{getattr(self, self.Meta.repr_fields[0])}"'


class User(Model, UserMixin):
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    class Meta:
        repr_fields = ['username']
        key_fields = ('username', 'email')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf8')).hexdigest()
        return f'https://www.gravater.com/avatar/{digest}?d=identicon&s={size}'

    @staticmethod
    def is_exist(**kwargs):
        return User.query.filter_by(**kwargs).count()


class Post(Model):
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    class Meta:
        repr_fields = ['author', 'body']
