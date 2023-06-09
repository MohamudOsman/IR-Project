import os

import pandas as pd

from PreProcessing import Processing as P

def DataProcessing(pathGetDataCleanCSV,testing_queries, testing_doc,training_queries,training_doc):

    temp_testing_queries, temp_testing_doc,temp_training_queries,temp_training_doc=loadAll(pathGetDataCleanCSV)
    if temp_testing_queries is None or temp_testing_doc is None or temp_training_queries is None or temp_training_doc is None :

        testing_queries['cleaned'] = testing_queries['query'].apply(lambda x: P.processing(x, False))
        save(pathGetDataCleanCSV + "QueriesTest.csv", testing_queries)

        testing_doc['cleaned'] = testing_doc['doc'].apply(lambda x: P.processing(x, True))
        save(pathGetDataCleanCSV + "DocTest.csv", testing_doc)

        training_queries['cleaned'] = training_queries['query'].apply(lambda x: P.processing(x, False))
        save(pathGetDataCleanCSV + "QueriesTrain.csv", training_queries)


        training_doc['cleaned'] = training_doc['doc'].apply(lambda x: P.processing(x, True))
        save(pathGetDataCleanCSV + "DocTrain.csv", training_doc)

        # temp=training_doc[11000:len(training_doc.index)]
        # # temp=training_doc[10000:11000]
        # temp['cleaned'] = temp['doc'].apply(lambda x: P.processing(x, True))
        # save(pathGetDataCleanCSV + "DocTrain11.csv", temp)


        # saveAll(pathGetDataCleanCSV,testing_queries, testing_doc,training_queries,training_doc)

        return testing_queries, testing_doc,training_queries,training_doc

    return temp_testing_queries, temp_testing_doc,temp_training_queries,temp_training_doc


def saveAll(pathGetDataCleanCSV,testing_queries, testing_doc,training_queries,training_doc):

    save(pathGetDataCleanCSV+"QueriesTest.csv",testing_queries)
    save(pathGetDataCleanCSV+"DocTest.csv",testing_doc)

    save(pathGetDataCleanCSV+"QueriesTrain.csv",training_queries)
    save(pathGetDataCleanCSV+"DocTrain.csv",training_doc)

    return

def loadAll(pathGetDataCleanCSV):
    testing_queries = load(pathGetDataCleanCSV + "QueriesTest.csv")
    testing_doc = load(pathGetDataCleanCSV + "DocTest.csv")

    training_queries = load(pathGetDataCleanCSV + "QueriesTrain.csv")
    training_doc = load(pathGetDataCleanCSV + "DocTrain.csv")

    return testing_queries,testing_doc,training_queries,training_doc

def save(pathCSV,df):

    df.to_csv(pathCSV,index=False)

    return

def load(pathCSV):

    if os.path.isfile(pathCSV):
        df=pd.read_csv(pathCSV)
        return df

    return None



# def run():
#     pathGetDataCleanCSV = 'Files\\DataSets\\CSV\\Data Clean\\'
#
#
#     training_doc0 = load(pathGetDataCleanCSV + "DocTrain0.csv")
#     training_doc1 = load(pathGetDataCleanCSV + "DocTrain1.csv")
#     training_doc2 = load(pathGetDataCleanCSV + "DocTrain2.csv")
#     training_doc3 = load(pathGetDataCleanCSV + "DocTrain3.csv")
#     training_doc4 = load(pathGetDataCleanCSV + "DocTrain4.csv")
#     training_doc5 = load(pathGetDataCleanCSV + "DocTrain5.csv")
#     training_doc6 = load(pathGetDataCleanCSV + "DocTrain6.csv")
#     training_doc7 = load(pathGetDataCleanCSV + "DocTrain7.csv")
#     training_doc8 = load(pathGetDataCleanCSV + "DocTrain8.csv")
#     training_doc9 = load(pathGetDataCleanCSV + "DocTrain9.csv")
#     training_doc10 = load(pathGetDataCleanCSV + "DocTrain10.csv")
#     training_doc11 = load(pathGetDataCleanCSV + "DocTrain11.csv")
#
#
#     frames = [training_doc0, training_doc1,training_doc2,training_doc3,training_doc4,training_doc5,training_doc6,training_doc7,training_doc8,training_doc9,training_doc10,training_doc11]
#
#     result = pd.concat(frames)
#     save(pathDataClean+"DocTrain.csv",result)
#
#     return