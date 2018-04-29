# coding: utf8


from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user

from app.forms.login_form import LoginForm
from app.models import User


class BaseView:

    def __init__(self):
        self._set_title()
        self.form = self.Meta.form() if self.Meta.form else None

    @classmethod
    def _set_title(cls):
        cls.__title__ = cls.Meta.title or cls.__name__.capitalize()

    @property
    def template(self):
        return self.Meta.template

    def render(self, template, **kwargs):
        return render_template(template, __title__=self.__title__, **kwargs)

    class Meta:
        title = None
        template = None
        form = None


class LoginView(BaseView):

    def __init__(self):
        super().__init__()
        self.user = current_user

    class Meta:
        title = 'Sing In'
        template = 'login.html'
        form = LoginForm

    def login(self):
        if self.is_authenticated:
            return redirect(url_for('index'))
        if self.form.validate_on_submit():
            try:
                return self._process_login()
            except NameError:
                return redirect(url_for('login'))
        else:
            return self._login_page()

    @property
    def is_authenticated(self):
        return self.user.is_authenticated

    @property
    def username(self):
        return self.form.username.data

    @property
    def password(self):
        return self.form.password.data

    def _login_page(self):
        return super().render(self.template, form=self.form)

    def _process_login(self):
        user = User.query.filter_by(username=self.username).first()
        self._check_user_exist(user, self.username)
        self._check_user_password(user, self.password)
        login_user(user, remember=self.form.remember_me.data)
        return redirect(url_for('index'))

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
