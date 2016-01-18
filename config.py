#!/usr/bin/env python 2
"""Configuration class for managing .env for the DC2 Data Lake API."""

from __future__ import absolute_import
import ast
from flask.ext.dotenv import DotEnv

class Config:
    @classmethod
    def init_app(self, app):
        env = DotEnv()
        env.init_app(app,
                     env_file=None,
                     verbose_mode=True)
         # this will set var like a `DEVELOPMENT_DEBUG` as `DEBUG`
        prefix = self.__name__.replace('Config', '').upper()
        env.alias(maps={
            prefix + '_SECRET_KEY': 'SECRET_KEY',
            prefix + '_DEBUG': 'DEBUG'
        })
        # Set environment variable values with appropriate types
        for key, value in app.config.iteritems():
            if key == key.upper():
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
                app.config[key] = value
        return self

class ProductionConfig(Config):
    pass

class TestConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class SandboxConfig(Config):
    pass

config = {
    'default': Config,
    'sandbox': SandboxConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}