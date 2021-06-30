from apriori_python import apriori
import random
#Mod refers to a list of the mods chosen so far

def apr(dataSet,mod):
    freqItemSet, rules = apriori(dataSet, minSup=0, minConf=0)
    inter = []
    for i in rules:
        if (i[0] == set(mod)):
            inter.append(i)
    inter = sorted(inter, key = lambda i: i[-1], reverse = True)
    output = []
    for i in inter:
        if (len(i[1])==1):
            output.append(list(i[1])[0])
    return output

def ranList(length):
    output = []
    for i in range(0,length):
        output.append(random.randint(0,3569))
    return output