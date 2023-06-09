import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def Matching(query,tfidf_vectorizer,tfidf_matrix,INVERTED_INDEX):

    tfidf_matrix_test = tfidf_vectorizer.transform([query])
    cos = cosine_similarity(tfidf_matrix_test,tfidf_matrix).flatten()


    return cos



def Ranking(cosine_similarities,maxNumResults,testing_doc, pathDataClean):
    ranked_documents = dict(enumerate(cosine_similarities, 0))

    sorted_dict = dict(sorted(ranked_documents.items(), key=lambda item: item[1], reverse=True))
    print(f"ranked_documents:{ranked_documents}")
    print(f"length is:{len(sorted_dict)}")
    print(f"sorted_dict:{sorted_dict}")


    j = 0
    result1=pd.DataFrame(columns=['doc_id','doc'])
    for i in sorted_dict.items():
        if(j>maxNumResults or i[1] <=float(0.0)):
            break
        doc_id = (testing_doc.iloc[i[0]])['doc_id']
        doc = (testing_doc.iloc[i[0]])['doc']
        newRow={'doc_id':doc_id,'doc':doc}
        result1.loc[len(result1)]=newRow
        j+=1

    return result1