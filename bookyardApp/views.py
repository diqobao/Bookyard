from flask import Flask
from flask import render_template
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bookyardApp.db import get_db
import bookyardApp.models as models

viewsbp = Blueprint('views', __name__)

# Homepage
@viewsbp.route('/')
def index():
    db = get_db()
    books = models.getBooksbyUser(db, g.user)
    return render_template('index.html', books=books)

@viewsbp.route('/search_book/<prefix>', methods=('GET', 'POST'))
def search_book(prefix='a'):
    db = get_db()
    books = models.searchBook(prefix, db, g.user)
    rated_books = models.getRatingbyUser(db, g.user)
    if request.method == 'POST':
        if request.form['name'] == 'bookSearch':
            prefix = request.form['bookSearch']
            return redirect(url_for('views.search_book', prefix=prefix))
        elif request.form['name'] == 'bookPreference':
            bookId = request.form['bookId']
            rating = request.form['rating']
            inst = models.searchRatingIns(db, g.user, bookId)
            if inst is not None:
                if inst['rating'] != rating:
                    models.deleteRating(db, g.user, bookId)
                    models.addRating(db, g.user, bookId, rating)
            else:
                models.addRating(db, g.user, bookId, rating)

            return redirect(request.referrer)

    return render_template('search_book.html', books=books, rated_books=rated_books)


@viewsbp.route('/recommend_book', methods=('GET', 'POST'))
def recommend_book():
    user_id = session.get('user_id')
    db = get_db()
    liked_bookId = db.execute(
        'SELECT * FROM rating WHERE rating > 5 AND userid = ?', (user_id,)
    )
    op = models.Operation(get_db())
    books = op.recommend(user_id, 20, 3)
    if request.method == 'GET':
        return render_template('recommend.html', books=books, liked_bookId=liked_bookId)
    elif request.method == 'POST':
        bookId = request.form['bookId']
        like = request.form['preference']
        # print("books******************************************")
        # print(bookId)
        # print(like)
        if like == "like":
            print("I am in like")
            print("books******************************************")
            print(models.selectBook(db, bookId)['title'])
            models.deleteRating(db, g.user, bookId)
            models.addRating(db, g.user, bookId, rating=6)
            flash("You Like {}.".format(models.selectBook(db, bookId)['title']))
        else:
            print("I am in un-like")
            models.deleteRating(db, g.user, bookId)
            flash("You don't like {}.".format(models.selectBook(db, bookId)['title']))
        return render_template('recommend.html', books=books, liked_bookId=liked_bookId)


@viewsbp.route('/recommend_book', methods=('GET', 'POST'))
def save_preference():
    db = get_db()
    bookId = request.form['bookId']
    like = request.form['preference']
    # print("books******************************************")
    # print(bookId)
    # print(like)
    if request.method == 'POST':
        if like == "like":
            print("I am in like")
            models.deleteRating(db, g.user, bookId)
            models.addRating(db, g.user, bookId, rating=6)
            print("books******************************************")
            print(models.selectBook(db, bookId)['title'])
            flash("You Like {}.".format(models.selectBook(db, bookId)['title']))
        else:
            print("I am in un-like")
            models.deleteRating(db, g.user, bookId)
            flash("You don't like {}.".format(models.selectBook(db, bookId)['title']))
    return recommend_book()
