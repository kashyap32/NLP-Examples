import spacy
import requests
url=requests.get('https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2017/04/04080929/Tripadvisor_hotelreviews_Shivambansal.txt').content
nlp=spacy.load('en')
document = url.decode('utf8')
document = nlp(document)


for word in list(document.sents)[0]:

    print word, word.tag_
noisy_pos_tags = ["PROP"]
min_token_length = 2

def isNoise(token):
    is_noise = False
    if token.pos_ in noisy_pos_tags:
        is_noise = True
    elif token.is_stop == True:
        is_noise = True
    elif len(token.string) <= min_token_length:
        is_noise = True
    return is_noise
def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()
from collections import Counter
cleaned_list = [cleanup(word.string) for word in document if not isNoise(word)]
print Counter(cleaned_list) .most_common(5)
