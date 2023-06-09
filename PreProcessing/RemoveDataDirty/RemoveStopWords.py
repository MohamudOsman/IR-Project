import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

def remove_stop_words(stringList):
    cleaned_text = []
    stop_words = set(stopwords.words('english'))
    for word in stringList:
        if word not in stop_words:
            cleaned_text.append(word)
    return cleaned_text