# coding: utf8

from flask import render_template

from app import app
from app.helpers.decorators import title


@app.route('/')
@app.route('/index.html')
@title(title_name='Main')
def hello_world(*args, **kwargs):
    user = {'name': 'Name'}
    return render_template('index.html', __title__=kwargs['__title__'], **locals())
