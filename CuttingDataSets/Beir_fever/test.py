from collections import OrderedDict
import ir_datasets
import pandas as pd




# training_qrels=list(training.qrels_iter())
# dic = {c.query_id:c.doc_id for c in training.qrels_iter()}
# l=dict(sorted(dic.items(), key=lambda item: int(re.sub('\D', '', item[0]))))

# l=sorted(training.qrels_iter(), key=lambda x: int(re.sub('\D', '', x.query_id)))
# l=sorted(training.qrels_iter(), key=attrgetter('query_id'))

# training_qrels=list(training.qrels_iter())
# training_qrels = training_qrels[:1000]
# training_qrels=sorted(training_qrels)



# training_qrels = training.qrels_iter()[-10:]
# testing_qrels = testing.qrels_iter()[:1000]

# training_doc = training.docs_iter()[:1000]
# testing_doc = training.docs_iter()[:1000]
#
# training_qeury = training.queries_iter()[:1000]
# testing_qeury = testing.queries_iter()[:1000]




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

def getAsDict():
    i=0

    training_doc={}
    training_queries={}

    for qrel in qrels.items():
        # print(qrel)
        training_queries[qrel[0]]=queries[qrel[0]]
        for doc in qrel[1].items():
            training_doc[doc[0]]=dataset_doc.get(doc[0]).text
        i+=1
    return training_doc,training_queries
def getAsDataFrame(qrels,queries,dataset_doc):
    i=0

    training_doc= pd.DataFrame(columns=['doc_id','doc','title'])
    training_queries= pd.DataFrame(columns=['query_id','query'])

    for qrel in qrels.items():
        new_row={'query_id':qrel[0], 'query':queries[qrel[0]]}
        training_queries.loc[len(training_queries)]=new_row
        for doc in qrel[1].items():
            doc=dataset_doc.get(doc[0])
            new_row = {'doc_id':doc[0], 'doc':doc.text, 'title':doc.title}
            training_doc.loc[len(training_doc)] = new_row
        i+=1


    print('Shape=>',training_doc.shape)

    return training_queries,training_doc

def gettrainingData():
    training = ir_datasets.load("beir/fever/train")
    testing = ir_datasets.load("beir/fever/test")

    print("Docs:", training.docs_count())
    print("Queries:", training.queries_count())
    print("Qrels:", training.qrels_count())

    training_qrels = training.qrels_dict()
    queries = dict(training.queries_iter())
    dataset_doc = training.docs_store()

    qrels = reduceDataSet(training_qrels)
    training_queries, training_doc = getAsDataFrame(qrels,queries,dataset_doc)

    return training_queries, training_doc

training_queries, training_doc=gettrainingData()
# print("========================= qrels =========================")
i=0
# for qrel in training.qrels_iter():
#     # if(qrel.relevance!=1):
#     if(i==1000):
#         break
#     print(qrel)
#     i+=1


# i=0
# corpus={}
# for x in training_qrels:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(x)
#     training_doc = training_doc.get(x.doc_id)
#     training_qeury = training_qeury.get(x.doc_id)
#     i+=1
# i=0
# for qrel in testing_qrels:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(qrel)
#     i+=1
#
# print("========================= docs =========================")
# i=0
# for x in training_doc:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(x)
#     i+=1
# i=0
# for qrel in testing_doc:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(qrel)
#     i+=1
#
# print("========================= query =========================")
#
# i=0
# for x in training_qeury:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(x)
#     i+=1
# i=0
# for qrel in testing_qeury:
#     # if(qrel.relevance!=1):
#     if(i==10):
#         break
#     print(qrel)
#     i+=1
#


