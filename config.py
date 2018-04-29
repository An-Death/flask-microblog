# coding: utf8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    PROD = 'production'
    TEST = 'test'
    DEV = 'development'

    def __new__(cls):
        env = os.environ.get('FLASK_ENV')
        if env == cls.DEV:
            return DevConfig
        elif env == cls.TEST:
            return TestConfig
        elif env == cls.PROD:
            return ProdConfig
        raise EnvironmentError('Environment variable not configured')


class BaseConfig:
    SECRET_KEY = 'some_key'


class DevConfig(BaseConfig):
    DEBUG = 1
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "dev.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass
