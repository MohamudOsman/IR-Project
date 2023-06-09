import os
import pandas as pd

def load(pathGetDataCSV):


    if (os.path.isfile(pathGetDataCSV +"QueriesTest.csv") and
        os.path.isfile(pathGetDataCSV +"DocTest.csv") and
        os.path.isfile(pathGetDataCSV + "QrelsTest.csv")):

        testing_queries=pd.read_csv(pathGetDataCSV +"QueriesTest.csv")
        testing_doc=pd.read_csv(pathGetDataCSV +"DocTest.csv")
        testing_qrels=pd.read_csv(pathGetDataCSV +"QrelsTest.csv")
        return testing_queries,testing_doc,testing_qrels

    return None,None,None


def save(pathGetDataCSV,testing_queries, testing_doc,qrelsDF):

    testing_queries.to_csv(pathGetDataCSV+'QueriesTest.csv',index=False)
    testing_doc.to_csv(pathGetDataCSV+'DocTest.csv',index=False)
    qrelsDF.to_csv(pathGetDataCSV+'QrelsTest.csv',index=False)

    return