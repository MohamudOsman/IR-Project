import os
import pickle

import pandas as pd



def build_inverted_index(terms):
    inverted_index = {}
    for term_id, term in enumerate(terms):
        for doc_id in term:
            if doc_id not in inverted_index:
                inverted_index[doc_id] = []
            if term_id not in inverted_index[doc_id]:
                inverted_index[doc_id].append(term_id)
    return inverted_index

# def getInvertedIndex(pathINVERTED_INDEX,tfidf_matrix, feature_names, all_files_terms):
#
#     if os.path.isfile(pathINVERTED_INDEX):
#         terms_dict=load(pathINVERTED_INDEX)
#     else :
#         terms_dict = {}
#         keys = []
#         for i in range(len(all_files_terms)):
#             # Get the document ID
#             doc_id = f"doc{i + 1}"
#             keys.append(doc_id)
#             # Get the terms in the document
#             terms = tfidf_matrix[i].nonzero()[1]
#
#             # Store the tf-idf scores in a dictionary with the term as the key and a list of tuples containing the document ID and tf-idf score as the value.
#             for term in terms:
#                 if feature_names[term] not in terms_dict:
#                     terms_dict[feature_names[term]] = []
#                 # terms_dict[feature_names[term]].append(("doc"+str(doc_id), tfidf_matrix[i, term]))
#                 terms_dict[feature_names[term]].append(doc_id)
#
#
#         # df = pd.DataFrame(tfidf_matrix.toarray(), columns=INVERTED_INDEX.values()[0], index=INVERTED_INDEX.keys())
#         save(pathINVERTED_INDEX,terms_dict)
#     return terms_dict,keys


def getInvertedIndex(pathINVERTED_INDEX,tfidf_matrix, feature_names, corpus):

    if os.path.isfile(pathINVERTED_INDEX):
        # INVERTED_INDEX=load(pathINVERTED_INDEX)
        INVERTED_INDEX= {}
    else :

        # keys = []
        # for i in range(len(corpus['cleaned'])):
        #     # Get the document ID
        #     doc_id = f"doc{i + 1}"
        #     keys.append(doc_id)

        INVERTED_INDEX = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=corpus['doc_id'])
        # INVERTED_INDEX = dict(INVERTED_INDEX)
        # d=INVERTED_INDEX.apply(lambda x: x[(x != 0) & (x.keys() != x.name)].to_dict())
        # d = INVERTED_INDEX.where(INVERTED_INDEX.astype(bool), 0).to_dict(orient='index')
        INVERTED_INDEX = INVERTED_INDEX.to_dict()
        # save(pathINVERTED_INDEX,INVERTED_INDEX)
    return INVERTED_INDEX


def save(pathINVERTED_INDEX,INVERTED_INDEX):

    with open(pathINVERTED_INDEX, 'wb') as fp:
        pickle.dump(INVERTED_INDEX, fp)


    return

def load(pathINVERTED_INDEX):

    with open(pathINVERTED_INDEX, 'rb') as fp:
        INVERTED_INDEX = pickle.load(fp)

    return INVERTED_INDEX