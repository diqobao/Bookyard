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

@viewsbp.route('/search_book', methods=('GET', 'POST'))
def search_book():
    books = []
    liked_bookId = []
    if request.method == 'POST':
        prefix = request.form['bookSearch']
        db = get_db()
        books = models.searchBook(prefix, db)
        return render_template('search_book.html', letter=prefix, books=books, liked_bookId=liked_bookId)
    return render_template('search_book.html', letter='a', books=books, liked_bookId=liked_bookId)


@viewsbp.route('/recommend_book', methods=('GET', 'POST'))
def recommend_book():
    books = []
    liked_bookId = []
    # if request.method == 'POST':
    #     prefix = request.form['bookSearch']
    #     db = get_db()
    #     books = models.searchBook(prefix, db)
    #     return render_template('search_book.html', letter=prefix, books=books, liked_bookId=[])
    user_id = session.get('user_id')
    op = models.Operation(get_db())
    op.recommend(user_id)
    return render_template('recommend.html', books=books, liked_bookId=liked_bookId)
