import nltk 

sample="I want to create an mobile application"

sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
print tokenized_sentences
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
print tagged_sentences
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
print chunked_sentences

entity_names = []

if hasattr(chunked_sentences, 'label') and chunked_sentences.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.append(extract_entity_names(child))

print entity_names


    #entity_names.append(extract_entity_names(tree))

# Print all entity names
print entity_names

# Print unique entity names
print entity_names