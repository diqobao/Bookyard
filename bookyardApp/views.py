from flask import Flask
from flask import render_template
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

viewsbp = Blueprint('views', __name__)

# Homepage
@viewsbp.route('/')
def index():
    return render_template('base.html')

@viewsbp.route('/search_book', methods=('GET', 'POST'))
def search_book():
    books = []
    if request.method == 'POST':
        letter = request.form['bookSearch']
        books = [letter, letter]
        return render_template('search_book.html', letter=letter, books=books)
    return render_template('search_book.html', letter='a', books=books)
