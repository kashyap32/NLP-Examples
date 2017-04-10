from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
phrases=["I am going to have a pizza   delivered for tonight","I am going to try that new French restaurant for dinner"
         ,"I prefer reading over going to the movie","I have friends in New York city","she loves going to the movies"]
vect=TfidfVectorizer(min_df=1)
tfidf=vect.fit_transform(phrases)
print tfidf
cosine=(tfidf*tfidf.T).A
print cosine
df=pd.DataFrame(cosine,index=phrases,columns=phrases)
print df.head(20)
