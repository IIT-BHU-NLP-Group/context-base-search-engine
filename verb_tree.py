from copy import deepcopy

temp=""
with open("../input.txt","r") as file1:
	for l in file1:
		temp=temp+l

pcfg=""
for c in temp:
	if c=='(':
		pcfg=pcfg+c
		pcfg=pcfg+' '
	elif c==')':
		pcfg=pcfg+' '
		pcfg=pcfg+c
	else :
		pcfg=pcfg+c

#print pcfg	

pcfglist=pcfg.split()

# strat class 
head_Node={'DT':['DT'],'NP':['NP','NN','PRP','NNS','NNP','VBG'],'S':['VP'],'VP':[ 'VP','VB','VBG','VBD','VBZ','VBN','VBP'],'ADJP':['JJ','PP'],'PP':['NP'],'ROOT':['S'],'PRT':['RP']}

class GraphNode:
    def __init__(self,data): # label is an int, data is DT,VB etc.
        self.data = data
        self.children = None
        self.head = None #to update the head based on rules

    def add_child(self,child): # Child is an object of type GraphNode
        if not self.children:  # No Child
            self.children = list()
        self.children.append(child)

    def check_child(self,test_object):
        return test_object in self.children




def prepcfg(root,t):
	for j in xrange(t):
		print '\t',
	print root.data,root.head

	if root.children==None:
		return
	t=t+1	
	for i in root.children:

		prepcfg(i,deepcopy(t))		


def treebuild(lst):
	level=0
	l=len(lst)
	#print l
	if l==4:
		cur_rot=GraphNode(lst[1])
		cur_rot.head=lst[2]
		return cur_rot
	lst1=[]
	root=GraphNode(lst[1])
	for t in range(2,l-1):
		lst1.append(lst[t])
		if lst[t]=='(':
			level=level+1
		elif lst[t]==')':
			level=level-1
			if level==0:
				#print "in level 0"
				lst2=deepcopy(lst1)
				#print lst2
				cur_root=treebuild(lst2)
				root.add_child(cur_root)
				lst1=[]
	for p in head_Node[root.data]:
		for ch in root.children:
			if ch.data==p:
				root.head=ch.head
				break
		if root.head != None:
			break 				
	return root	


class SyntaxNode:
	def __init__(self):
		self.tag=None
		self.bracket_tag_list=None
	def pprint(self):
		if self.tag :
			print  "\t\t",self.tag
			print "\t\t--<",
			for i in self.bracket_tag_list:
				print i,		
			print ">--"

class Syntax:
    def __init__(self):
        self.before =None 
        self.after = None

    def add_before(self,child): 
        if not self.before:  
            self.before = list()
        p=SyntaxNode()
        #print child,type(child)
        try:
	        p.tag=child.split('[')[0]
	        p.bracket_tag_list=child.split('[')[1][:-1].split(' ')    
	except:
	    	print "Error 26" 
        self.before.append(p)

    def add_after(self,child): 
        if not self.after:  
            self.after = list()
        p=SyntaxNode()
        #print child,type(child)
        try:
	        p.tag=child.split('[')[0]
	        p.bracket_tag_list=child.split('[')[1][:-1].split(' ')    
	except:
	    	print "Error 37"    
        self.after.append(p)

    def pprint(self):
    	if self.before :
    		print "\t(before) "
    		for j in self.before:
    			j.pprint()
    	if self.after :
    		print "\t(after) "
    		for j in self.after:
    			j.pprint()		


        

class VerbNode:
    def __init__(self,head): 
        self.head = head
        self.syntax = None
        self.semantic = None 

    def add_syntax(self,syntax_list): 
        self.syntax=Syntax()
        flag=0
        for j in syntax_list:
        	if j=='Syntax:':
        		pass
        	elif j=='VERB':
        		flag=1
        	elif flag==0 :
        		self.syntax.add_before(j)
        	elif flag==1:
        		self.syntax.add_after(j)	

    def add_semantic(self,data): 
        if not self.semantic:  
            self.semantic = list()
        self.semantic.append(data)

    def pprint(self):
    	if self.head :
    		print ">(Head)"
    		print "\t",self.head
    		print ">(Syntax)"
    		self.syntax.pprint()
    		print ">(Semantic)"
    		#print len(self.semantic)
    		for j in self.semantic:
    			print "\t",j


class Verb:
	def __init__(self,verb_name):
		self.verb_name=verb_name
		self.frame_list=list()
	def add(self,whole_list) :
		size_whole_list=len(whole_list)
		j=0
		while j < size_whole_list :
			try:
				node=VerbNode(whole_list[j])
				j+=1
				node.add_syntax(whole_list[j])
				j+=1
				if whole_list[j][0]=="Semantics:" :
					try:
						while whole_list[j+1][0]=='*':
							node.add_semantic(whole_list[j+1])
							j+=1
					except:
						print "error 109"				
				self.frame_list.append(node)
			except:
				pass
			j=j+1
			

	def pprint(self):
		if self.verb_name :
			print "******",self.verb_name,"*******"
			for y in self.frame_list:
				print "error 109"
				y.pprint()						
		






line_list=list()
flag=0
verb_name=''
with open("verb_.txt","r") as f1:
	for i in f1:
		cur_line=i.rstrip()
		if flag==0:
			flag=1
			verb_name=cur_line
			continue
		start_flag=1
		bracket_flag=0
		s=str()
		cur_word_list=[]
		for j in cur_line:
			#print j,
			if j==' ' and start_flag==0 and bracket_flag==0 :
				cur_word_list.append(s)
				s=''
			elif j=='[' or j=='(':
				s=s+j
				bracket_flag+=1
			elif j==']' or j==')':
				s=s+j
				bracket_flag-=1
			elif j==' ' and start_flag==1:
				pass	
			else:
				start_flag=0
				s=s+j
		cur_word_list.append(s)
		
		line_list.append(cur_word_list)

