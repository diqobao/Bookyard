import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# get user by username
def selectUser(username, db):
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    return user

# add new user
def addUser(username, password, db):
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, password)
    )
    db.commit()

# sesarch book
def searchBook(prefix, db):
    books = db.execute(
        'SELECT * from books WHERE (lower(title) LIKE \' ?%\');',
        (prefix)
    )
    return books
