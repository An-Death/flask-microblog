# coding: utf8
from datetime import datetime

from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms.login_forms import LoginForm, RegistrationForm
from app.forms.profile_forms import EditProfileForm
from app.models import User


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


class BaseView:

    def __init__(self):
        self.form = self.Meta.form() if self.Meta.form else None
        self.user = current_user
        self.__title__ = None

    @property
    def title(self):
        return self.__title__ or \
               getattr(self.Meta, 'title')

    @title.setter
    def title(self, title=None):
        self.__title__ = title

    @property
    def template(self):
        return self.Meta.template

    @property
    def default_page(self):
        if hasattr(self.Meta, 'default_page'):
            return url_for(self.Meta.default_page)
        else:
            return url_for('/')

    def is_post(self):
        return self.form.validate_on_submit()

    def is_get(self):
        return request.method == 'GET'

    def _render_own_template(self, **kwargs):
        return render_template(self.template, __title__=self.title, form=self.form, **kwargs)

    def _get_url(self):
        next_page = request.args.get('next')
        if next_page or not url_parse(next_page).netloc != '':
            return next_page
        else:
            return self.default_page

    class Meta:
        title = None
        template = None
        form = None
        default_page = 'home'


class BaseLoginView(BaseView):

    @property
    def is_authenticated(self):
        return self.user.is_authenticated

    @property
    def username(self):
        return self.form.username.data

    @property
    def password(self):
        return self.form.password.data


class LoginView(BaseLoginView):

    def __init__(self):
        super().__init__()
        self.page = url_for('login')

    class Meta:
        title = 'Sing In'
        template = 'login.html'
        form = LoginForm
        default_page = 'home'

    def login(self):
        if self.is_authenticated:
            return redirect(self.default_page)
        if self.is_post():
            try:
                return self._process_login()
            except NameError:
                return redirect(self.page)
        else:
            return self._render_own_template()

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('login'))

    def _process_login(self):
        user = User.query.filter_by(username=self.username).first()
        self._check_user_exist(user, self.username)
        self._check_user_password(user, self.password)
        login_user(user, remember=self.form.remember_me.data)
        url = self._get_url()
        return redirect(url)

    @staticmethod
    def _check_user_exist(user, user_name):
        if not user:
            flash(f'User with username "{user_name}" doesn`t exist')
            raise NameError

    @staticmethod
    def _check_user_password(user, password):
        if not user.check_password(password):
            flash(f'Invalid password for user {user.username}')
            raise NameError


class RegisterView(BaseLoginView):

    def __init__(self):
        super().__init__()
        self.page = 'register'

    class Meta:
        title = 'Register'
        template = 'register.html'
        form = RegistrationForm
        default_page = 'login'

    @property
    def email(self):
        return self.form.email.data

    def register(self):
        if self.is_authenticated:
            return redirect(self.default_page)
        if self.is_post():
            try:
                return self._process_register()
            except NameError:
                return redirect(self.page)
        else:
            return self._render_own_template()

    def _process_register(self):
        user = User(username=self.username, email=self.email)
        user.set_password(self.password)
        db.session.add(user)
        db.session.commit()
        flash('You are registered!')
        return redirect(self.default_page)


class UserView(BaseView):
    def __init__(self, username):
        super().__init__()
        self.user = self._get_user_by_username(username)
        self.title = f'{self.user} Home Page'

    def user_home_page(self):
        posts = [
            {'author': self.user, 'body': 'Test post #1'},
            {'author': self.user, 'body': 'Test post #2'},
        ]
        return self._render_own_template(posts=posts, user=self.user)

    @staticmethod
    def _get_user_by_username(username):
        return User.query.filter_by(username=username).first_or_404()

    class Meta:
        title = 'Home Page'
        template = 'user_home_page.html'
        form = None


class EditProfileView(BaseView):
    def __init__(self):
        super().__init__()

    @property
    def default_page(self):
        return url_for(self.Meta.default_page, username=current_user.username)

    def edit(self):
        if self.is_post():
            self._save_changes()
            return redirect(self.default_page)
        elif self.is_get():
            self.form.username.data = current_user.username
            self.form.about_me.data = current_user.about_me
        return self._render_own_template()

    def _save_changes(self):
        current_user.username = self.form.username.data
        current_user.about_me = self.form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')

    class Meta:
        title = 'Edit Profile'
        template = 'edit_profile.html'
        form = EditProfileForm
        default_page = 'user'


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
