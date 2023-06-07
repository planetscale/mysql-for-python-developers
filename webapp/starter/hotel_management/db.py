import click
import mysql.connector
import os

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        # connect to the database
        pass

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        # close the database 
        pass

def init_app(app):
    app.teardown_appcontext(close_db)
