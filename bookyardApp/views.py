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
    return render_template('base.html')

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
    books = []
    rated_books = []
    # if request.method == 'POST':
    #     prefix = request.form['bookSearch']
    #     db = get_db()
    #     books = models.searchBook(prefix, db)
    #     return render_template('search_book.html', letter=prefix, books=books, liked_bookId=[])
    user_id = session.get('user_id')
    op = models.Operation(get_db())
    op.recommend(user_id)
    return render_template('recommend.html', books=books, rated_books=rated_books)
