import spacy
import random

nlp = spacy.load('en')

trump_text = open('text1.txt', 'r').read()
replacement_text = open('text2.txt').read()

trump_text_nlp = nlp(unicode(trump_text))
replacement_nlp = nlp(unicode(replacement_text))


replacement_vb = []
replacement_vbd = []
replacement_vbg = []
replacement_vbn = []
replacement_vbp = []
replacement_vbz = []
#nouns
replacement_nn = []
replacement_nnp = []
replacement_nnps = []
replacement_nns = []
#adjectives
replacement_adj = []
replacement_det = []
replacement_intj = []

for replacement_word in replacement_nlp:
	if replacement_word.tag_ == "VB": ##VERB
		replacement_vb.append(replacement_word.text)
	elif replacement_word.tag_ == "VBD":
		replacement_vbd.append(replacement_word.text)
	elif replacement_word.tag_ == "VBG":
		replacement_vbg.append(replacement_word.text)
	elif replacement_word.tag_ == "VBN":
		replacement_vbn.append(replacement_word.text)
	elif replacement_word.tag_ == "NN":
	 	replacement_nn.append(replacement_word.text)
	elif replacement_word.tag_ == "NNS":
	 	replacement_nns.append(replacement_word.text)
	elif replacement_word.pos_ == "ADJ":  ##adjective
	 	replacement_adj.append(replacement_word.text)
	elif replacement_word.pos_ == "DET":  ##determiner
	 	replacement_det.append(replacement_word.text)
	elif replacement_word.pos_ == "INTJ":   ## maybe interjection
		replacement_intj.append(replacement_word.text)
	pass

trump_new_speech = "" ##SORRy

for word in trump_text_nlp:
	if word.tag_ == "VB":
		trump_new_speech += (random.choice(replacement_vb) + " ")
	elif word.tag_ == "VBD":
		trump_new_speech += (random.choice(replacement_vbd) + " ")
	elif word.tag_ == "VBG":
		trump_new_speech += (random.choice(replacement_vbg) + " ")
	elif word.tag_ == "VBN":
		trump_new_speech += (random.choice(replacement_vbn) + " ")
	elif word.tag_ == "NN":
		trump_new_speech += (random.choice(replacement_nn) + " ")
	elif word.tag_ == "NNS":
		trump_new_speech += (random.choice(replacement_nns) + " ")
	elif word.pos_ == "ADJ":
		trump_new_speech += (random.choice(replacement_adj) + " ")
	elif word.pos_ == "DET":
		trump_new_speech += (random.choice(replacement_det) + " ")
	elif word.pos_ == "INTJ":
		trump_new_speech += (random.choice(replacement_intj) + " ")
	else:
		trump_new_speech += (word.text + " ")

trump_new_speech = trump_new_speech.replace(" , ", ", ")
trump_new_speech = trump_new_speech.replace(" . ", ". ")
trump_new_speech = trump_new_speech.replace(" ; ", "; ")
trump_new_speech = trump_new_speech.replace(" : ", ": ")
print trump_new_speech

replacement_text_saved = open("Generated.txt", "w")
replacement_text_saved.write(trump_new_speech)
replacement_text_saved.close()
