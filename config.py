import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # Для начала мы будем использовать SQLite.
    # Потом возможно поменяем на PostgreSQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'WM.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
