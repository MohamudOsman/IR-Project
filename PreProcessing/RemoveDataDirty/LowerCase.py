import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

import os

def lowerCase(SentenceList):
    lowerd=[]
    for word in SentenceList:
        lowerd.append(word.lower())
    return lowerd



