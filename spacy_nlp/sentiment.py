# -*- coding: UTF-8 -*-


from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

import string
punctuations = string.punctuation

from spacy.en import English
parser = English()

class predictors(TransformerMixin):
    def transform(self, X, **transform_params): #args
        return [clean_text(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

def clean_text(text):
    return text.strip().lower()
def spacy_tokenizer(sentence):
    tokens = parser(sentence)
    tokens = [tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_ for tok in tokens]
    tokens = [tok for tok in tokens if (tok not in stopwords and tok not in punctuations)]
    return tokens

vectorizer = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))
classifier = LinearSVC()
pipe = Pipeline([("cleaner", predictors()),
                 ('vectorizer', vectorizer),
                 ('classifier', classifier)])

train = [('I love this sandwich.', 'pos'),
         ('this is an amazing place!', 'pos'),
         ('I feel very good about these beers.', 'pos'),
         ('this is my best work.', 'pos'),
         ("what an awesome view", 'pos'),
         ('I do not like this restaurant', 'neg'),
         ('I am tired of this stuff.', 'neg'),
         ("I can't deal with this", 'neg'),
         ('he is my sworn enemy!', 'neg'),
         ('my boss is horrible.', 'neg')]
test =   [('the beer was good.', 'pos'),
         ('I do not enjoy my job', 'neg'),
         ("I ain't feelin dandy today.", 'neg'),
         ("I feel amazing!", 'pos'),
         ('Gary is a good friend of mine.', 'pos'),
         ("I can't believe I'm doing this.", 'neg')]

pipe.fit([x[0] for x in train], [x[1] for x in train])
pred_data = pipe.predict([x[0] for x in test])
for (sample, pred) in zip(test, pred_data):
    print sample, pred
print "Accuracy:", accuracy_score([x[1] for x in test], pred_data)
