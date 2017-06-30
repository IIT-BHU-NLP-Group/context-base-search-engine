import verbnet_cleaner
from copy import deepcopy
import re
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import verbnet as vn
import sys

# verb = sys.argv[1]
lemmatizer = WordNetLemmatizer()

temp=""
with open("input.txt","r") as file1:
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

root_list=list()
# strat class 
head_Node={'DT':['DT'],'SBAR':['S','VP','NP','PP'],'SBARQ':['S','VP','NP','PP'],'SQ':['S','VP','NP','PP'],'SINV':['S','VP','NP','PP'],'NP':['NP','NN','PRP','NNS','NNP','CD','VBG'],'S':['VP'],'VP':[ 'VP','VB','VBG','VBD','VBZ','VBN','VBP'],'ADJP':['JJ','PP'],'PP':['NP'],'ROOT':['S'],'PRT':['RP']}

class GraphNode:
    def __init__(self,data): # label is an int, data is DT,VB etc.
        self.data = data # POS Tags
        self.children = [] # CHANGE BY KRISHNKANT
        self.head = None #to update the head based on rules
        self.phrase=None 
        self.tag=None # Relation 
    def add_child(self,child): # Child is an object of type GraphNode
        if not self.children:  # No Child
            self.children = list()
        self.children.append(child)

    def check_child(self,test_object):
        return test_object in self.children




def prepcfg(root,t):
	for j in xrange(t):
		print '\t',
	print root.data+'{'+root.phrase+'}'
	if root.tag!=None:
		for j in xrange(t):
			print '\t',
		print "[",root.tag,"]"

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
		cur_rot.phrase=lst[2]
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
	try:	
		es=''
		for ch in root.children:
			es=es+" "+ch.phrase
		root.phrase=es			
		for p in head_Node[root.data]:
			for ch in root.children:
				if ch.data==p:
					root.head=ch.head
					break
			if root.head != None:
				break 
	except:
		pass							
	return root	


#*****************************START THE GAME FROM HERE*******************
'''stack=[list(),list()]
list_stack=[list(),list()]'''

sco_cur=0
stack=list()
class Result:
	def __init__(self,data_list,data_score):
		self.data_list=data_list
		self.data_score=data_score
	def __str__(self):
		ret='{ '
		for u in self.data_list:
			ret=ret+str(u[0])+" : "+str(u[1])+"\n"
		ret=ret+"score :"+str(self.data_score)+" }"
		return ret	


