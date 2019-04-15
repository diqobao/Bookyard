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

sparse_ratings = csr_matrix((df_top_books['rating'], (df_top_books['userID'], df_top_books['bookID'])),
                            shape=(maxUID + 1, maxBID + 1), dtype=np.float32)

train_sparse = sparse_ratings.copy()
test_sparse = sparse_ratings.copy()
test_sparse[test_sparse != 0] = 1


random.seed(17)

nonzero_indexs = train_sparse.nonzero()
nonzero_pairs = list(zip(nonzero_indexs[0], nonzero_indexs[1]))

num_samples = int(np.ceil(0.1 * len(nonzero_pairs)))
samples = random.sample(nonzero_pairs, num_samples)

user_indexs = [index[0] for index in samples]
artist_indexs = [index[1] for index in samples]

train_sparse[user_indexs, artist_indexs] = 0
train_sparse.eliminate_zeros()

altered_users = np.sort(list(set(user_indexs)))
dict_altered_samples = {}
for user, artist in samples:
	if user in dict_altered_samples:
		dict_altered_samples[user].append(artist)
	else:
		dict_altered_samples[user] = [artist]

train_coo = train_sparse.tocoo()
test_coo = test_sparse.tocoo()

model = LightFM(loss="warp")
model.fit(train_coo, epochs=10)

train_precision = precision_at_k(model, train_coo, k=3).mean()
test_precision = precision_at_k(model, test_coo, k=3).mean()

print("Train Precision:", train_precision)
print("Test Precision:", test_precision)

train_recall = recall_at_k(model, train_coo, k=3).mean()
test_recall = recall_at_k(model, test_coo, k=3).mean()

print("Train Recall:", train_recall)
print("Test Recall:", test_recall)

train_auc = auc_score(model, train_coo).mean()
test_auc = auc_score(model, test_coo).mean()

print("Train AUC Score:", train_auc)
print("Test AUC Score:", test_auc)


import pickle

with open("explicit_rec.pkl", "wb") as fid:
    pickle.dump(model, fid)

# def __init__(self):
	# 	with open("recsys/explicit_rec.pkl", "rb") as fid:
	# 		self.model = pickle.load(fid)









