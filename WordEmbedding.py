from ast import literal_eval
from os import path

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

from PreProcessing.DataProcessing import save
from PreProcessing.Processing import queryProcessing



def run(pathModel,testing_queries,testing_corpus,training_queries,training_corpus):

    pathModel+="w2v_model.model"

    if path.exists(pathModel):
        w2v_model=Word2Vec.load(pathModel)
    else:
        # Combining corpus and queries for training
        combined_training = pd.concat([training_corpus.rename(columns={'cleaned': 'text'})['text'],
                                       training_queries.rename(columns={'cleaned': 'text'})['text']]) \
                                        .sample(frac=1).reset_index(drop=True)

        # Creating data for the model training
        train_data = []
        for i in combined_training:
            train_data.append(i.split())

        # Training a word2vec model from the given data set
        w2v_model = Word2Vec(train_data, vector_size=300, min_count=2, window=5, sg=1, workers=4)
        w2v_model.save(pathModel)

    # print('Vocabulary size:', len(w2v_model.wv))

    # Getting Word2Vec Vectors for Testing Corpus and Queries
    testing_corpus['vector'] = testing_corpus['cleaned'].apply(lambda x: get_embedding_w2v(w2v_model, x.split()))
    testing_queries['vector'] = testing_queries['cleaned'].apply(lambda x: get_embedding_w2v(w2v_model, x.split()))




    return w2v_model,testing_queries, testing_corpus



# Function returning vector reperesentation of a document
def get_embedding_w2v(w2v_model,doc_tokens):
    embeddings = []
    if len(doc_tokens)<1:
        return np.zeros(300)
    else:
        for tok in doc_tokens:
            if tok in w2v_model.wv.key_to_index:
                embeddings.append(w2v_model.wv.word_vec(tok))
            else:
                embeddings.append(np.random.rand(300))
        # mean the vectors of individual words to get the vector of the document
        return np.mean(embeddings, axis=0)


def ranking_ir(w2v_model,queryNative,testing_corpus,numResult):

        # pre-process Query
    query = queryProcessing(queryNative)
    # query = query.lower()
    # query = expand_contractions(query)
    # query = clean_text(query)
    # query = re.sub(' +', ' ', query)

    # generating vector
    vector = get_embedding_w2v(w2v_model,query.split())

    # ranking documents
    documents = testing_corpus[['doc_id', 'doc', 'title']].copy()
    documents['similarity'] = testing_corpus['vector'].apply(
        lambda x: cosine_similarity(np.array(vector).reshape(1, -1), np.array(x).reshape(1, -1)).item())
    documents.sort_values(by='similarity', ascending=False, inplace=True)

    return documents.head(numResult).reset_index(drop=True)