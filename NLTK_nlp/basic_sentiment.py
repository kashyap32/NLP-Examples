import nltk
import csv
import numpy as np 
negative=[]
with open("negetive.csv","rb") as file:
	reader=csv.reader(file)
	for row in reader:
		negative.append(row)
positive=[]
with open("positive.csv","rb") as file:
	reader=csv.reader(file)
	for row in reader:
		positive.append(row)
#print positive[:10]

def sentiment(text):
	temp=[]
	text_sent=nltk.sent_tokenize(text)
	for sentence in text_sent:
		n_count=0
		p_count=0
		sent_words=nltk.word_tokenize(sentence)
		for word in sent_words:
			for item in positive:
				if(word==item[0]):
					p_count+=1
			for item in negative:
				if (word==item[0]):
					n_count+=1
					temp.append(-1)
		if (p_count>0 and n_count==0):
			temp.append(1)

			print "+ : " +sentence
		elif n_count%2>0:
			temp.append(-1)

			print "- : " +sentence
		elif n_count%2==0 and n_count>0:
			temp.append(-1)

			print "+ : " +sentence
		else:
			temp.append(0)

			print "----"+sentence
	return temp
sentiment("It was not that good!")
sentiment("HI how are you")
sentiment("La la land is worst")
sentiment("I am good")

comments=[]
with open("movie-pang02.csv",'rb') as file:
	reader=csv.reader(file)
	for row in reader:
		comments.append(row)
print comments[0]
for review in comments:
	print "\n"
	print np.average(sentiment(str(review)))
	print review