class Pattern:
	def __init__(self,tag,list_):
		self.tag=tag
		self.pre_list=list_




#*****************************START THE GAME FROM HERE*******************
stack=[list(),list()]
list_stack=[list(),list()]
sco_cur=0
def search(root,find_list,flag,u=-1,score=5):
	global sco_cur
	if len(root)==0 or len(find_list)==0 :
		if len(stack[u]) >0 :
			list_stack[u].append( [deepcopy(stack[u]),deepcopy(sco_cur)] )
		return

	if flag==0:
		bef_verb=list()
		with_verb=list()
		after_verb=list()
		is_verb_occur=0
		for i in root[0].children:
			if i.data=='VP' :
				is_verb_occur=1
				if i.children[1].data=='VP':
					try:
						if i.children[1].children[1].data=='VP':
							with_verb=with_verb+i.children[1].children[1].children
					except:
						pass
					with_verb=with_verb+i.children[1].children		
				with_verb=with_verb+i.children
			elif is_verb_occur==0 :
				bef_verb.append(i)	
			elif i.data !='.':
				after_verb.append(i)
		befo_verb=list()
		afte_verb=list()
		flag1=0
		for i in find_list:	
			if i.tag=='VERB':
				flag1=1
			elif flag1==0 :
				befo_verb.append(i)
			else:
				afte_verb.append(i)
		#print "check",len(bef_verb),len(with_verb),len(after_verb)		
		search(bef_verb,befo_verb,1,0,score)
		for i in xrange(0,len(afte_verb)):
			search(with_verb,afte_verb[:i],1,1,score)
			search(after_verb,afte_verb[i:],1,1,score)
		search(with_verb,afte_verb,1,1,score)
	else:
		if root and find_list :
			root_len=len(root)
			list_len=len(find_list)
			if root_len > 0 :
				if root[0].data == find_list[0].tag :

					#start matching preposition from list (may be mistake)
					flag3=0
					if find_list[0].tag=='PP' :                   
						for pre in find_list[0].pre_list:
							if pre==root[0].children[0].head :
								flag3=1
								break
					if flag3==1:
						sco_cur=sco_cur+1000
					# end**************
					stack[u].append([root[0].head,find_list[0].pre_list[-1]])
					sco_cur=sco_cur+score*100
					try:
						search(root[1:],find_list[1:],1,u,score-1)
						#print "2",stack
					except:
						pass
					stack[u].pop()
					sco_cur-=score*100
					if flag3==1:
						sco_cur-=1000
				if root[0].children:
					j=0
					bonus=0
					for k in root[0].children:
						try:
							if(k.data==find_list[j].tag):
								#start of backchodi**************
								flag3=0
								if find_list[j].tag=='PP' :                   
									for pre in find_list[j].pre_list:
										if pre==k.children[0].head :
											flag3=1
											break
								if flag3==1:
									sco_cur=sco_cur+1000
									bonus+=1000
								#end of backchodi*****************	
								sco_cur+= (score-1)*100
								stack[u].append([k.head,find_list[j].pre_list[-1]])
								j+=1
								try:
									search(root[1:],find_list[j:],1,u,score-2)		
								except:
									pass
						except:
							pass
					for y in xrange(j):
						stack[u].pop()
						sco_cur-=100*(score-1)
					sco_cur-=bonus		
				search(root[1:],find_list,1,u)						







"""for j in line_list:
	print j"""
v_node=Verb(verb_name)
v_node.add(line_list)
v_node.pprint()

root=treebuild(pcfglist)
prepcfg(root,0)




for u in v_node.frame_list:
	r=u.syntax
	cur_frame=[]
	try:
		for i in xrange(len(r.before)):
			if r.before[i].tag=='PREP':
				y=Pattern("PP",r.before[i].bracket_tag_list+r.before[i+1].bracket_tag_list)
				cur_frame.append(y)
				i+=1
			else:	
				y=Pattern(r.before[i].tag,r.before[i].bracket_tag_list)
				cur_frame.append(y)
		cur_frame.append(Pattern('VERB',[]))
	except:
		pass
	try:		
		for i in xrange(len(r.after)):
			if r.after[i].tag=='PREP':
				y=Pattern('PP',r.after[i].bracket_tag_list+r.after[i+1].bracket_tag_list)
				cur_frame.append(y)
				i+=1
			else:	
				y=Pattern(r.after[i].tag,r.after[i].bracket_tag_list)
				cur_frame.append(y)
	except:
		pass			
	"""for yy in cur_frame:
		print yy.tag,yy.pre_list"""	
	search([root.children[0]],cur_frame,0)
	
	"""for i in list_stack[0]:
		print "fr :",i
	for i in list_stack[1]:
		print "back :" ,i """  

print "**********************************************************"	
t=0
y=0
for i in xrange(0,len(list_stack[0])):
	if t < list_stack[0][i][1]:
		t=list_stack[0][i][1]

for i in xrange(0,len(list_stack[0])):
	if t == list_stack[0][i][1]:
		print list_stack[0][i]

t=0
y=0
for i in xrange(0,len(list_stack[1])):
	if t < list_stack[1][i][1]:
		t=list_stack[1][i][1]
print '-----------------------------------------------------------'
for i in xrange(0,len(list_stack[1])):
	if t == list_stack[1][i][1]:
		print list_stack[1][i]
















