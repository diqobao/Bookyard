import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash
#
# from bookyardApp.db import get_db

authbp = Blueprint('auth', __name__, url_prefix='/auth')

# Register Page
@authbp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # elif db.execute(
        #     'SELECT id FROM user WHERE username = ?', (username,)
        # ).fetchone() is not None:
        #     error = 'User {} is already registered.'.format(username)
        #
        if error is None:
            # db.execute(
            #     'INSERT INTO user (username, password) VALUES (?, ?)',
            #     (username, generate_password_hash(password))
            # )
            # db.commit()
            return redirect(url_for('views.index'))

        flash(error)

    return render_template('register.html')

# Login Page
@authbp.route('/login')
def login():

    return 'login'

# Logout Page
@authbp.route('/logout')
def logout():

    return 'logout'

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view