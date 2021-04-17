"""
Файло локальных настроек. Эти настройки нужны для упрощения разработки.
"""
import os


DEBUG = True
ALLOWED_HOSTS = ['*']
AUTH_PASSWORD_VALIDATORS = []
os.environ['MY_SERVER_VERSION'] = '1.0.0.0'
VERSION = '1.2.3.4'
