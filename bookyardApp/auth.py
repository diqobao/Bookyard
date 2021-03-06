import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bookyardApp.db import get_db
import bookyardApp.models as models

authbp = Blueprint('auth', __name__, url_prefix='/auth')

# Register Page
@authbp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif models.selectUser(username, db) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            models.addUser(username, generate_password_hash(password), db)
            session.clear()
            session['user_id'] = models.selectUser(username, db)['id']
            return redirect(url_for('views.index'))

        flash(error)

    return render_template('register.html')

# Login Page
@authbp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = models.selectUser(username, db)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('views.index'))

        flash(error)

    return render_template('login.html')

# Logout Page
@authbp.route('/logout')
def logout():
    g.user = None
    session.clear()
    return redirect(url_for('views.index'))

@authbp.route('/save_preference')
def save_preference():
    return '..'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@authbp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id
