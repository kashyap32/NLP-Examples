# -*- coding: UTF-8 -*-
# import spacy
# import random
# from spacy.gold import GoldParse
# from spacy.language import EntityRecognizer
#
# train_data = [
#     ('Who is Chaka Khan?', [(7, 17, 'PERSON')]),
#     ('I like London and Berlin.', [(7, 13, 'LOC'), (18, 24, 'LOC')]),
#     ('I want to make a website', [(16, 23, 'WEBSITE')]),
#
# ]
#
# nlp = spacy.load('en', entity=False, parser=False)
# ner = EntityRecognizer(nlp.vocab, entity_types=['PERSON', 'LOC','WEBSITE'])
#
# for itn in range(5):
#     random.shuffle(train_data)
#     for raw_text, entity_offsets in train_data:
#         doc = nlp.make_doc(raw_text)
#         gold = GoldParse(doc, entities=entity_offsets)
#
#         nlp.tagger(doc)
#         ner.update(doc, gold)
# ner.model.end_training()
# # doc = nlp.make_doc('make a website for me')
# # ner(doc)
# # for word in doc:
# #         print(word.text, word.orth, word.lower, word.tag_, word.ent_type_, word.ent_iob)
#
#
#
# #
# # import plac
# #
# # from spacy.en import English
# # from spacy.gold import GoldParse
# #
# #
# # def main(out_loc):
# #     nlp = English(parser=False) # Avoid loading the parser, for quick load times
# #     # Run the tokenizer and tagger (but not the entity recognizer)
# #     doc = nlp.tokenizer(u'Lions and tigers and grizzly bears!')
# #     nlp.tagger(doc)
# #
# #     nlp.entity.add_label('ANIMAL') # <-- New in v0.100
# #
# #     # Create a GoldParse object. This should have a better API...
# #     indices = tuple(range(len(doc)))
# #     words = [w.text for w in doc]
# #     tags = [w.tag_ for w in doc]
# #     heads = [0 for _ in doc]
# #     deps = ['' for _ in doc]
# #     # This is the only part we care about. We want BILOU format
# #     ner = ['U-ANIMAL', 'O', 'U-ANIMAL', 'O', 'B-ANIMAL', 'L-ANIMAL', 'O']
# #
# #     # Create the GoldParse
# #     annot = GoldParse(doc, (indices, words, tags, heads, deps, ner))
# #
# #     # Update the weights with the example
# #     # Here we iterate until we get it entirely correct. In practice this is probably a bad idea.
# #     # Note that we've added a class to the existing model here! We "resume"
# #     # training the previous model. Whether this is good or not I can't say, you'll have to
# #     # experiment.
# #     loss = nlp.entity.train(doc, annot)
# #     i = 0
# #     while loss != 0 and i < 1000:
# #         loss = nlp.entity.train(doc, annot)
# #         i += 1
# #     print("Used %d iterations" % i)
# #
# #     nlp.entity(doc)
# #     for ent in doc.ents:
# #         print(ent.text, ent.label_)
# #     nlp.entity.model.dump(out_loc)
# #
# # if __name__ == '__main__':
# #     plac.call(main)


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
