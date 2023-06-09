import pandas


def CuttingAntique(DataSetPath,StorPath):

    # antique = ir_datasets.load("antique/testing")

    # file = pandas.read_csv("C:\\Users\\lamak\\.ir_datasets\\antique\\collection.tsv",sep="\t")
    file = pandas.read_csv(DataSetPath, sep="\t")

    print(file)

    #Cutting Data Sets

    # csvfile = open("C:\\Users\\lamak\\.ir_datasets\\antique\\collection.tsv", mode='r', encoding='utf-8')
    csvfile = open(DataSetPath, mode='r', encoding='utf-8')
    # or 'Latin-1' or 'CP-1252'
    i=0
    for rownum, line in enumerate(csvfile):
        # with open("D:\\DataSets\\antique\\ant_doc"+str(i)+".txt","w",encoding='utf-8') as c1:
        with open(StorPath+str(i)+".txt","w",encoding='utf-8') as c1:
         c1.writelines(line)
        print(str(i)+"Finish Cutting in antique")
        i = i+1
    print("Finish Cutting Antique")
    return


