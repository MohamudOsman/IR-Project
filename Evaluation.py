import os

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



# Function for calculating average precision for a query
def average_precision(qid, qvector):
    # Getting the ground truth and document vectors
    qresult = testing_result.loc[testing_result['query_id'] == qid, ['doc_id', 'qrel']]
    qcorpus = testing_corpus.loc[testing_corpus['doc_id'].isin(qresult['doc_id']), ['doc_id', 'vector']]
    qresult = pd.merge(qresult, qcorpus, on='doc_id')


    notRel=pd.DataFrame(columns=['doc_id','qrel','vector'])
    for index, row in testing_corpus.iterrows():
        if len(notRel) >= numResult:
            break
        elif row['doc_id'] not in qresult['doc_id'].values:
            new_row = {'doc_id':row['doc_id'],'qrel':0,'vector':row['vector']}
            notRel.loc[len(notRel)] = new_row
    qresult = pd.concat([qresult, notRel]).reset_index(drop=True)

    # Ranking documents for the query
    qresult['similarity'] = qresult['vector'].apply(
        lambda x: cosine_similarity(np.array(qvector).reshape(1, -1), np.array(x).reshape(1, -1)).item())
    qresult.sort_values(by='similarity', ascending=False, inplace=True)

    # IRmodelResult = pd.DataFrame(data=testing_corpus, columns=["doc_id"])
    # IRmodelResult['similarity'] = testing_corpus['vector'].apply(
    #     lambda x: cosine_similarity(np.array(qvector).reshape(1, -1), np.array(x).reshape(1, -1)).item())

    # IRmodelResult.sort_values(by='similarity', ascending=False, inplace=True)

    # Taking Top numResult documents for the evaluation

    ranking = qresult.head(numResult)['qrel'].values

    # rankingModel = IRmodelResult.head(numResult)[['doc_id']].values
    # ranking_doc = qresult.head(numResult)['doc_id'].values

    # Calculating precision
    precision = []
    for i in range(1, numResult+1):
        if i>len(ranking):
            break
        elif ranking[i - 1]:
            precision.append(np.sum(ranking[:i]) / i)

    # # Calculating precision
    # precision = []
    # i=1
    # j=0
    # for row in rankingModel:
    #     # print(row['doc_id'])
    #     if row[0] in ranking[0]:
    #         j += 1
    #         x=sum(range(0, j+1))
    #         x=float(x / float(i))
    #         precision.append(x)
    #     i+=1

    # If no relevant document in list then return 0
    if precision == []:
        return 0

    return np.mean(precision)


def evaluationW2V(pathResult,num,testing_queries, test_corpus, test_result):
    pathResult+= "evaluationW2V.csv"
    global testing_corpus
    global testing_result
    global numResult
    testing_corpus = test_corpus
    testing_result = test_result
    numResult=num

    if os.path.isfile(pathResult):
        testing_queries=pd.read_csv(pathResult)
    else:
        # Calculating average precision for all queries in the test set
        testing_queries['AP'] = testing_queries.apply(lambda x: average_precision(x['query_id'], x['vector']), axis=1)

        # Finding Mean Average Precision
        print('Mean Average Precision=>', testing_queries['AP'].mean())

        testing_queries.to_csv(pathResult, index=False)
        return testing_queries
    print('Mean Average Precision=>', testing_queries['AP'].mean())
    return testing_queries



def evaluationCore(tfidVectorizer,tfidfMatrix,  pathResult,num,testing_queries, test_corpus, test_result):
    pathResult+="evaluationCore.csv"
    global testing_corpus
    global testing_result
    global numResult
    global tfidf_vectorizer
    global tfidf_matrix
    testing_corpus = test_corpus
    testing_result = test_result
    numResult=num
    tfidf_vectorizer=tfidVectorizer
    tfidf_matrix=tfidfMatrix

    if os.path.isfile(pathResult):
        testing_queries=pd.read_csv(pathResult)
    else:
        # Calculating average precision for all queries in the test set
        testing_queries['AP'] = testing_queries.apply(lambda x: average_precisionCore(x['query_id'],x['query']), axis=1)

        # Finding Mean Average Precision
        print('Mean Average Precision=>', testing_queries['AP'].mean())

        testing_queries.to_csv(pathResult,index=False)
        return testing_queries
    print('Mean Average Precision=>', testing_queries['AP'].mean())
    return testing_queries



def average_precisionCore(qid,query):
    # Getting the ground truth and document vectors
    qresult = testing_result.loc[testing_result['query_id'] == qid, ['doc_id', 'qrel']]


    # Getting documents are not related
    notRel=pd.DataFrame(columns=['doc_id','qrel'])
    for index, row in testing_corpus.iterrows():
        if len(notRel) >= numResult:
            break
        elif row['doc_id'] not in qresult['doc_id'].values:
            new_row = {'doc_id':row['doc_id'],'qrel':0}
            notRel.loc[len(notRel)] = new_row
    qresult = pd.concat([qresult, notRel]).reset_index(drop=True)


    # Ranking documents for the query
    tfidf_matrix_test = tfidf_vectorizer.transform([query])
    similarity = cosine_similarity(tfidf_matrix_test,tfidf_matrix).flatten()

    ranked_documents = dict(enumerate(similarity, 0))

        # Assign the weight of each document to it
    qresult['similarity']= ""
    for index,row  in qresult.iterrows():
        if index in ranked_documents.keys():
            i=list(np.where(testing_corpus["doc_id"] == row['doc_id']))
            if i :
                i=i[0].tolist()
                qresult['similarity'][index]=ranked_documents[i[0]]
            else:
                qresult['similarity'][index] = 0
        else:
            qresult['similarity'][index] =0


    qresult.sort_values(by='similarity', ascending=False, inplace=True)

    # Taking Top numResult documents for the evaluation
    ranking = qresult.head(numResult)['qrel'].values

    # Calculating precision
    precision = []
    for i in range(1, numResult+1):
        if i>len(ranking):
            break
        elif ranking[i - 1]:
            precision.append(np.sum(ranking[:i]) / i)

    # If no relevant document in list then return 0
    if precision == []:
        return 0

    return np.mean(precision)