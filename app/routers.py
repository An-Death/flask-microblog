# coding: utf8

from flask import render_template

from app import app
from app import helpers


@app.route('/')
@app.route('/index.html')
@helpers.title(title_name='Home')
def hello_world(*args, **kwargs):
    user = {'username': 'Name'}
    posts = [
                {
                    'author': {'username': 'Name'},
                    'body': 'Some message'

                }
            ] * 10
    return render_template('index.html', __title__=kwargs['__title__'], **locals())
