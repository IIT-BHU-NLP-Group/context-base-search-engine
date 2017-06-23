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

tf = open('/media/krishnkant/ACCC5095CC505BA0/Users/Krishnakanth/Desktop/DIH/PHASE 5/wiki/wiki-Varanasi.txt','r')
text = (tf.read())# .encode('utf-8')
tf.close()

text = text.replace('\"','\'')# .decode('utf-8')

req = 'curl http://model.dbpedia-spotlight.org/en/annotate --data-urlencode \"text=%s\" --data \"confidence=0.1\" -H \"Accept: application/json"'%(text)
status = os.system(req+'> temp.txt')
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
		NER[e[0]] = TYPE[0]
	with open('NER-pickled','w')as f:
		pk.dump(NER,f)



















