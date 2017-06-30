import re
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import verbnet as vn
import sys

# verb = sys.argv[1]
lemmatizer = WordNetLemmatizer()
# verb = raw_input('enter verb')
Them_Roles =['Participant','Actor','Agent','Co-Agent','Cause','Stimulus','Undergoer','Beneficiary','Attribute','Pivot','Instrument','Theme','Co-Theme','Topic','Patient','Co-Patient','Experiencer','Material','Result','Product','Place','Source','Initial_Location','Material','Goal','Result','Product','Destination','Recipient','Location','Initial_Location','Destination','Recipient','Value','Asset','Extent','Trajectory','Time','Duration','Initial_Time','Final_Time','Frequency']
 #['Actor','Agent','Asset','Attribute','Beneficiary','Cause','Location','Destination','Source','Experiencer','Extent','Instrument','Material','Product','Material','Product','Patient','Predicate','Recipient','Stimulus','Theme','Time','Topic']
# tha following list contains all those syntactic restrictions which make a phrase a sentence (many more restrictions yet to be added).
SENT = ['THAT_COMP','WH_COMP','FOR_COMP','WHAT_EXTRACT','HOW_EXTRACT','WH_EXTRACT','WH_INF','WHAT_INF','SC_TO_INF','WHETH_INF','RS_TO_INF','NP_PPART','BE_SC_ING','POSS_ING','SC_TO_ING','NP_P_ING','TO_BE','QUOTATION']

#print len(SENT)


class Node:
	def __init__(self):
		self.children = []
		self.spec_children = [] # Special Children list to be used for NP when PREP NP sequence comes(while main list stores for PREP).
		self.tag = ''
		self.head = None
		self.is_sentence = False

	def __str__(self):
		ret=''
		ret=ret+"\n Head : "+str(self.head)	
		ret=ret+"\n Tag : "+str(self.tag)
		ret=ret+"\n Sentence : "+str(self.is_sentence)+"\n"	 
		ret=ret+' Children : [ '
		for u in self.children:
			ret=ret+str(u)+", "
		ret=ret+" ] "
		ret=ret+"\n Spec-children : [ "
		for u in self.spec_children:
			ret=ret+str(u)+", "
		ret=ret+" ] "

		
		return ret

class vdNode:
	def __init__(self,synlis=[],synstr=''):
		self.synlis = synlis
		self.synstr = synstr

vd = dict()

with open('new_verb_count_result.csv','r') as f:
	for line in f:
		verb = line.strip().split(',')[1]
		if(verb == 'build'):print verb
		if('/'in verb):
			verb = verb.replace('/','-')
		#print '\n',verb,'*'*50
		# vs = [vn.vnclass(i) for i in vn.classids(verb)]
		# for v in vs:
		with open('Aug-Verbnet/%s.txt'%verb,'r')as vfile:
			# frames = v.findall('FRAMES/FRAME')
			f_LIST = []
			# for i in frames:
			for l in vfile:
				syn_str = l.strip()# vn.pprint_syntax(i)
				# if(verb == 'build'):print '*',syn_str
				# Split the main SYNTAX string
				lis = [] # holds the tokens in form of String
				LIST = [] # holds the tokens in original form
				temp = ''
				op = 0
				for s in syn_str:
					temp+=s
					if(s == '['):
						op+=1
						continue
					if(s == ']'):
						op-=1
						continue
					if(op == 0 and s == ' '):
						lis.append(temp.strip())
						temp = ''
				if(temp!=''):
					lis.append(temp.strip())
				# print ' , '.join(lis)

				# Split the tokens of the SYNTAX String
				prev_head, head = '', ''
				for l in lis:
					n = Node()
					prev_head = head
					temp,head = '',''
					for i in l:
						if(i=='['):break
						head += i 
					n.head = head
					op = 0
					first = True
					for s in l:
						if(s == '['):
							op+=1
							continue
						if(s == ']'):
							op-=1
							break
						if(op!=0 and (s!=' ')):
							temp+=s
						elif(op!=0 ): 
							# print 'REACHED HERE'
							if(first and (temp in Them_Roles) ):
								n.tag = temp
								first = False	
							else:
								n.children.append(temp)
							temp=''
					if(temp!=''):
						if(first and (temp in Them_Roles) ):
							n.tag = temp
						else:
							n.children.append(temp.strip().strip('+').strip('-'))
					for t in SENT:  
						if(t.lower() in n.children):
							n.is_sentence = True
							break
					if(prev_head == 'PREP'):
						#print '-'*10
						prev_n = LIST.pop()
						prev_n.head = 'PP'
						prev_n.spec_children = n.children
						prev_n.tag = n.tag 
						n = prev_n
					if(n.tag == 'ADV'):n.tag = 'ADVP'
					if(n.children == []):n.children = ''
					LIST.append(n)
					# if(verb == 'build'):print n
				f_LIST.append(vdNode(LIST,syn_str))
			vd[lemmatizer.lemmatize(verb,'v')] = f_LIST

# for j in vd['build']:
# 	print 'here2'
#	print j.synstr
#	for y in j.synlis:
#		print "************\n"
#		print y ,
#		print "\n************\n"
#	print " "
						
