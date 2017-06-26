import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import verbnet as vn
import sys

# verb = sys.argv[1]
lemmatizer = WordNetLemmatizer()
# verb = raw_input('enter verb')
Them_Roles = ['Actor','Agent','Asset','Attribute','Beneficiary','Cause','Location','Destination','Source','Experiencer','Extent','Instrument','Material','Product','Material','Product','Patient','Predicate','Recipient','Stimulus','Theme','Time','Topic']

class Node:
	def __init__(self):
		self.children = []
		self.tag = None
		self.head = None

	def __str__(self):
		ret = '< HEAD:%s TAG : %s, CHILDREN: '%(self.head,self.tag)
		for c in self.children:
			ret += c+', '  
		return ret

class vdNode:
	def __init__(self,synlis=[],synstr=''):
		self.synlis = synlis
		self.synstr = synstr

vd = dict()

with open('verb_count_result.csv','r') as f:
	for line in f:
		verb = line.strip().split(',')[1]
		if('/'in verb):
			verb = verb.replace('/','-')
		print verb,'*'*50
		vs = [vn.vnclass(i) for i in vn.classids(verb)]
		for v in vs:
			frames = v.findall('FRAMES/FRAME')
			f_LIST = []
			for i in frames:
				syn_str = vn.pprint_syntax(i)
				print '*',syn_str
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
				# print ' , '.join(lis)

				# Split the tokens of the SYNTAX String
				for l in lis:
					n = Node()
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
							n.children.append(temp)
					# print n
					LIST.append(n)
				f_LIST.append(vdNode(LIST,syn_str))
			vd[verb] = f_LIST



for syn in vd['break']:
	print syn.synstr
	for i in syn.synlis:
		print i,'\n'
					

						