result_list=list()
result_list_before=list()
def search(root,find_list,flag,u=-1,score_level=5):    
	# root should be list of pcfg tree node
	# find_list should be list of Node 
	# flag show if it is call by itself or not
	# u is not in use
	# score_level decide in which level we are searching upward have high value and down have low

	global sco_cur,root_list
	if len(root)==0 or len(find_list)==0 :
		#print "jaypee eyes :",stack,sco_cur
		if len(stack) >0:
			#print stack,sco_cur
			a=Result(deepcopy(stack),deepcopy(sco_cur))
			if u==1:
				result_list.append(a)
			else: 
				result_list_before.append(a)	
		return [deepcopy(stack),deepcopy(sco_cur)]

	if flag==0:
		bef_verb=list()
		with_verb=list()
		after_verb=list()
		is_verb_occur=0
		for i in root[0].children:

			if i.data=='VP' :
				is_verb_occur=1
				flagg=0
				if i.children[1].data=='VP':
					flagg=1
					flag=0
					try:
						if i.children[1].children[1].data=='VP':
							flag=1
							with_verb=with_verb+i.children[1].children[1].children
					except:
						print "error verb.1.1.1"
					if len(i.children[1].children) > 2 and flag==1:	
						with_verb=with_verb+i.children[1].children[3:]	
					if flag==0:	
						#print i.children[1].phrase
						with_verb=with_verb+i.children[1].children
				if len(i.children) >2 and flagg==1:			
					with_verb=with_verb+i.children[3:]
				if flagg==0:
					with_verb=with_verb+i.children	
			elif is_verb_occur==0 :
				bef_verb.append(i)	
			elif i.data !='.':
				after_verb.append(i)

		befo_verb=list()
		afte_verb=list()
		flag1=0
		for i in find_list:	
			if i.head=='VERB':
				flag1=1
			elif flag1==0 :
				befo_verb.append(i)
			else:
				afte_verb.append(i)
		#print "check",len(bef_verb),len(with_verb),len(after_verb)	

		#search for subject 	
		subject_list,subject_score=search(bef_verb,befo_verb,1,0,score_level)

		#search for predicate
		predicate_list=list()
		predicate_score=0
		for i in xrange(0,len(afte_verb)):
			pre_list1,sco1=search(with_verb,afte_verb[:i],1,1,score_level)
			pre_list2,sco2=search(after_verb,afte_verb[i:],1,1,score_level)
			if sco1+sco2 >predicate_score :
				predicate_list=deepcopy(pre_list1+pre_list2)
				predicate_score=sco1+sco2
		pre_list,sco=search(with_verb,afte_verb,1,1,score_level)
		if sco > predicate_score:
			predicate_score=sco
			predicate_list=pre_list
			
		return [subject_list+predicate_list,predicate_score+subject_score]	
	else:
		match_list=list()
		score=0
		#print root[0].data,find_list[0].head
		if root and find_list :
			root_len=len(root)
			list_len=len(find_list)
			if root_len > 0  and list_len > 0:
				if root[0].data == find_list[0].head :
					
					#start matching preposition from list (may be mistake)
					flag3=0
					if find_list[0].head=='PP' :                  
						for pre in find_list[0].spec_children:
							if pre==root[0].children[0].head :
								flag3=1
								break
					if flag3==1:
						sco_cur=sco_cur+1000
					# end**************
					stack.append([root[0].phrase,find_list[0].tag])
					sco_cur=sco_cur+score_level*100
					try:
						
						match_list,score=search(root[1:],find_list[1:],1,u,score_level-1)
						#print match_list,score
						
					except:
						pass
					stack.pop()
					sco_cur-=score_level*100
					if flag3==1:
						sco_cur-=1000
						
				if root[0].children:
					j=0
					bonus=0
					
					for k in root[0].children:
						try:
							if(k.data==find_list[j].head):
								#start of backchodi**************
								flag3=0
								if find_list[j].head=='PP' :                  
									for pre in find_list[j].spec_children:
										if pre==k.children[0].head :
											flag3=1
											break
								if flag3==1:
									sco_cur=sco_cur+1000
									bonus+=1000
								#end of backchodi*****************	
								sco_cur+= (score_level-1)*100
								stack.append([k.phrase,find_list[j].tag])
								j+=1
								try:
									cur_list,cur_sco=search(root[1:],find_list[j:],1,u,score_level-2)
									if cur_sco > score:
										score=cur_sco
										match_list=deepcopy(cur_list)		
								except:
									pass
						except:
							pass
					for y in xrange(j):
						stack.pop()
						sco_cur-=100*(score_level-1)
					sco_cur-=bonus	
					
				if 	root[0].data == 'S' and find_list[0].head == 'NP':
					print " root data S"
					root_list.append(root[0])
					#start matching preposition from list (may be mistake)
					flag3=0
					if find_list[0].is_sentence==True :                   
						sco_cur=sco_cur+1000
						flag3=1
					# end**************
					stack.append([root[0].phrase,find_list[0].tag])
					sco_cur=sco_cur+score_level*100
					try:
						
						cur_list,cur_sco=search(root[1:],find_list[1:],1,u,score_level-1)
						if cur_sco > score:
							score=cur_sco
							match_list=deepcopy(cur_list)
					except:
						pass
					stack.pop()
					sco_cur-=score_level*100
					if flag3==1:
						sco_cur-=1000
						
					#searching for this sentence
					
					#end
				if 	root[0].data == 'SBAR' and find_list[0].head == 'NP':
					root_list.append(root[0])
					#start matching preposition from list (may be mistake)
					flag3=0
					if find_list[0].is_sentence==True :                   
						sco_cur=sco_cur+1000
						flag3=1
					# end**************
					stack.append([root[0].phrase,find_list[0].tag])
					sco_cur=sco_cur+score_level*100
					try:
						
						cur_list,cur_sco=search(root[1:],find_list[1:],1,u,score_level-1)
						if cur_sco > score:
							score=cur_sco
							match_list=deepcopy(cur_list)
					except:
						pass
					stack.pop()
					sco_cur-=score_level*100
					if flag3==1:
						sco_cur-=1000	
					#searching for this sentence
					
					#end	

				#leave the above tag match list or tag is not found   
				cur_list,cur_sco=search(root[1:],find_list,1,u,score_level)
				if cur_sco > score:
					score=cur_sco
					match_list=cur_list

		return [match_list,score]			


