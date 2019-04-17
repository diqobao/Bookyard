import os, sys, csv, sqlite3, click
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('iso-8859-1'))
    reader = csv.reader(open('BX-Books.csv', 'r', encoding='iso-8859-1'),delimiter='\n')
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        row1 = row[0].split(';"')
        to_db = [row1[0], row1[1][0:-1], row1[2][0:-1], row1[3][0:-1], row1[4][0:-1], row1[5][0:-1], row1[6][0:-1], row1[7][0:-1]]
        db.execute('INSERT INTO book (isbn,title,author,year_of_pub,publisher,img_url_s,img_url_m,img_url_l) VALUES (?, ?, ?,?,?,?,?,?);',to_db)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
