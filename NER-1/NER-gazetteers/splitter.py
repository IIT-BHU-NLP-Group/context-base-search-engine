from nltk.tokenize import sent_tokenize
#from nltk.tag.stanford import StanfordPOSTagger
import nltk
#st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
locs = [ 'churches', 'dam', 'dargahs', 'ghats','lake','mosques', 'mountains', 'rivers']
# cities = ['story']
files = [loc+'.txt' for loc in locs]


import codecs
import os
#files = 
for file in files:
	f =open(file, 'r')
	f2=open(file+"2",'w')
	