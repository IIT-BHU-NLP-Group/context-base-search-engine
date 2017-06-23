import xml.etree.ElementTree as ET
import codecs
import os
# from nltk.tag.stanford import StanfordPOSTagger

# cities = [ 'Agra', 'Jaipur', 'Banglore', 'Gangtok','Varanasi','Kanpur', 'Goa', 'Nainital', 'Mathura', 'Darjiling', 'Manali', 'Kullu', 'Ujjain', 'Mumbai', 'Amritsar', 'Ooty','Kolkata', 'Hyderabad','Delhi', 'Guwahati','New_Delhi']
cities = ['story']
files = ['wiki-'+city+'.txt' for city in cities]

for fl_name in files:
	fc =open('./wiki/'+fl_name,'r')
	os.chdir('./stanford-corenlp-full-2017-06-09/')

	for l in fc:
		fi =open('./input.txt','w') 
		fi.write(l)
		fi.close()
		os.system('java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file input.txt')
		tree = ET.parse('input.txt.xml')
		root = tree.getroot()

		sentences = root.find('document').find('sentences').findall('sentence')
		sent_list = []
		pos_list = []


		for sent in sentences:
			s_list, p_list = [], []
			for tok in sent.find('tokens').findall('token'):
				s_list.append(tok.find('word').text)
				p_list.append(tok.find('POS').text)
				# print tok.find('word').text,
			sent_list.append(s_list)
			pos_list.append(p_list)
		print '\n','*'*15,'\n'



		coreferences = root.find('document').find('coreference').findall('coreference')



		for corr in coreferences:
			head_word = ''
			once_occurred = []
			for mention in corr.findall('mention'):
				if(mention.get('representative') == 'true'):
					head_word = mention.find('text').text
					print head_word,'<-- head'
				else:
					word = mention.find('text').text
					sent_i = int(mention.find('sentence').text)-1
					start_i = int(mention.find('start').text)-1
					end_i = int(mention.find('end').text)-1		
					print word
					if (end_i-start_i==2 and pos_list[sent_i][start_i]=='DT' and (pos_list[sent_i][start_i]=='NN' or pos_list[sent_i][start_i]=='NNS')):
						for i in range(start_i,end_i):
							sent_list[sent_i][i] = ""# print '%s(del)'%sent_list[sent_i][start_i],
						del sent_list[sent_i][start_i]
						sent_list[sent_i].insert(start_i,head_word)
					elif (end_i-start_i==1 and (pos_list[sent_i][start_i]=='PRP' or pos_list[sent_i][start_i]=='PRP$')):
						for i in range(start_i,end_i):
							sent_list[sent_i][i] = ""# print '%s(del)'%sent_list[sent_i][start_i],
						del sent_list[sent_i][start_i]
						if(pos_list[sent_i][start_i]=='PRP'):
							sent_list[sent_i].insert(start_i,head_word)
						else:
							sent_list[sent_i].insert(start_i,head_word+'\'s')
					elif (word.lower() in once_occurred):
						# print '# ',sent_list[sent_i][:],' #'
						# print start_i,len(sent_list[sent_i])
						for i in range(start_i,end_i):
							sent_list[sent_i][i] = ""# print '%s(del)'%sent_list[sent_i][start_i],
						del sent_list[sent_i][start_i]
						sent_list[sent_i].insert(start_i,head_word)
					else:
						once_occurred.append(word.lower())

		print '\n','*'*15,'\n'


		# result = codecs.open("output.txt","w",'utf-8-sig')
		result = open("./../out/output-"+fl_name,"a+")
		for s in sent_list:
			for w in s:
				result.write(w.encode('utf-8')+' ')
				# result.write(unicode(w+' '))
		result.close()	
	fc.close()
	fi.close()
	os.chdir('./../')
