import pandas as pd
import sqlite3
from vectorizerClass import StemmedTfidfVectorizer
from sklearn.externals import joblib
from pysparnn import cluster_index as ci


def create_query(values):
    return ",".join(str(int(x[1])) for x in values[0])


def bot_answer(question_text, count=3):
    vector = joblib.load('vector.pkl')
    knn_index = joblib.load('index_knn.pkl')

    new_question = question_text
    new_question_vector = vector.transform([new_question])

    answers_data = knn_index.search(new_question_vector, k=count, k_clusters=2, return_distance=True)
    answer_data_frame = {int(index): distance for distance, index in answers_data[0]}

    with sqlite3.connect("vk.sql") as con:
        answer_text = con.execute(
            """SELECT * FROM 'vk.sql' WHERE "index" IN ({0})""".format(create_query(answers_data)))
    answer_text_frame = {index: [question, answer] for index, question, answer in answer_text.fetchall()}

    for key, value in answer_data_frame.items():
        answer_text_frame[key].insert(0, value)
    return answer_text_frame.values()
