# coding: utf8

from flask import render_template

from app import app
from app import helpers
from app.views import LoginView


@app.route('/')
@app.route('/index.html')
@helpers.title('Home')
def home(*args, **kwargs):
    user = {'username': 'Name'}
    posts = [
                {
                    'author': {'username': 'Name'},
                    'body': 'Some message'

                },
                {
                    'author': {'username': 'Русский'},
                    'body': 'Русское сообщение'
                }
            ] * 2
    return render_template('index.html', __title__=kwargs['__title__'], **locals())


@app.route('/login', methods=['GET', 'POST'])
def login():
    return LoginView().login()
