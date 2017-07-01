import verb_tree as vt
from copy import deepcopy


nouns = ['NP','NX','NN','NNS','NNP','NNPS','PRP']# for noun phrases also consider the NX
adjectives = ['JJ','JJR','JJS']
adverb = ['RB','RBR','RBS']
verbs  = ['VB','VBD','VBG','VBN','VBP','VBZ']

class GraphNode:
    def __init__(self,data): # label is an int, data is DT,VB etc.
        self.data = data
        self.children = None
        self.head = None #to update the head based on rules
        self.phrase=None
        self.relation=None
    def add_child(self,child): # Child is an object of type GraphNode
        if not self.children:  # No Child
            self.children = list()
        self.children.append(child)
    def check_child(self,test_object):
        return test_object in self.children

def prepcfg(root,t):
	for j in xrange(t):
		print '\t',
	if(root.data == 'NP'):
		root = augment_NP(root)
	if(root.data == 'VP'):
		root = augment_VP(root)
	if(root.data == 'PP'):
		root = augment_PP(root)
	if(root.data == 'ADJP'):
		root = augment_ADJP(root)
	if('ADJP' in [c.data for c in root.children]):
		ac,at,vt,vc =  None, None, None, None
	 	for c in root.children:
	 		if(c.data == 'ADJP'):
	 			ac,at = deepcopy(c),c
	 		if(c.data in verbs):
	 			vc,vt = deepcopy(c),c
	 	root.children.remove(at)
	 	if(vc is not None):
	 		root.children.remove(vt)
	 	Children  = []
	 	Children += root.children

	 	ac = augment_ADJP(ac)
	 	for c in ac.children:
	 		Children.append(c)
	 	if(vc is not None):
	 		root.phrase = vc.phrase
	 	root.children = Children

	print root.data+'{'+root.phrase+'}' 
	if root.relation!=None:
		for j in xrange(t):
			print '\t',
		print "<",root.relation,">"
	if root.tag!=None:
		for j in xrange(t):
			print '\t',
		print "[",root.tag,"]"
	if root.children==None:
		return
	t=t+1	
	for i in root.children:
		prepcfg(i,deepcopy(t))	

def augment_PP(root):
	# print '*'*20,root.data,root.phrase,'*'*20
	if(root.children == None):
		return root
	# Rule PP <- IN NP
	PREP_child,NP_child=None,None
	P_temp,NP_temp = None,None
	for c in root.children:
		if(c.data == 'IN' or c.data == 'TO'):
			PREP_child, P_temp= deepcopy(c),c
		elif (c.data in nouns ):# (c.data == 'NP'):
			NP_child, NP_temp= deepcopy(c),c
	root.children.remove(NP_temp)
	root.children.remove(P_temp)
	if(root.relation is not None): # and (IN_child is not None):
		root.data, root.children, root.phrase, root.head = 'NP', NP_child.children, NP_child.phrase, NP_child.head
		root.relation.add( PREP_child.phrase) 
	else:
		root.data, root.children, root.phrase, root.relation ,root.head = 'NP', NP_child.children, NP_child.phrase, [PREP_child.phrase], NP_child.head 
	
	# print '{{',root.data,root.phrase,root.relation,'}}'
	root = augment_NP(root)
	return root

def augment_NP_VBG(root):
 	# Rule NP <- NP (VP) <- NP (VBG NP)
 	NP = False
	for n in nouns:
		if n in [c.data for c in root.children]:
			NP=True 
 	if(root.data == 'NP') and NP and ('VP'in [c.data for c in root.children]):
	 	parent = root
	 	vc,nc,vt,nt = None, None, None, None
	 	for c in parent.children:
	 		if(c.data == 'VP'):
	 			vc,vt = deepcopy(c),c
	 		if(c.data in nouns ):#(c.data == 'NP'):
	 			nc, nt = deepcopy(c),c
	 	parent.children.remove(nt)
		parent.children.remove(vt)
		
		root = vc
	 	NP_child, VBG_child = None,None
	 	V_temp,N_temp = None,None
	 	for c in root.children:
	 		if(c.data == 'VBG'):
				VBG_child, V_temp= deepcopy(c),c
			elif(c.data in nouns ):#(c.data == 'NP'):
				NP_child, N_temp= deepcopy(c),c

		if(VBG_child == None):
			return parent

		root.children.remove(N_temp)
		root.children.remove(V_temp)
		root.data, root.children, root.phrase, root.relation ,root.head = 'NP', NP_child.children, NP_child.phrase, VBG_child.phrase, NP_child.head 
		
		root = augment_NP(root)

		nc = augment_NP(nc)

		nc.children.append(root)
		
		return nc
	return root


