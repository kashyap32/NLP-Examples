import spacy
import requests
url=requests.get('https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2017/04/04080929/Tripadvisor_hotelreviews_Shivambansal.txt').content
# print url
nlp=spacy.load('en')
document = url.decode('utf8')
document = nlp(document)
# print dir(document)
#print document[0]
print list(document.sents)[0]

for word in list(document.sents)[0]:
    print word, word.tag_
