DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE book (
  isbn TEXT PRIMARY KEY,
  title TEXT UNIQUE NOT NULL,
  author TEXT,
  year_of_pub INTEGER,
  publisher TEXT,
  img_url_s TEXT,
  img_url_m TEXT,
  img_url_l TEXT
);

INSERT INTO book VALUES ('0195153448','Classical Mythology','Mark P. O. Morford',2002,'Oxford University Press','http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg','http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg','http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg');
INSERT INTO book VALUES ('0002005018','Clara Callan','Richard Bruce Wright',2001,'HarperFlamingo Canada','http://images.amazon.com/images/P/0002005018.01.THUMBZZZ.jpg','http://images.amazon.com/images/P/0002005018.01.MZZZZZZZ.jpg','http://images.amazon.com/images/P/0002005018.01.LZZZZZZZ.jpg');
INSERT INTO book VALUES ('0060973129','Decision in Normandy','Carlo D''Este',1991,'HarperPerennial','http://images.amazon.com/images/P/0060973129.01.THUMBZZZ.jpg','http://images.amazon.com/images/P/0060973129.01.MZZZZZZZ.jpg','http://images.amazon.com/images/P/0060973129.01.LZZZZZZZ.jpg');
INSERT INTO book VALUES ('0374157065','Flu: The Story of the Great Influenza Pandemic of 1918 and the Search for the Virus That Caused It','Gina Bari Kolata',1999,'Farrar Straus Giroux','http://images.amazon.com/images/P/0374157065.01.THUMBZZZ.jpg','http://images.amazon.com/images/P/0374157065.01.MZZZZZZZ.jpg','http://images.amazon.com/images/P/0374157065.01.LZZZZZZZ.jpg');
