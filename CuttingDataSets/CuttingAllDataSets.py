from CuttingDataSets.CuttingAntique import CuttingAntique
from CuttingDataSets.CuttingBeir_fever import CuttingBeir_fever


def CuttingAllDataSets():
    # DataSetPath = "C:\\Users\\ASUS\\.ir_datasets\\antique\\collection.tsv"
    # StorPath = "D:\\IR\\DataSets\\antique\\ant_doc"
    # CuttingAntique(DataSetPath, StorPath)

    # DataSetPath = "beir/fever/testing"
    DataSetPath = "beir/fever/test"
    StorPath = "D:\\IR\\DataSets\\Beir_fever\\"
    CuttingBeir_fever(DataSetPath, StorPath)
    # queries= getAllQuery(queries_train)
    # queries= getAllQuery(queries_train)
    # training_queries=getQueryTraining(queries)
    # testing_queries=getQueryTesting(queries)
    return


def getAllQuery(queries_train):
    queries = queries_train.sample(n=2000, random_state=42).reset_index(drop=True)
    print('Shape=>', queries.shape)
    queries.head()

    return queries

def getQueryTraining(queries):
    training_queries = queries.iloc[:1000]

    print('Shape=>', training_queries.shape)
    training_queries.head()

    return training_queries

def getQueryTesting(queries):
    testing_queries = queries.iloc[1000:]
    print('Shape=>', testing_queries.shape)
    testing_queries.head()

    return testing_queries


