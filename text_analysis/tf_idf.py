'''
    Implements Term Frequency - Inverse Term Frequency
'''
import pandas as pd
import sklearn as sk
import math 
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))


def tf_idf(corpus):
    '''
        Input: corpus - list of documents
        Output: tf-idf matrix
    '''
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=1000)
    X = vectorizer.fit_transform(corpus).toarray()
    feauture_names = vectorizer.get_feature_names_out()
    return feauture_names, X

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / (float(val) + 1))
        
    return(idfDict)

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return(tfidf)

if __name__ == "__main__":
    # Get corpus from books dataset
    import os
    corpus = [file for file in os.listdir('books') if file.endswith('.txt')]
    feature_names, X = tf_idf(corpus)
    
    print(feature_names)
    print(X)

    # Print size of X
    print(X.shape)