from nltk.tag import StanfordNERTagger
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tag.stanford import StanfordPOSTagger
import pickle as pk

st = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')  
st1 = StanfordPOSTagger('english-bidirectional-distsim.tagger')
# print st.tag('Ram is a god boy. Ramzan is a holy month. Rami Eid was studying at Stony Brook University in NY at 9:00 pm on 23 July, 2017.'.split())

cities = [ 'Agra', 'Jaipur', 'Banglore', 'Gangtok','Varanasi','Kanpur', 'Goa', 'Nainital', 'Mathura', 'Darjiling', 'Manali', 'Kullu', 'Ujjain', 'Mumbai', 'Amritsar', 'Ooty','Kolkata', 'Hyderabad','Delhi', 'Guwahati','New_Delhi']
# cities = ['Varanasi']
cfiles = ['wiki-'+city+'.txt' for city in cities]

entities = ['temples','churches','dam','lake' ,'dargahs' ]

ent = dict() 
for e in entities:
	fc =open('NER-gazetteers/'+e+'.txt','r')
	text  = fc.read()
	fc.close()
	ent[e] = text.lower().strip().split('\n')

for fl_name in cfiles:
	fc =open('./wiki/'+fl_name,'r')
	text  = fc.read()	
	fc.close()
	inp = nltk.word_tokenize(text.decode('utf-8'))
	ner = st.tag(inp)
	for i in xrange(len(ner)):
		ner[i] = [ner[i][0],ner[i][1] ]
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]=='ORGANIZATION'):
			if( i>1 and not ner[i-1][1]=='ORGANIZATION'):
				word = ner[i][0].lower()
				org_pos = [ner[i][1].lower()]
				best_match = 'ORGANIZATION'	
				j = i+1
				while( j<len(ner)  and ner[j][1]=='ORGANIZATION' ):
					word = word +' '+ner[j][0].lower()
					org_pos.append([ner[j][1].lower()])
					j+=1
				# print '-----   ', word
				# YOU GET THE ORG TAGGED PHRASE HERE 
				# FIRST DO GAZETTEER SEARCH AND CHANGE TAGS WITH EXACT MATCH
				org_l = word.split()
				for en in entities:
					for e in ent[en]:
						count = 0	
						for x in range(len(org_l)):
							for y in range(x,len(org_l)):		
								w = ''
								# print x,y
								for z in range(x,y+1):
									w = w + ' ' + org_l[z] 
								if w.strip() == e.strip().lower(): 
									best_match = en
									# print (' '+w+' ') ,(' '+e+' ')
				# if (len(org_l)>=3 and (org_l[0].lower()== or org_l[0].lower()=='temples') and org_l[1]=='of'):
				# 	flag = True
				# 	for i in range(2,len(org_l)):
				# 		if not (org_pos[i]=='NNP'): 
				# 			flag=False
				# 			break
				# if(flag = True):
				# 	best_match = en
				j = i
				while( j<len(ner)  and ner[j][1]=='ORGANIZATION'):
					ner[j][1] = best_match.upper()
					j+=1
	f = open('ner-vara','w')
	pk.dump(ner,f)
	f.close()
	en = 'TEMPLES'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')	
	en = 'MOSQUES'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')	
	en = 'DAM'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')				
	en = 'LAKE'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')	
	en = 'CHURCHES'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')	
	en = 'DARGAHS'
	print en
	for i in xrange(len(ner)):
		# print ner[i][0].encode('utf-8'),'\t',ner[i][1].encode('utf-8')
		if(ner[i][1]==en):
			if( i>1 and not ner[i-1][1]==en):
				word = ner[i][0].lower()
				best_match = [0,en]	
				j = i+1
				while( j<len(ner)  and ner[j][1]==en ):
					word = word +' '+ner[j][0].lower()
					j+=1
				print '#####   ', word.encode('utf-8')		
	# Print NER tags for ALL tokens
	# for i in ner:
	# 	print i[0].encode('utf-8'),'\t',i[1].encode('utf-8')
