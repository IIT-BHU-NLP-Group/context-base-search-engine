"""Tokenizer and verb analyzer software"""
import nltk
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
from nltk.stem import SnowballStemmer
verbTags = ['VBD','VBG','VBN','VB','VBP','VBZ']
freqDict = {}
import codecs
text = ""

cities =['Varanasi' , 'Kanpur', 'Goa', 'Nainital', 'Mathura', 'New York', 'Tokyo', 'Darjiling', 'Manali', 'Kullu', 'Ujjain', 'Mumbai', 'Amritsar', 'ooty']
cities += ['London', 'Barcelona', 'Paris', 'Vatican city', 'Agra', 'Jaipur', 'Banglore', 'Gangtok']
files = ['1'+city+'.txt' for city in cities]

for i in files:
    f = codecs.open(i, 'r', 'utf-8-sig')
    text += f.read()
    f.close()

sent_tokenize_list = sent_tokenize(text)
stemmer = SnowballStemmer("english")
for x in sent_tokenize_list:
    text = nltk.word_tokenize(x)
    tagged = nltk.pos_tag(text)
    for i in  range(len(tagged)):
        x = tagged[i]
        if ((i+1)<len(tagged)):
            nex = tagged[i+1]
        else:
            nex = ("","NP")   
        if (x[1] in verbTags) and (nex[1] not in verbTags):
            root = stemmer.stem(x[0])
            #print root,x[1],x[0]
            if root in freqDict:
                freqDict[root] += 1
            else:
                freqDict[root] = 1

tup = freqDict.items()
#print tup
def comps(info1):
    return info1[1]
result = codecs.open("result_new.csv","w",'utf-8-sig')
tup = sorted(tup,key = comps,reverse = True)
for x in tup:
    print x
    result.write(x[0] +","+unicode(x[1])+"\n")
result.close()
