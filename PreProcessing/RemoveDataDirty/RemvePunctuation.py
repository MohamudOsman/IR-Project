import os
import re
from nltk.tokenize import word_tokenize
from nltk.stem import  WordNetLemmatizer,PorterStemmer

wnl=WordNetLemmatizer()
ps=PorterStemmer()

def removepunctuation(stringList):
    removed = []
    for word in stringList:
        op_string = re.sub(r'[^\w\s]', '', word)
        op_string = re.sub('_', '', op_string)
        # remove white spaces
        op_string = op_string.strip()
        # removing last space
        #op_string = op_string[:-1]
        removed.append(op_string)
    return removed


    #Stemmimg
def Stemming(stringList):
    sep = " "
    string1=""
    Stemmed = []
    for word in stringList:
        Stemmed.append(ps.stem(word))
    return Stemmed

    # Lemmetize
def Lemmetizing(stringList):
    Lemmetized=[]
    for word in stringList:
        Lemmetized.append(word)

    return Lemmetized







