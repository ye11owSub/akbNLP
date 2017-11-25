from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("russian")


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda data: (stemmer.stem(word) for word in analyzer(data))
