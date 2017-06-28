# -*- coding: utf-8 -*-
import os
import json
import re
import pickle as pk

def get_ontology_by_level():
        f_ont = open('ontology.txt','r')
        text_o = f_ont.read()
        f_ont.close()
        ont = text_o.strip().split('\n')
        ont = [[i.count('.'),i.strip().split()] for i in ont]
        ont.sort(reverse = True)
        # print ont
        level = dict({0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]})
        for o in ont:
                # print o[1],len(o[1])
                # print o[1]
                level[o[0]].append(o[1][1])
        return level

def explore_json(js):
        jo = json.loads(js)
        keys = json.loads(js).keys()
        for k in keys:
                print k,' :: ',
                print jo[k]
        resources = jo['Resources']
        for r in resources:
                for k in r.keys():
                        print k,":",
                        print r[k] , type(r[k])
                print '*'*20


# This is a Very cool Example of DBPedia Spotlight's Sucess
text = 'Anne Hathaway helps to improve the stock prices of American company Berkshire Hathaway.'

tf = open('C:\Users\Harsh\Desktop\context-base-search-engine-improvement-in-pipelines\NER-1\wiki\wiki-Varanasi.txt','r')
text = (tf.read())# .encode('utf-8')
tf.close()

text = text.replace('\"','\'')# .decode('utf-8')

#req = 'curl http://model.dbpedia-spotlight.org/en/annotate --data-urlencode \"text=%s\" --data \"confidence=0.1\" -H \"Accept: application/json"'%(text)
status = 0
if not (status == 0):
        print "ERROR EXIT STATUS : ",status
else:
        # Load Json String
        f = open('temp.txt','r')
        js = f.read()
        f.close()
        
        # Extract info from json
        jo = json.loads(js)
        keys = json.loads(js).keys()
        resources = jo['Resources']

        # Explore Json
        # explore_json(js)

        # Load Ontology
        level = get_ontology_by_level()
        # print level

        # Here we get all the required info. We will use only the resources (which have dbtype not None) as entities. 
        print text
        Entities = []
        for r in resources:
                if not (r['@types'] == ''):
                        Entities.append([r['@surfaceForm'],r['@types']])
        NER = dict()
        NER1 = dict()
        for e in Entities:
                print ' * ',e[0],'==>',#  e[1] 
                type_list = e[1].strip().split(',')
                type_list = [t.strip().split(':')[1] for t in type_list]
                TYPE = []
                # print type_list
                for i in range(7,0,-1):
                        found = False
                        for t in level[i]:
                                if(t in type_list):
                                        TYPE.append(t)
                                        found = True
                        if(found):
                                break
                print TYPE
                
                if NER1.has_key(e[0].lower().split()[0]) and (NER.has_key(e[0].lower()) == False):
                        NER1[e[0].lower().split()[0]].append([e[0].lower(),TYPE[0],len(e[0].lower().split())])
                else:
                        NER1[e[0].lower().split()[0]] = [[e[0].lower(),TYPE[0],len(e[0].lower().split())]]
                print e[0].lower().split()[0]," >>",NER1[e[0].lower().split()[0]]
                NER[e[0].lower()] = TYPE[0]
        with open('NER-pickled','w')as f:
                pk.dump(NER,f)

#Script for replacing the word by a corefrent
annotated = ""
listTags = []
PersonList = []
TempleList = []
DargahList = []
DamList = []
LakeList = []
ChurchesList = []
group = []
tags = {'PERSON':['John Hopkins','Peter Parker','Cristiano Ronaldo'],'LOCATION':['New York','Assi Ghat'],'CHURCHES':['Goa Central Church'],'ORGANIZATION':['Red Wood Works','DLW'],'TEMPLES':['KASHI']}
data = file('output.txt','r')
word_entity_list = []
l = data.readlines()
for x in l:
    node = x.strip("\n").split("\t")
    word_entity_list.append(node)
new_sent = []
sent = ""
match = [False for i in range(len(word_entity_list))]
for x in word_entity_list:
        x[0] = x[0].lower()
for i in range(len(word_entity_list)):
    sent += word_entity_list[i][0]+" "
    if(match[i] == False):
            if ((word_entity_list[i][1] in tags) and ((word_entity_list[i][1] != word_entity_list[i+1][1]) or (i+1 == len(word_entity_list) ))): 
                lis = tags[word_entity_list[i][1]]
                #print word_entity_list[i][0],word_entity_list[i][1]
                group.append(word_entity_list[i][0].lower())
                #print group
                match[i] = True
                entity_name = " ".join(group)
                group = []
                NERTag = ""
                if( NER.has_key(entity_name.lower().strip())):
                        NERTag = NER[entity_name]
                else:  
                        NERTag = word_entity_list[i][1]
                print entity_name,">>",NERTag
                new_word = lis.pop()
                new_sent.append(new_word)
            elif (word_entity_list[i][1] not in tags):
                maxmatch = 0
                tag = ""
                entity = ""
                #print word_entity_list[i][0].lower()
                #print NER1['emperor']
                if((word_entity_list[i][0].lower()) in NER1):
                        #print word_entity_list[i][0].lower()
                        for x in NER1[word_entity_list[i][0].lower()]:
                                #print x
                                length = x[2]
                                p = x[0].split(" ")
                                #print p
                                for j in range(length):
                                        #print word_entity_list[i+j][0].lower()
                                        #print p[j].lower()
                                        if(word_entity_list[i+j][0].lower() == p[j].lower()):
                                                                 #print word_entity_list[i+j][0].lower() 
                                                                 pass
                                        else:
                                                                 break
                                else:
                                                                 if(maxmatch < length):
                                                                         maxmatch = length
                                                                         tag = x[1]
                                                                         entity = x[0]
                        for j in range(maxmatch):
                                match[i+j] = True
                if(entity != ""):
                        print entity,">>",tag
                else:
                        print word_entity_list[i][0],">> O"

                                                                 
            else:
                group.append(word_entity_list[i][0].lower())

print sent
print " ".join(new_sent)

        
        

















