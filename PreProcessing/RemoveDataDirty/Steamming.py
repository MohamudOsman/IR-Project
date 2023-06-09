from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import os

ps = PorterStemmer()

def steamming(path):
    for filename in filter(lambda p: p.endswith("text"), os.listdir(path)):
        files_content = ""
        doc_id=""
        filepath = os.path.join(path, filename)
        with open(filepath, mode='r') as f:
            files_content = f.readlines()
            f.close()
        with open(filepath, mode='w') as f1:
            #with open("C:\\Users\\lamak\\Desktop\\CURBUS1\\Steamming\\steaming" + filename , 'w') as f1:
            f1.seek(0)
            f1.truncate()
            words = word_tokenize(files_content[0])
            for word in words:
                  #  print(word, " : ", ps.stem(word))
                  f1.write(ps.stem(word))
            f1.close()
    return