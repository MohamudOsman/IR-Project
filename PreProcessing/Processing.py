import os
import re

from PreProcessing.RemoveDataDirty import Tokenization as tok
from PreProcessing.RemoveDataDirty import LowerCase as t
from PreProcessing.RemoveDataDirty import RemoveStopWords as rs
from PreProcessing.RemoveDataDirty import RemvePunctuation as rp
from PreProcessing.RemoveDataDirty import Spelling as sp
from PreProcessing.RemoveDataDirty import DateFormat as df

def queryProcessing(query):

    result = processing(query, False)
    return result

def CorpusProcessing(pathGetData, pathDataClean, storeTermsPath):

    vector_model=getAllFilesTerms(pathDataClean)
    if vector_model is None:
        with open(storeTermsPath, "w", encoding='utf-8') as f:
            f.close()
        vector_model = []
        i = 0
        for filename in filter(lambda p: p.endswith("txt"), os.listdir(pathGetData)):
            filepath = os.path.join(pathGetData, filename)
            with open(filepath, mode='r', encoding='utf-8') as f:
                files_content = f.readlines()
                f.close()
            # print(filepath)
            print("\n-----------------------"+filename+"--------------------------")

            result = processing(files_content[0], True)

            # with open(pathStoreDataClean + f"{i}.txt", mode='w', encoding='utf-8') as f1:
            with open(pathDataClean + f"doc"+str(i)+".txt", mode='w', encoding='utf-8') as f1:
                f1.write(str(result))
                vector_model.append(str(result))
                f1.close()
            i = i + 1

            with open(storeTermsPath, "a", encoding='utf-8') as f:
                f.writelines(str(result)+"\n")
                f.close()
        print("\n")
    return vector_model

def processing(string,Dataprocessing):
    all_terms = []

    print("Tokenization", end="")
    temptext = tok.tokenization(string)

    print(" ==> ", end="")
    print("LOWER", end="")
    temptext = t.lowerCase(temptext)

    print(" ==> ", end="")
    print("STOP WORDS", end="")
    temptext = rs.remove_stop_words(temptext)

    print(" ==> ", end="")
    print("PUNCTUATION", end="")
    temptext = rp.removepunctuation(temptext)

    if(Dataprocessing):
        print(" ==> ", end="")
        print("STEMMING", end="")
        temptext = rp.Stemming(temptext)

        print(" ==> ", end="")
        print("LEMMETIZING", end="")
        temptext = rp.Lemmetizing(temptext)

        print(" ==> ", end="")
        print("Spelling", end="")
        temptext = sp.check_spelling(temptext)



    print(" ==> ", end="")
    print("FORMATEDATE")
    temptext = df.dateFormat(temptext)

    result = re.sub(' +', ' ', temptext)

    return result


def getAllFilesTerms(pathDataClean):
    all_files_terms = []


    files = os.listdir(pathDataClean)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    if os.path.isdir(pathDataClean):
        for filename in list(files):
            if not os.path.isfile(pathDataClean+filename):
                return None
            filepath = os.path.join(pathDataClean, filename)
            with open(filepath, mode='r', encoding='utf-8') as f:
                files_content = f.readlines()
                f.close()
            all_files_terms += files_content

        if all_files_terms :
            return all_files_terms
    return None
