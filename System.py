from sklearn.feature_extraction.text import TfidfVectorizer

from CuttingDataSets.Beir_fever import TestingData,TrainingData
from PreProcessing import Processing as P
from PreProcessing import DataProcessing as DP
from Indexing import invertedIndex as invert
from QueryRanking_Matching import matching_ranking as mr
from Evaluation import evaluationW2V, evaluationCore
import WordEmbedding
#----------------------------------------------------------------------------
pathGetDataCSV = 'Files\\DataSets\\CSV\\Data\\'
pathGetDataCleanCSV = 'Files\\DataSets\\CSV\\Data Clean\\'
pathGetData = 'Files\\DataSets\\Data\\'
pathDataClean = 'Files\\DataSets\\Data Clean\\'
storeTermsPath = "Files\\Result\\All Terms.txt"
pathINVERTED_INDEX = "Files\\Result\\INVERTED INDEX.pkl"
pathResult = "Files\\Result\\"

#----------------------------------------------------------------------------

def getdataSetNow():
    return dataSetNow


def getData():
    return testing_queries, testing_doc, training_queries, training_doc
def initialize():
    global dataSetNow
    # --------------------------------beir--------------------------------------
    global beir_testing_queries, beir_testing_doc, beir_testing_qrels, beir_training_queries, beir_training_doc, beir_training_qrels
    global beir_tfidf_vectorizer, beir_tfidf_matrix, beir_INVERTED_INDEX

    dataSetNow='beir'
    beir_testing_queries, beir_testing_doc, beir_testing_qrels, beir_training_queries, beir_training_doc, beir_training_qrels= CuttingDataSets(dataSetNow)

    beir_testing_queries,beir_testing_doc,beir_training_queries,beir_training_doc= DataPreprocessing(beir_testing_queries,beir_testing_doc,beir_training_queries,beir_training_doc)
    beir_tfidf_vectorizer,beir_tfidf_matrix,beir_feature_names,beir_INVERTED_INDEX= Indexing(beir_testing_doc)


    numResult = 10
    evaluationcore(beir_tfidf_vectorizer,beir_tfidf_matrix,numResult,beir_testing_queries,beir_testing_doc,beir_testing_qrels)


        #------------------------------antique-------------------------------------

    global antique_testing_queries, antique_testing_doc,antique_testing_qrels, antique_training_queries, antique_training_doc, antique_training_qrels
    global antique_tfidf_vectorizer, antique_tfidf_matrix, antique_INVERTED_INDEX

    dataSetNow = 'antique'
    antique_testing_queries, antique_testing_doc, antique_testing_qrels, antique_training_queries, antique_training_doc, antique_training_qrels= CuttingDataSets(dataSetNow)

    antique_testing_queries,antique_testing_doc,antique_training_queries,antique_training_doc= DataPreprocessing(antique_testing_queries,antique_testing_doc,antique_training_queries,antique_training_doc)
    antique_tfidf_vectorizer,antique_tfidf_matrix,antique_feature_names,antique_INVERTED_INDEX= Indexing(antique_testing_doc)

    numResult = 10
    evaluationcore(antique_tfidf_vectorizer,antique_tfidf_matrix,numResult,antique_testing_queries,antique_testing_doc,antique_testing_qrels)

    dataSetNow=None
    return

def query(queryNative,advantage):
    testing_queries, testing_doc, training_queries, training_doc = getData()
    # queryNative=(testing_queries.iloc[0])['query']

    query = QueryProcessing(queryNative)
    if advantage==1:

        w2v_model,testing_queries,testing_corpus = WordEmbedding.run(pathResult, testing_queries, testing_doc, training_queries, training_doc)

        ranking = WordEmbedding.ranking_ir(w2v_model, queryNative, testing_corpus, numResult)
        # print(result)
    else:
        matching= QueryMatching(query,tfidf_vectorizer,tfidf_matrix,INVERTED_INDEX)
        ranking=QueryRanking(matching,testing_doc)

    return ranking

def selectDataSet(datasetNew,dataSetNow,numResult):

    if dataSetNow == datasetNew:
        return True
    elif datasetNew == 'beir':
        dataSetNow = "beir/fever/"
        change('beir',numResult)
        return True
    elif datasetNew == 'antique':
        dataSetNow = "antique/"
        change('antique',numResult)
        return True
    return False

