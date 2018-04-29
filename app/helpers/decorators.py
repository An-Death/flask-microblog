# coding: utf8
__all__ = ['title', 'jsonify', 'jencode', 'jdecode']


import json
from functools import wraps

from flask import jsonify as jsnf


def title(title_name=None):
    def title(func):
        @wraps(func)
        def wraper(*args, **kwargs):
            title = title_name or func.__name__.capitalize()
            return func(__title__=title, *args, **kwargs)
        return wraper

    return title


def jencode(**json_kwargs):
    def jencode(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return json.dumps(func(*args, **kwargs), **json_kwargs)

        return wrapper

    return jencode


def jdecode(**json_kwargs):
    def jdecode(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return json.loads(func(*args, **kwargs), **json_kwargs)

        return wrapper

    return jdecode


def jsonify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return jsnf(**func)

    return wrapper
