# coding: utf8
import json
from functools import wraps

from flask import jsonify as jsnf


def title(title_name=None):
    def title(func):
        @wraps(func)
        def wraper(*args, **kwargs):
            g = func.__globals__
            sentinel = object()
            oldvalue = g.get('__title__', sentinel)
            title = title_name or func.__name__
            g['__title__'] = title
            try:
                res = func(*args, **kwargs)
            finally:
                if oldvalue is sentinel:
                    del g['__title__']
                else:
                    g['__title__'] = oldvalue
            return res

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
