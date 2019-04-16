import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import pickle
import numpy as np
from lightfm import LightFM
from scipy.sparse import coo_matrix, csr_matrix

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

# Search book by prefix
def searchBook(prefix, db):
    books = db.execute(
        "SELECT * from book Where title LIKE '"+prefix+"%'"
    ).fetchall()
    return books

def addRating(db, userId, bookId, rating):

    return

class Operation:
    user_count = 0
    book_count = 0
    db = None
    sm = None
    user_list = []
    book_list = []
    rating = []
    def __init__(self, db):
        self.db = db
        self.user_count = db.execute(
            'SELECT COUNT(DISTINCT userid) FROM rating'
        ).fetchone()[0]
        self.book_count = db.execute(
            'SELECT COUNT(DISTINCT book) FROM rating'
        ).fetchone()
        users_ratings_tuples = self.db.execute(
            'SELECT * FROM rating WHERE'
        ).fetchone()
        for tuple in users_ratings_tuples:
            self.user_list.append(tuple[0])
            self.book_list.append(tuple[1])
            self.rating.append(tuple[2])

    # 需要rating的table, userid, book, rating
    def reTrain_addNewUser(self, username):
        users_ratings_tuples = self.db.execute(
            'SELECT * FROM rating WHERE username = ?', (username,)
        ).fetchall()[0]

        for tuple in users_ratings_tuples:
            self.user_list.append(tuple[0])
            self.book_list.append(tuple[1])
            self.rating.append(tuple[2])

        sm = coo_matrix((self.rating,(self.user_list, self.book_list)), shape=(self.user_count + 1, self.book_count + 1), dtype=np.float32)
        pretrain_model = LightFM(loss="warp").fit(sm, epochs=10)
        with open("utils/explicit_rec.pkl", "wb") as fid:
            pickle.dump(pretrain_model, fid)

    def reTrain_changeRating(self, username):
        users_ratings_tuples = self.db.execute(
            'SELECT * FROM rating WHERE username = ?', (username,)
        ).fetchall()[0]

        user_list = []
        book_list = []
        rating = []
        for tuple in users_ratings_tuples:
            user_list.append(tuple[0])
            book_list.append(tuple[1])
            rating.append(tuple[2])

        sm = coo_matrix((rating, (user_list, book_list)),
                        shape=(self.user_count + 1, self.book_count + 1), dtype=np.float32)
        # etrain the modelr
        with open("utils/explicit_rec.pkl", "rb") as fid:
            pretrain_model = pickle.load(fid)
        pretrain_model.fit_partial(sm, epochs=5)
        with open("utils/explicit_rec.pkl", "wb") as fid:
            pickle.dump(pretrain_model, fid)


    def recommend(self, user_id, n = 10, top_n = 3):
        user = self.db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        user_list = list(user)
        bookId_tuple = self.db.execute(
            'SELECT isbn FROM Book'
        ).fetchall()
        book_list = []
        if n < top_n * 2:
            n = top_n * 2

        for tuple in bookId_tuple:
            book_list.append(tuple[0])
        with open("utils/explicit_rec.pkl", "rb") as fid:
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
            book_list = np.delete(book_list, pos)


        return recommended








