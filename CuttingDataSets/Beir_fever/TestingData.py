from collections import OrderedDict
import ir_datasets
import pandas as pd
from CuttingDataSets.Beir_fever import GetTestingDataCSV as CSV
def reduceDataSet(testing_qrels):
    res = OrderedDict(sorted(testing_qrels.items(),reverse=True, key = lambda item: len(item[1])))

    resFirst = dict(list(res.items())[: 1000])
    resMid = dict(list(res.items())[3000: 4000])
    resLast = dict(list(res.items())[-1000:])

    qrels={}
    qrels.update(resFirst)
    qrels.update(resMid)
    qrels.update(resLast)

    return qrels

def getAsDict(qrels,queries,dataset_doc):
    i=0

    testing_doc={}
    testing_queries={}

    for qrel in qrels.items():
        testing_queries[qrel[0]] = queries[qrel[0]]
        for doc in qrel[1].items():
            testing_doc[doc[0]] = dataset_doc.get(doc[0]).text
        i+=1
    return testing_doc,testing_queries
def getAsDataFrame(qrels,queries,dataset_doc):
    i=0

    # testing_doc= pd.DataFrame(columns=['doc_id','doc','title'])
    testing_doc= pd.DataFrame(columns=['doc_id','doc'])
    testing_queries= pd.DataFrame(columns=['query_id','query'])
    testing_qrels= pd.DataFrame(columns=['query_id','doc_id','qrel'])

    for qrel in qrels.items():
        new_row={'query_id':qrel[0], 'query':queries[qrel[0]]}
        testing_queries.loc[len(testing_queries)]=new_row

        for doc in qrel[1].items():
            new_row = {'query_id': qrel[0],'doc_id':doc[0], 'qrel':doc[1]}
            testing_qrels.loc[len(testing_qrels)] = new_row

            if doc[0] not in testing_doc['doc_id'].unique():
                doc=dataset_doc.get(doc[0])
                # new_row = {'doc_id':doc[0], 'doc':doc.text, 'title':doc.title}
                new_row = {'doc_id':doc[0], 'doc':doc.text}
                testing_doc.loc[len(testing_doc)] = new_row
        i+=1


    print('Shape=>',testing_doc.shape)

    return testing_queries,testing_doc,testing_qrels
def getTestingData(pathGetDataCSV,dataSet):

    testing_queries, testing_doc ,testing_qrels=CSV.load(pathGetDataCSV)
    if testing_queries is None or testing_doc is None or testing_qrels is None:
        testing = ir_datasets.load(dataSet)

        print("Testing: ==>")
        print("\tDocs:", testing.docs_count())
        print("\tQueries:", testing.queries_count())
        print("\tQrels:", testing.qrels_count())

        testing_qrels = testing.qrels_dict()
        queries = dict(testing.queries_iter())
        dataset_doc = testing.docs_store()

        qrels = reduceDataSet(testing_qrels)
        testing_queries, testing_doc, testing_qrels = getAsDataFrame(qrels, queries, dataset_doc)


        CSV.save(pathGetDataCSV,testing_queries, testing_doc,testing_qrels)


    return testing_queries, testing_doc,testing_qrels