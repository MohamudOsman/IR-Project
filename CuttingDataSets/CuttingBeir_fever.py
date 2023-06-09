import ir_datasets
import pandas as pd

def CuttingBeir_fever(DataSetPath,StorPath):

    # fever = ir_datasets.load("beir/fever/testing")
    fever = ir_datasets.load(DataSetPath)

    #Cutting Data Sets
    corpus = pd.DataFrame({},columns=['doc_id', 'text','title'])

    # fever.columns = ['doc_id', 'text','title']
    i=0
    for doc in fever.docs_iter():
        if(i==5000):
            break
        # queries_train = queries_train.append(doc, ignore_index=True)
        corpus.loc[len(corpus.index)] = doc
        # with open("D:\\DataSets\\"+doc[0]+".txt","w",encoding='utf-8') as c:
        with open(StorPath+f"doc{i}.txt","w",encoding='utf-8') as c:
            c.writelines(doc[0])
            c.writelines(doc[1])
            c.writelines(doc[2])
            c.close()
            print(f"Next doc{i+1}...")
            i +=1

    print("Finish Cutting Beir/fever")
    print(corpus.head())

    queries_train = pd.DataFrame({}, columns=['query_id', 'text'])
    i=0
    for query in fever.queries_iter():
        if (i == 1000):
            break
        queries_train.loc[len(queries_train.index)] = query
        i+=1


    queries_test = pd.DataFrame({}, columns=['query_id', 'text'])
    i=0
    for query in fever.qrels_iter():
        if (i == 1000):
            break
        queries_test.loc[len(queries_test.index)] = query
        i+=1


    return corpus,queries_train,queries_test


    # def CuttingBeir_fever(DataSetPath,StorPath):
    #
    #
    # queries_train = pd.read_table('msmarco-doctrain-queries.tsv', header=None)
    # queries_train.columns = ['qid', 'query']
    # print('Shape=>', queries_train.shape)
    # print(queries_train.head())
    #
    #
    # # fever = ir_datasets.load("beir/fever/testing")
    # fever = ir_datasets.load(DataSetPath)
    #
    # queries = queries_train.sample(n=2000, random_state=42).reset_index(drop=True)
    # print('Shape=>', queries.shape)
    # queries.head()
    #
    # #Cutting Data Sets
    # i=0
    # for doc in fever.docs_iter():
    #     # with open("D:\\DataSets\\"+doc[0]+".txt","w",encoding='utf-8') as c:
    #     with open(StorPath+doc[0]+".txt","w",encoding='utf-8') as c:
    #         c.writelines(doc[1])
    #         c.writelines(doc[2])
    #         print(str(i)+"Finish Cutting fever")
    #         i = i+1
    # print("Finish Cutting Beir/fever")
    # return