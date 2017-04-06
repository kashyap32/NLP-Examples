import spacy
import requests
url=requests.get('https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2017/04/04080929/Tripadvisor_hotelreviews_Shivambansal.txt').content
# print url
nlp=spacy.load('en')
document = url.decode('utf8')
document = nlp(document)
#print document.ents ## freaking awesome!! can even detect thanksgiving as date!!
labels = set([w.label_ for w in document.ents])
def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()
for label in labels:
    entities = [cleanup(e.string, lower=False) for e in document.ents if label==e.label_]
    entities = list(set(entities))
    # print label,entities


###### Depenedancy Parsing!! ##########
hotel = [sent for sent in document.sents if 'hotel' in sent.string.lower()]
sentence = hotel[2]
print sentence

sentence = hotel[2]
for word in sentence:
    # tree
    print word, ': ', str(list(word.children))


# Generate Noun Phrases ######

doc = nlp(u'Well, I am kind of falling love in spacy!!')
for no in doc.noun_chunks:
    print no
for np in doc.noun_chunks:
    print np.root.dep_
    print np.root.head.text





def iter_products(docs):
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ == 'PRODUCT':
                yield ent ## Trying out generator

def word_is_in_entity(word):
    return word.ent_type != 0

def count_parent_verb_by_person(docs):
    counts = defaultdict(defaultdict(int))
    for doc in docs:
        for ent in doc.ents:
            if ent.label_ == 'PERSON' and ent.root.head.pos == VERB:
                counts[ent.orth_][ent.root.head.lemma_] += 1
    return counts
