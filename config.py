# coding: utf8
import os


class Config:
    PROD = 'production'
    TEST = 'test'
    DEV = 'develop'

    def __new__(cls):
        env = os.environ.get('ENV')
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


class TestConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass
