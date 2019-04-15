import pickle
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import coo_matrix, csr_matrix
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, recall_at_k, auc_score


df_bx_book_ratings = pd.read_csv("../data/BX-Book-Ratings.csv", delimiter=";", encoding="iso-8859-1")
df_bx_book_ratings.columns = ['userID', 'isbn', 'rating']

df_bx_books = pd.read_csv("../data/BX-Books.csv", delimiter=";",encoding="iso-8859-1", error_bad_lines=False)
df_bx_books.columns = ["isbn", "title", "author", "pubyear", "publisher", "img_s", "img_m", "img_l"]

df_bx_book_ratings = df_bx_book_ratings.merge(df_bx_books, on="isbn")
df_bx_book_ratings = df_bx_book_ratings.dropna()

book_encoder = LabelEncoder()
df_bx_book_ratings['bookID'] = book_encoder.fit_transform(df_bx_book_ratings['isbn'])

reference_book = dict(zip(df_bx_book_ratings['isbn'], df_bx_book_ratings['title']))

df_ratings = df_bx_book_ratings[['userID', "bookID", "rating"]]
df_ratings = df_ratings.query("rating > 0")

group_book_frequency = df_ratings.groupby("bookID").count()[["rating"]]
top_k_books = group_book_frequency['rating'].nlargest(2000).index.values

df_top_books = df_bx_book_ratings.loc[df_bx_book_ratings['bookID'].isin(top_k_books)]




df_ratings = pd.pivot_table(df_top_books, index="userID", columns="bookID", values="rating", fill_value=0)

maxUID = np.max(df_top_books['userID'])
maxBID = np.max(df_top_books['bookID'])

with open("../utils/explicit_rec.pkl", "rb") as fid:
	test_model = pickle.load(fid)

df_split = df_top_books[['userID', 'bookID', 'rating']]
df_split = df_split.query("userID == 243")
df_split = df_split.query("rating == 0")

user = ['234', '234']
booID = ['22987','37587']
rating = [0, 0]

df = pd.DataFrame([user, booID, rating], index=['userID', 'bookID', 'rating'])




with open("explicit_rec.pkl", "rb") as fid:
    test_model = pickle.load(fid)

usrs = [243]
bookID = [95179, 7029, 8348]
pre_result = test_model.predict(usrs, bookID)
print(bookID[np.argmax(pre_result)])



