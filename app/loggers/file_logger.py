# coding: utf8
import logging
import os
from logging.handlers import RotatingFileHandler

from app import app

DEFAULT_LOG_FILE_PATH = '~/app/logs'
DEFAULT_LOG_FILE_NAME = 'microblog.log'
MAX_FILE_WEIGHT = 100 * 1024 * 1024  # 100 MB


class FileLogger:
    def __init__(self, path=None, file_name=None, level='INFO'):
        self.path = path or DEFAULT_LOG_FILE_PATH
        self.file_name = file_name or DEFAULT_LOG_FILE_NAME
        self._level = level
        self._check_or_create_log_file()
        self._set_handler()

    @property
    def level(self):
        assert self._level.upper() in {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'}
        return getattr(logging, self._level.upper())

    @property
    def log_file_path(self):
        return os.path.join(self.path, self.file_name)

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, name):
        if not name.endswith('.log'):
            name = f'{name}.log'
        self._file_name = name

    def _check_or_create_log_file(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def _set_handler(self):
        file_handler = RotatingFileHandler(self.log_file_path, maxBytes=MAX_FILE_WEIGHT, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathame)s:%(lineno)s]'
        ))
        file_handler.setLevel(self.level)
        app.logget.addHandler(file_handler)
        app.logger.setLevel(self.level)
        app.logger.info(f'Microblog started')