def DictionaryMake(lst):
	s=dict()
	for i in lst:
		for u in i.data_list:
			try:
				if s.has_key(str(u[0])):
					s[str(u[0])].add(u[1])
				else:
					s[str(u[0])]=set()	
					s[str(u[0])].add(u[1])
			except:
				print "DictionaryMake error"	
	return s				


def TreeTag(root,dic):
	if(root.phrase!=None and root.tag==None):
		try:
			for j in dic.keys():
				if j==root.phrase :
					root.tag=dic[j]
					break 
		except:
			print "error 101"	
	if root.children==None:
		return				
	for i in root.children:
		TreeTag(i,dic)


def search_call(sent):
	global result_list , result_list_before
	
	if sent.data=='S' :
		flag_for_verb=0
		verb_temp_name=''
		for  u in sent.children:
			if u.data=='VP':
				flag_for_verb=1
				verb_temp_name=u.head

		if flag_for_verb==1:
			max_score_list=list() 
			verb_name=lemmatizer.lemmatize(verb_temp_name,'v')
			print verb_name
			list_result=list()
			score=0
			for syn in verbnet_cleaner.vd[verb_name]:
				x,y=search([sent],syn.synlis,0) 
				if y > score :
					score=y
					list_result=deepcopy(x)
				# this time global variable result_list give
				# the all possible match for predicates
				# and result_list_before gives the all possible 
				# match with subject
				# I am going to find the list of maximum score list for all sentences
				"""print " ----------result by syntex---------------"
				print syn.synstr
				for u in result_list_before:
					print u	
				print "after verb "	
				for u in result_list:
					print u
				result_list=[]
				result_list_before=[]
				print "------------------------------------------"
				print "\n\n\n"	"""

				# Finding the maximum of every sentences 
				mx=0
				cur_lst=list()
				for u in result_list_before:
					if u.data_score >mx:
						mx=u.data_score
				for u in result_list_before:
					if u.data_score == mx:
						cur_lst+=deepcopy(u.data_list)
						
				mxx=0
				for u in result_list:
					if u.data_score >mxx:
						mxx=u.data_score
				for u in result_list:
					if u.data_score == mxx:
						cur_lst+=deepcopy(u.data_list)

				#append in list
				a=Result(deepcopy(cur_lst),mx+mxx)
				max_score_list.append(a)
				#empty the whole thing
				result_list=[]
				result_list_before=[]
			"""print " ----------result by syntex---------------"
			for u in max_score_list:
				print u	
			print "------------------------------------------"
			print list_result,score 
			# greedy result """
			print ">>>"
			s=DictionaryMake(max_score_list)
			TreeTag(sent,s)
			for u in s.keys():
				print u,":",s[u]
			
		else:
			
			search_call(sent)		


root=treebuild(pcfglist)
prepcfg(root,0)
root_list.append(root.children[0])
while len(root_list) >0:
	t=root_list.pop()
	y=len(root_list)
	for u in range(y-1,-1,-1):
		if id(root_list[u])==id(t):
			root_list.remove(root_list[u])						
	search_call(t)

prepcfg(root,0)













