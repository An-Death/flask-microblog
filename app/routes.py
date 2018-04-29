# coding: utf8

from flask import render_template, redirect, flash

from app import app
from app import helpers
from app.forms.login_form import LoginForm


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
@helpers.title('Login')
def login(*args, **kwargs):
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged by {form.username.data} remember {form.remember_me.data}')
        return redirect('/')
    return render_template('login.html', __title__=kwargs['__title__'], **locals())
