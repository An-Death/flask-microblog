# coding: utf8

from app import app


@app.route('/')
def hello_world():
    return 'Привет лошара!'
