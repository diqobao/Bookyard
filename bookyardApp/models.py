import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import pickle
import numpy as np

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

def recommend(username, db, n = 10, top_n = 3):
    user = selectUser(username, db)
    user_list = [user[0]]
    bookId_tuple = db.execute(
        'SELECT isbn FROM Book'
    ).fetchall()
    book_list = []

    if n < top_n * 2:
        n = top_n * 2

    for tuple in bookId_tuple:
        book_list.append(tuple[0])
    with open("explicit_rec.pkl", "rb") as fid:
        pretrain_model = pickle.load(fid)

    book_list = np.random.choice(book_list, n, replace=False)

    #Choose top_n books as recommendation
    pre_result = pretrain_model.predict(user_list, book_list)
    recommended = []
    for i in range(top_n):
        print(book_list[np.argmax(pre_result)])
        pos = np.argmax(pre_result)
        recommended.append(book_list[pos])
        pre_result = np.delete(pre_result, pos)
    print(recommended)
    return recommended








