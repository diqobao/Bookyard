DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS rating;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE book (
  bookId INTEGER PRIMARY KEY AUTOINCREMENT,
  isbn TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  author TEXT,
  year_of_pub INTEGER,
  publisher TEXT,
  img_url_s TEXT,
  img_url_m TEXT,
  img_url_l TEXT
);

CREATE TABLE rating (
  userid INTEGER,
  bookId INTEGER,
  rating INTEGER
);

INSERT INTO rating values(1, 1, 6);
INSERT INTO rating values(1, 2, 5);