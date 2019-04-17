import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import pickle
import numpy as np
from lightfm import LightFM
from scipy.sparse import coo_matrix, csr_matrix
import os

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
def searchBook(prefix, db, userId):
    books = db.execute(
        "SELECT * from book Left JOIN rating ON book.bookID = rating.bookID AND rating.userId = {} Where title LIKE \'%".format(userId)+prefix+"%'"
    ).fetchall()
    return books

def selectBook(db, bookId):
    books = db.execute(
        "SELECT * from book Where bookId = ?", (bookId,)
    ).fetchone()
    return books

# Get ratings from a user
def searchRatingIns(db, userId, bookId):
    rating = db.execute(
        'SELECT * FROM rating WHERE userId = ? AND bookId = ?', (userId, bookId)
    ).fetchone()

    return rating

# Add rating data
def addRating(db, userId, bookId, rating):
    db.execute(
        'INSERT INTO rating (userId, bookId, rating) VALUES (?, ?, ?)',
        (userId, bookId, rating)
    )
    db.commit()
    return

def deleteRating(db, userId, bookId):
    db.execute(
        'DELETE FROM rating WHERE userId = ? AND bookId = ?', (userId, bookId)
    )
    db.commit()
    return

# Get ratings from a user
def getRatingbyUser(db, userId):
    userRatings = db.execute(
        'SELECT * FROM rating WHERE userId = ?', (userId,)
    ).fetchall()

    return userRatings

# Get ratings for a book
def getRatingbyBook(db, bookId):
    bookRatings = db.execute(
        'SELECT * FROM rating WHERE bookId = ?', (bookId,)
    ).fetchall()

    return bookRatings

def getBooksbyUser(db, userId):
    userBooks = db.execute(
        'SELECT * FROM rating Left JOIN book ON book.bookID = rating.bookId WHERE userId = ?', (userId,)
    ).fetchall()

    return userBooks

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
            'SELECT COUNT(DISTINCT bookid) FROM rating'
        ).fetchone()
        users_ratings_tuples = self.db.execute(
            'SELECT * FROM rating'
        ).fetchall()
        for tuple in users_ratings_tuples:
            self.user_list.append(tuple[0])
            self.book_list.append(tuple[1])
            self.rating.append(tuple[2])
        self.basepath = os.path.dirname(__file__)
    # 需要rating的table, userid, book, rating
    def reTrain(self, userid):
        if(self.user_count > 278854):
            users_ratings_tuples = self.db.execute(
                'SELECT * FROM rating WHERE userid = ?', (userid,)
            ).fetchall()
            for tuple in users_ratings_tuples:
                self.user_list.append(tuple[0])
                self.book_list.append(tuple[1])
                self.rating.append(tuple[2])

            sm = coo_matrix((self.rating,(self.user_list, self.book_list)), shape=(self.user_count + 1, self.book_count + 1), dtype=np.float32)
            pretrain_model = LightFM(loss="warp").fit(sm, epochs=10)
            filepath = os.path.abspath(os.path.join(self.basepath, "utils/explicit_rec.pkl"))
            with open(filepath, "wb") as fid:
                pickle.dump(pretrain_model, fid)
        else:
            users_ratings_tuples = self.db.execute(
                'SELECT * FROM rating WHERE userid = ?', (userid,)
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
            filepath = os.path.abspath(os.path.join(self.basepath, "utils/explicit_rec.pkl"))
            with open(filepath, "rb") as fid:
                pretrain_model = pickle.load(fid)
            pretrain_model.fit_partial(sm, epochs=5)
            with open(filepath, "wb") as fid:
                pickle.dump(pretrain_model, fid)



    # def reTrain_changeRating(self, username):
    #     users_ratings_tuples = self.db.execute(
    #         'SELECT * FROM rating WHERE userid = ?', (username,)
    #     ).fetchall()[0]
    #
    #     user_list = []
    #     book_list = []
    #     rating = []
    #     for tuple in users_ratings_tuples:
    #         user_list.append(tuple[0])
    #         book_list.append(tuple[1])
    #         rating.append(tuple[2])
    #
    #     sm = coo_matrix((rating, (user_list, book_list)),
    #                     shape=(self.user_count + 1, self.book_count + 1), dtype=np.float32)
    #     # etrain the modelr
    #     filepath = os.path.abspath(os.path.join(self.basepath, "utils/explicit_rec.pkl"))
    #     with open(filepath, "rb") as fid:
    #         pretrain_model = pickle.load(fid)
    #     pretrain_model.fit_partial(sm, epochs=5)
    #     with open(filepath, "wb") as fid:
    #         pickle.dump(pretrain_model, fid)


    def recommend(self, user_id, n = 4, top_n = 1):
        user_list = [user_id]
        bookId_tuple = self.db.execute(
            'SELECT bookId FROM book'
        ).fetchall()
        book_list = []
        if n < top_n * 2:
            n = top_n * 2

        for tuple in bookId_tuple:
            book_list.append(tuple[0])

        filepath = os.path.abspath(os.path.join(self.basepath, "utils/explicit_rec.pkl"))
        with open(filepath, "rb") as fid:
            pretrain_model = pickle.load(fid)

        book_list = np.random.choice(book_list, n, replace=True)

        #Choose top_n books as recommendation
        pre_result = pretrain_model.predict(user_list, book_list)
        recommended = []
        for i in range(top_n):
            pos = np.argmax(pre_result)
            recommended.append(book_list[pos])
            pre_result = np.delete(pre_result, pos)
            book_list = np.delete(book_list, pos)
        rmd_result = []
        for bookId in recommended:
            tmp = self.db.execute(
                'SELECT * FROM book WHERE bookId = ?', (int(bookId),)
            ).fetchone()
            rmd_result.append(tmp)
        return rmd_result








