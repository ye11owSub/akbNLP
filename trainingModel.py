import pandas as pd
import sqlite3
from vectorizerClass import StemmedTfidfVectorizer
from sklearn.externals import joblib
from nltk.corpus import stopwords
from pysparnn import cluster_index as ci

with sqlite3.connect("vk.sql") as con:
    data = pd.read_sql("""SELECT "index","question" FROM 'vk.sql'""", con)

questions_index = data["index"]
questions_data = data["question"]
stop_words = stopwords.words("russian")
vector = StemmedTfidfVectorizer(min_df=1, stop_words=stop_words, decode_error="ignore")
vector_data = vector.fit_transform(questions_data)
knn_index = ci.MultiClusterIndex(vector_data, questions_index)

joblib.dump(vector, 'vector.pkl')
joblib.dump(knn_index, 'index_knn.pkl')
