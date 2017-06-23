"""Tokenizer and verb analyzer software"""
import nltk
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
# from nltk.stem import SnowballStemmer
verbTags = ['VBD','VBG','VBN','VB','VBP','VBZ']
freqDict = {}
#sentDict = {}
import codecs
text = ""

cities = [ 'Agra', 'Jaipur', 'Banglore', 'Gangtok','Varanasi','Kanpur', 'Goa', 'Nainital', 'Mathura', 'Darjiling', 'Manali', 'Kullu', 'Ujjain', 'Mumbai', 'Amritsar', 'Ooty','Kolkata', 'Hyderabad','Delhi', 'Guwahati','New_Delhi']

files = ['wiki-'+city+'.txt' for city in cities]

for i in files:
    f = codecs.open(i, 'r', 'utf-8-sig')
    text += f.read()
    f.close()

sent_tokenize_list = sent_tokenize(text)
lemmatizer = WordNetLemmatizer()#stemmer = SnowballStemmer("english")
for y in sent_tokenize_list:
    # print y
    x = y
    text = nltk.word_tokenize(x)
    tagged = nltk.pos_tag(text)
    for i in  range(len(tagged)):
        x = tagged[i]
        if ((i+1)<len(tagged)):
            nex = tagged[i+1]
        else:
            nex = ("","NP")   
        if (x[1] in verbTags) and (nex[1] not in verbTags):
            root = lemmatizer.lemmatize(x[0],'v') #stemmer.stem(x[0])
            #print root,x[1],x[0]
            if root in freqDict:
                freqDict[root] += 1
                # sentDict[root]  = sentDict[root] + [y] 
            else:
                freqDict[root] = 1
                # sentDict[root] = [y]
            print '*******************************',root,'**************************'
            # print sentDict[root]


tup = freqDict.items()
#print tup
def comps(info1):
    return info1[1]
result = codecs.open("result_wiki_only.csv","w",'utf-8-sig')
tup = sorted(tup,key = comps,reverse = True)
for x in tup:
    #print unicode(x[1])+","+x[0]+"\n"
    result.write(unicode(x[1])+","+x[0]+"\n")
    # result.write('***************************'+unicode(x[1])+","+x[0]+'*****************************\n'+'\n'.join(sentDict[x[0]])+'\n\n')

result.close()