def augment_ADJP(root):
	RB,PP,CC,JJ = False,False,False,False
	for c in root.children:
		if(c.data in adverb):
			RB = True
		if(c.data in adjectives):
			JJ = True
		elif(c.data  == 'PP'):
			PP = True
		elif(c.data  == 'CC'):
			CC = True

	# RULE ADJP <- RB* ADJ PP
	if (root.data == 'ADJP') and RB and PP and (not CC):
		jc, rbc, pc, jt, rbt , pt = None, [], None, None, [], None 
	 	for c in root.children:
	 		if(c.data == 'PP'):
	 			pc = deepcopy(c)
	 			pt = c
	 		if(c.data in adjectives):
	 			jc = deepcopy(c)
	 			jt = c
	 		if(c.data in adverb ):#(c.data == 'NP'):
	 			rbc.append(deepcopy(c))
	 			rbt.append(c)
	 	root.children.remove(pt)
	 	root.children.remove(jt)
	 	for j in rbt:
	 		root.children.remove(j)

	 	root.children = []
	 	jc.relation = 'modifier'
	 	jc.children = []
	 	jc.children.append(augment_PP(pc))
	 	for r in rbc:
	 		r.relation = 'adjectival-modifier'
	 		jc.children.append(r)
	 	root.children.append(jc)
	 	return root

	# RULE ADJP <- RB* ADJ
	elif (root.data == 'ADJP') and RB and (not PP and not CC):
		jc, rbc, jt, rbt  = None, [], None, [] 
	 	for c in root.children:
	 		if(c.data in adjectives):
	 			jc = deepcopy(c)
	 			jt = c
	 		if(c.data in adverb ):#(c.data == 'NP'):
	 			rbc.append(deepcopy(c))
	 			rbt.append(c)
	 	root.children.remove(jt)
	 	for j in rbt:
	 		root.children.remove(j)

	 	root.children = []
	 	jc.relation = 'modifier'
	 	jc.children = []
	 	for r in rbc:
	 		r.rag = 'adjectival-modifier'
	 		jc.children.append(r)
	 	root.children.append(jc)
	 	return root

	# RULE ADJP <- ADJ PP
	elif (root.data == 'ADJP') and PP and (not CC and not RB):
		jc, pc, jt , pt = None, None, None, None 
	 	for c in root.children:
	 		if(c.data == 'PP'):
	 			pc = deepcopy(c)
	 			pt = c
	 		if(c.data in adjectives):
	 			jc = deepcopy(c)
	 			jt = c
	 	root.children.remove(pt)
	 	root.children.remove(jt)

	 	root.children = []
	 	jc.relation = 'modifier'
	 	jc.children = [augment_PP(pc)]
	 	root.children.append(jc)
	 	return root

	# RULE ADJP <- ADJP (CC ADJP (CC ADJ)*)*
	elif (root.data == 'ADJP') and CC and (not PP and not RB):
		jc, ac, jt , at, faltu = [], [], [], [], []
	 	for c in root.children:
	 		if(c.data == 'DT')or(c.data == 'CC'):
	 			faltu.append(c)
	 		if(c.data in adjectives):
	 			jc.append(deepcopy(c))
	 			jt.append(c)
	 		if(c.data == 'ADJP' ):#(c.data == 'NP'):
	 			ac.append(deepcopy(c))
	 			at.append(c)
	 	for f in faltu:
		 	root.children.remove(f)
	 	for a in at:
	 		root.children.remove(a)
	 	for j in jt:
	 		root.children.remove(j)
	 	Children = []
	 	for j in jc:
	 		j.relation='modifier'
	 		Children.append(j)
	 	for a in ac:
	 		Children.append(augment_ADJP(a))
	 	root.children = Children
	 	return root

	# default RULE ADJP <- something ADJ*
	elif (root.data == 'ADJP') and (JJ):
		jc,jt, faltu = [], [], []
	 	for c in root.children:
	 		if(c.data == 'DT')or(c.data == 'CC'):
	 			faltu.append(c)
	 		if(c.data in adjectives):
	 			jc.append(deepcopy(c))
	 			jt.append(c)
	 	for f in faltu:
		 	root.children.remove(f)
	 	for j in jt:
	 		root.children.remove(j)
	 	Children = []
	 	for j in jc:
	 		j.relation='modifier'
	 		Children.append(j)
	 	root.children = Children
	 	return root
	return root




