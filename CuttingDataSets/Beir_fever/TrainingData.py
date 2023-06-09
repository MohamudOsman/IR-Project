from collections import OrderedDict
import ir_datasets
import pandas as pd
from CuttingDataSets.Beir_fever import GetTrainingDataCSV as CSV


def reduceDataSet(training_qrels):
    res = OrderedDict(sorted(training_qrels.items(),reverse=True, key = lambda item: len(item[1])))

    resFirst = dict(list(res.items())[: 1000])
    resMid = dict(list(res.items())[11000: 12000])
    resLast = dict(list(res.items())[-1000:])

    qrels={}
    qrels.update(resFirst)
    qrels.update(resMid)
    qrels.update(resLast)

    return qrels

def getAsDict(qrels,queries,dataset_doc):
    i=0

    training_doc={}
    training_queries={}

    for qrel in qrels.items():
        training_queries[qrel[0]] = queries[qrel[0]]
        for doc in qrel[1].items():
            training_doc[doc[0]] = dataset_doc.get(doc[0]).text
        i+=1
    return training_doc,training_queries
def getAsDataFrame(qrels,queries,dataset_doc):
    i=0

    # training_doc= pd.DataFrame(columns=['doc_id','doc','title'])
    training_doc= pd.DataFrame(columns=['doc_id','doc'])
    training_queries= pd.DataFrame(columns=['query_id','query'])
    training_qrels = pd.DataFrame(columns=['query_id', 'doc_id', 'qrel'])

    for qrel in qrels.items():
        new_row={'query_id':qrel[0], 'query':queries[qrel[0]]}
        training_queries.loc[len(training_queries)]=new_row

        for doc in qrel[1].items():
            new_row = {'query_id': qrel[0],'doc_id':doc[0], 'qrel':doc[1]}
            training_qrels.loc[len(training_qrels)] = new_row

            if doc[0] not in training_doc['doc_id'].unique():
                doc=dataset_doc.get(doc[0])
                # new_row = {'doc_id':doc[0], 'doc':doc.text, 'title':doc.title}
                new_row = {'doc_id':doc[0], 'doc':doc.text}
                training_doc.loc[len(training_doc)] = new_row
        i+=1


    print('Shape=>',training_doc.shape)

    return training_queries,training_doc,training_qrels
def getTrainingData(pathGetDataCSV,dataSet):


    training_queries, training_doc, training_qrels=CSV.load(pathGetDataCSV)
    if training_queries is None or training_doc is None or training_qrels is None:
        training = ir_datasets.load(dataSet)

        print("Training: ==>")
        print("\tDocs:", training.docs_count())
        print("\tQueries:", training.queries_count())
        print("\tQrels:", training.qrels_count())

        training_qrels = training.qrels_dict()
        queries = dict(training.queries_iter())
        dataset_doc = training.docs_store()

        qrels = reduceDataSet(training_qrels)
        training_queries, training_doc, training_qrels= getAsDataFrame(qrels,queries,dataset_doc)

        CSV.save(pathGetDataCSV, training_queries, training_doc, training_qrels)

    return training_queries, training_doc,training_qrels