import os
import pandas as pd

def load(pathGetDataCSV):


    if (os.path.isfile(pathGetDataCSV +"QueriesTrain.csv") and
        os.path.isfile(pathGetDataCSV +"DocTrain.csv") and
        os.path.isfile(pathGetDataCSV +"QrelsTrain.csv")):

        training_queries=pd.read_csv(pathGetDataCSV +"QueriesTrain.csv")
        training_doc=pd.read_csv(pathGetDataCSV +"DocTrain.csv")
        training_qrels=pd.read_csv(pathGetDataCSV +"QrelsTrain.csv")
        return training_queries,training_doc ,training_qrels

    return None,None,None


def save(pathGetDataCSV, training_queries, training_doc, qrelsDF):

    training_queries.to_csv(pathGetDataCSV+'QueriesTrain.csv',index=False)
    training_doc.to_csv(pathGetDataCSV+'DocTrain.csv',index=False)
    qrelsDF.to_csv(pathGetDataCSV+'QrelsTrain.csv',index=False)

    return