def augment_NP(root):
	# print '*'*30
	# print '#'*20,root.data,root.phrase,'#'*20
	if(root.children == None):
		return None

	only_nouns = True # only nouns in NP
	ADJP = False# any ADJP in np
	NP = False # any nouns in np
	ADJ = False# any adjectives in NP
	for c in root.children:
		if not (c.data in nouns):
			only_nouns = False
		if(c.data == 'ADJP'):
			ADJP = True
		if(c.data in nouns):
			NP=True
		if(c.data in adjectives):
			ADJ=True

	# RULE NP <- NP PP
	if(root.data == 'NP') and NP and ('PP'in [c.data for c in root.children]):
		# print 'HERERERERERE ',root.data,root.phrase
	 	pc,nc,pt,nt = None, None, None, None
	 	for c in root.children:
	 		if(c.data == 'PP'):
	 			pc,pt = deepcopy(c),c
	 		if(c.data in nouns ):#(c.data == 'NP'):
	 			nc, nt = deepcopy(c),c
	 	root.children.remove(nt)
		root.children.remove(pt)

		parent = root
		nc = augment_NP(nc)
		nc.children+=[augment_PP(pc)]

		if(parent.relation is not None):
			parent.data, parent.children, parent.phrase, parent.head = nc.data, nc.children, nc.phrase, nc.head 
			# parent.relation = pc.relation
		else:
			parent.data, parent.children, parent.phrase,   parent.head = nc.data, nc.children, nc.phrase, nc.head 
		# print '#'*20,nc.phrase

		# print '\\\\',parent.data,parent.phrase,parent.relation,'//'
		return parent
	
	# Rule NP <- NP (VP) <- NP (VBG NP) 
	if(root.data == 'NP') and NP and ('VP'in [c.data for c in root.children]):
		nc = augment_NP_VBG(root)
		if(root.relation is not None): # and (IN_child is not None):
			root.data, root.children, root.phrase, root.head = nc.data, nc.children, nc.phrase, nc.head
			# print '#'*20,nc.relation
			# root.relation.add(nc.relation) 
		else:
			root.data, root.children, root.phrase, root.relation ,root.head = nc.data, nc.children, nc.phrase, nc.relation, nc.head 
	
	# RULE ADJP in NP
	elif(root.data == 'NP') and ADJP and NP:
		ac,at,nc,nt =  None, None, None, None
	 	for c in root.children:
	 		if(c.data in nouns):
	 			nc,nt = deepcopy(c),c
	 		if(c.data == 'ADJP'):
	 			ac,at = deepcopy(c),c
	 	root.children.remove(at)
	 	root.children.remove(nt)

	 	nc = augment_NP(nc)
	 	ac = augment_ADJP(ac)
	 	Children = []
	 	for a in ac.children:
	 		a.relation = 'modifier'
	 		Children.append(a)
	 	root.children = Children
	 	root.phrase = nc.phrase 
	 	return root 

	# RULE NP <- DT ADJ* Noun
	elif(root.data == 'NP') and NP and ADJ:
		JJc,nc,JJt,nt,dt = [], [], [], [], None
	 	for c in root.children:
	 		if(c.data == 'DT'):
	 			dt = c
	 		if(c.data in adjectives):
	 			JJc.append(deepcopy(c))
	 			JJt.append(c)
	 		if(c.data in nouns ):#(c.data == 'NP'):
	 			nc.append(deepcopy(c))
	 			nt.append(c)
	 	root.children.remove(dt)
	 	for n in nt:
	 		root.children.remove(n)
	 	for j in JJt:
	 		root.children.remove(j)
	 	
	 	Children = []
	 	phrase = '' 
	 	for n in nc:
		 	nn = augment_NP(n)
		 	phrase+= nn.phrase+' '
	 	for j in JJc:
	 		j.relation = 'modifier'
		 	Children.append(j)

		root.data, root.children, root.phrase, root.head = 'NP', Children, phrase, None
		# print '#'*20
		# for i in root.children:
		# 	print i.phrase,i.data, i.relation 
		return root
	
	# RULE NP <- only_nouns
	elif(root.data == 'NP') and only_nouns:
		# print '3'*20, root.data, root.phrase
		nc,nt = [],[]
		for c in root.children:
	 		if(c.data in nouns):# (c.data == 'NP'):
	 			nc.append(deepcopy(c))
	 			nt.append(c)
		phrase = ''
		for c in nc:
			phrase += c.phrase+' '
		if not(phrase == ''):
			root.phrase = phrase

		# print '{{{',root.data,phrase,'}}}'
		root.children = []
		return root

	# RULE NP <- SOMETHING NP
	elif (root.data == 'NP') and ('NP'in [c.data for c in root.children]):
		nc = None
		for c in root.children:
	 		if(c.data == 'NP'):
	 			nc = c
		nc = augment_NP(nc)		
		# Keep the relation of the root and update all other things # root.relation not <- nc.relation
		root.data, root.children, root.phrase,root.head = nc.data, nc.children, nc.phrase, nc.head 
		# print '//',root.children[0].data,root.children[0].phrase,root.children[0].relation,'\\\\'
		return root

	# RULE NP <- SOMETHING(DT) noun
	elif(root.data == 'NP') and NP:
		# print '*'*20, root.data, root.phrase
		nc,nt = [],[]
		for c in root.children:
	 		if(c.data in nouns):# (c.data == 'NP'):
	 			nc.append(deepcopy(c))
	 			nt.append(c)
	 	is_NP = ('NP' in [c.data for c in root.children])
	 	
		root.children = []
		phrase = ''
		for c in nc:
			phrase += c.phrase+' '
		root.phrase = phrase
		if(is_NP):
			for c in nc:
				if(c.data == 'NP'):
					c = augment_NP(c)
					root.children.append(c)
			# print "<><>",root.children[0].children[0].phrase,"<><>"
		return root
	# Default
	return root

def augment_VP(root):
	if(root.children is None):
		return root
	# RULE verb
	if(root.data in verbs):
		return root
	
	VP =False
	for c in root.children:
		if(c.data in verbs):
			VP = True
	# RULE VP <- verb ...
	if (root.data == 'VP') and VP:
		# print '#'*20,'<%s>'%root.phrase
		vc,vt,vpt,vpc = None, None, None, None
	 	for c in root.children:
	 		if(c.data == 'VP'):
	 			vpc,vpt = deepcopy(c),c
	 		if(c.data in verbs):
	 			vc,vt = deepcopy(c),c
	 	# root.children.remove(vt)
	 	if(vpt is not None):
	 		root.children.remove(vpt)
	 		vpc = augment_VP(vpc)
			Children  = []
	 		Children += root.children 
	 		Children += vpc.children
	 		root.children =  Children
	 		root.phrase = vpc.phrase
	 	else:
		 	root.phrase = vc.phrase
		 	root.children.remove(vt)

	 	return root
	return root

# def augment(root):
# 	if(root.data =='PP'):
# 		root = augment_PP(root)

root = vt.root

prepcfg(root,0)
# vt.prepcfg(root,0)
