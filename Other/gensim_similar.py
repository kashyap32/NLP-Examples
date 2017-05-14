import logging, sys, pprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from gensim.corpora import TextCorpus, MmCorpus, Dictionary

background_corpus = TextCorpus(input=YOUR_CORPUS)

background_corpus.dictionary.save(
    "my_dict.dict")

MmCorpus.serialize("background_corpus.mm",
    background_corpus) 

from gensim.corpora import WikiCorpus, wikicorpus

articles = "enwiki-latest-pages-articles.xml.bz2" 

wiki_corpus = WikiCorpus(articles)
wiki_corpus.dictionary.save("wiki_dict.dict")

MmCorpus.serialize("wiki_corpus.mm", wiki_corpus) 

bow_corpus = MmCorpus("wiki_corpus.mm") 

dictionary = Dictionary.load("wiki_dict.dict")  

from gensim.models import LsiModel, LogEntropyModel

logent_transformation = LogEntropyModel(wiki_corpus,
    id2word=dictionary) 

tokenize_func = wikicorpus.tokenize  
document = "Some text to be transformed."

bow_document = dictionary.doc2bow(tokenize_func(
    document))
logent_document = logent_transformation[[
    bow_document]]

documents = ["Some iterable", "containing multiple", "documents", "..."]
bow_documents = (dictionary.doc2bow(
    tokenize_func(document)) for document in documents) 
logent_documents = logent_transformation[
                   bow_documents] 
logent_corpus = MmCorpus(corpus=logent_transformation[bow_corpus])

lsi_transformation = LsiModel(corpus=logent_corpus, id2word=dictionary,
    num_features=400)



logent_transformation.save("logent.model")
lsi_transformation.save("lsi.model")

from gensim.similarities import Similarity

index_documents = ["A bear walked in the dark forest.",
             "Tall trees have many more leaves than short bushes.",
             "A starship may someday travel across vast reaches of space to other stars.",
             "Difference is the concept of how two or more entities are not the same."]
corpus = (dictionary.doc2bow(tokenize_func(document)) for document in index_documents)

index = Similarity(corpus=lsi_transformation[logent_transformation[corpus]], num_features=400, output_prefix="shard")

print "Index corpus:"
pprint.pprint(documents)

print "Similarities of index corpus documents to one another:"
pprint.pprint([s for s in index])

query = "In the face of ambiguity, refuse the temptation to guess."
sims_to_query = index[lsi_transformation[logent_transformation[dictionary.doc2bow(tokenize_func(query))]]]
print "Similarities of index corpus documents to '%s'" % query
pprint.pprint(sims_to_query)

best_score = max(sims_to_query)
index = sims_to_query.tolist().index(best_score)
most_similar_doc = documents[index]
print "The document most similar to the query is '%s' with a score of %.2f." % (most_similar_doc, best_score)