############################ Cutting All DataSets ############################
def CuttingDataSets(dataSetNow):


    dataSetTesting=dataSetNow+"/test"
    dataSetTraining=dataSetNow+"/train"
    testing_queries, testing_doc,testing_qrels=TestingData.getTestingData(pathGetDataCSV+dataSetNow+"\\",dataSetTesting)
    training_queries,training_doc,training_qrels=TrainingData.getTrainingData(pathGetDataCSV+dataSetNow+"\\",dataSetTraining)

    return testing_queries, testing_doc,testing_qrels,training_queries,training_doc,training_qrels

############################ 1-Data Preprocessing ############################
############################ 2-Data Representation ############################


def DataPreprocessing(testing_queries,testing_doc,training_queries,training_doc):

    testing_queries,testing_doc,training_queries,training_doc = DP.DataProcessing(pathGetDataCleanCSV+dataSetNow+"\\",testing_queries,testing_doc,training_queries,training_doc)


    return testing_queries,testing_doc,training_queries,training_doc

# ############################ 3-Indexing ############################
def Indexing(testing_doc):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(testing_doc['cleaned'])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    # INVERTED_INDEX={}
    INVERTED_INDEX = invert.getInvertedIndex(pathINVERTED_INDEX,tfidf_matrix, feature_names, testing_doc)

    # print(INVERTED_INDEX)
    return tfidf_vectorizer,tfidf_matrix,feature_names,INVERTED_INDEX

# ############################ 4-Query Processing ############################
def QueryProcessing(queryNative):
    print(f"Query: {queryNative}")
    query = P.queryProcessing(queryNative)

    return query

# ############################ 5-Query Matching & Ranking ############################
#
#
# ############################ Query Matching ############################
def QueryMatching(query,tfidf_vectorizer,tfidf_matrix,INVERTED_INDEX):
    matching = mr.Matching(query, tfidf_vectorizer, tfidf_matrix,INVERTED_INDEX)

    # print(f"matching={matching}")

    return matching
# ############################ Query Ranking ############################
def QueryRanking(matching,testing_doc):
    maxNumResults = 50
    ranking = mr.Ranking(matching, maxNumResults,testing_doc, pathDataClean)
    return ranking


def evaluationcore(tfidf_vectorizer,tfidf_matrix,numResult,testing_queries,testing_doc,testing_qrels):

    testing_queries=evaluationCore(tfidf_vectorizer,tfidf_matrix,pathResult,numResult,testing_queries,testing_doc,testing_qrels)
    return

# ############################ Word Embedding ############################

def wordembedding(testing_queries, testing_doc, testing_qrels, training_queries, training_doc):

    queryNative = (testing_queries.iloc[0])['query']
    print(f"\nQuery:{queryNative}")
    numResult = 50
    w2v_model, testingx_queries, testingx_corpus = WordEmbedding.run(pathResult, testing_queries, testing_doc, training_queries, training_doc)


    x = WordEmbedding.ranking_ir(w2v_model, queryNative, testingx_corpus, numResult)
    print(x)

    numResult = 50
    testing_queries = evaluationW2V(pathResult, numResult, testingx_queries, testingx_corpus, testing_qrels)
    return


def change(dataset,num):
    global testing_queries, testing_doc, testing_qrels, training_queries, training_doc, training_qrels
    global tfidf_vectorizer, tfidf_matrix, INVERTED_INDEX,numResult
    if dataset== 'beir':
        testing_queries= beir_testing_queries
        testing_doc= beir_testing_doc
        testing_qrels= beir_testing_qrels
        training_queries= beir_training_queries
        training_doc= beir_training_doc
        training_qrels= beir_training_qrels
        tfidf_vectorizer= beir_tfidf_vectorizer
        tfidf_matrix= beir_tfidf_matrix
        INVERTED_INDEX= beir_INVERTED_INDEX
    else :
        testing_queries = antique_testing_queries
        testing_doc = antique_testing_doc
        testing_qrels = antique_testing_qrels
        training_queries = antique_training_queries
        training_doc = antique_training_doc
        training_qrels = antique_training_qrels
        tfidf_vectorizer = antique_tfidf_vectorizer
        tfidf_matrix = antique_tfidf_matrix
        INVERTED_INDEX = antique_INVERTED_INDEX
    numResult=num
    return testing_queries, testing_doc, testing_qrels, training_queries, training_doc, training_qrels, tfidf_vectorizer, tfidf_matrix, INVERTED_INDEX



initialize()