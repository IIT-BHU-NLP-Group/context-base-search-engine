import verb_tree as vt
from copy import deepcopy


nouns = ['NP','NX','NN','NNS','NNP','NNPS','PRP']# for noun phrases also consider the NX
adjectives = ['JJ','JJR','JJS']


class GraphNode:
    def __init__(self,data): # label is an int, data is DT,VB etc.
        self.data = data
        self.children = None
        self.head = None #to update the head based on rules
        self.phrase=None
        self.tag=None
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
	if(root.data == 'PP'):
		root = augment_PP(root)
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

def augment_PP(root):
	# print '*'*20,root.data,root.phrase,'*'*20
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
	if(root.tag is not None): # and (IN_child is not None):
		root.data, root.children, root.phrase, root.head = 'NP', NP_child.children, NP_child.phrase, NP_child.head
		root.tag.add( PREP_child.phrase) 
	else:
		root.data, root.children, root.phrase, root.tag ,root.head = 'NP', NP_child.children, NP_child.phrase, PREP_child.phrase, NP_child.head 
	
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
		root.data, root.children, root.phrase, root.tag ,root.head = 'NP', NP_child.children, NP_child.phrase, VBG_child.phrase, NP_child.head 
		
		root = augment_NP(root)

		nc = augment_NP(nc)

		nc.children.append(root)
		
		return nc
	return root




def augment_NP(root):
	# print '*'*30
	# print '*'*20,root.data,root.phrase,'*'*20
	if(root.children == None):
		return None


	only_nouns = True # only nouns in NP
	for c in root.children:
		if not (c.data in nouns):
			only_nouns = False
	NP = False # any nouns in np
	for n in nouns:
		if n in [c.data for c in root.children]:
			NP=True
	ADJ = False# any adjectives in NP
	for a in adjectives:
		if a in [c.data for c in root.children]:
			ADJ=True

	# RULE NP <- NP PP
	if(root.data == 'NP') and NP and ('PP'in [c.data for c in root.children]):
	 	pc,nc,pt,nt = None, None, None, None
	 	for c in root.children:
	 		if(c.data == 'PP'):
	 			pc,pt = deepcopy(c),c
	 		if(c.data in nouns ):#(c.data == 'NP'):
	 			nc, nt = deepcopy(c),c
	 	root.children.remove(nt)
		root.children.remove(pt)

		parent = root
		nc.children=[augment_PP(pc)]

		if(parent.tag is not None):
			parent.data, parent.children, parent.phrase, parent.head = nc.data, nc.children, nc.phrase, nc.head 
			parent.tag.add(pc.tag)
		else:
			parent.data, parent.children, parent.phrase, parent.tag , parent.head = nc.data, nc.children, nc.phrase, pc.phrase, nc.head 
		# print '#'*20,nc.phrase

		return parent
	
	# Rule NP <- NP (VP) <- NP (VBG NP) 
	if(root.data == 'NP') and NP and ('VP'in [c.data for c in root.children]):
		nc = augment_NP_VBG(root)
		if(root.tag is not None): # and (IN_child is not None):
			root.data, root.children, root.phrase, root.head = nc.data, nc.children, nc.phrase, nc.head
			# print '#'*20,nc.tag
			# root.tag.add(nc.tag) 
		else:
			root.data, root.children, root.phrase, root.tag ,root.head = nc.data, nc.children, nc.phrase, nc.phrase, nc.head 
	
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
		 	phrase+= nn.phrase
	 	for j in JJc:
	 		j.tag = 'modifier'
		 	Children.append(j)

		root.data, root.children, root.phrase, root.head = 'NP', Children, phrase, None
		# print '#'*20
		# for i in root.children:
		# 	print i.phrase,i.data, i.tag 
		return root


	# RULE NP <- SOMETHING NP
	elif (root.data == 'NP') and ('NP'in [c.data for c in root.children]):
		nc = None
		for c in root.children:
	 		if(c.data == 'NP'):
	 			nc = c
		nc = augment_NP(nc)		
		# Keep the tag of the root and update all other things # root.tag not <- nc.tag
		root.data, root.children, root.phrase,root.head = nc.data, nc.children, nc.phrase, nc.head 
		return root
	
	# RULE NP <- only_nouns
	elif(root.data == 'NP') and only_nouns:
		root.children = []
		return root

	# RULE NP <- SOMETHING(DT) noun
	elif(root.data == 'NP') and NP:
		nc,nt = None,None
		for c in root.children:
	 		if(c.data in nouns):# (c.data == 'NP'):
	 			nc,nt = deepcopy(c),c
	 	root.children.remove(nt)
	 	# Keep the tag of the root and update all other things # root.tag not <- nc.tag
	 	root.data, root.children, root.phrase,root.head = nc.data, nc.children, nc.phrase, nc.head
	 	return root
	# Default
	return root

# def augment(root):
# 	if(root.data =='PP'):
# 		root = augment_PP(root)

root = vt.root

prepcfg(root,0)
# vt.prepcfg(root,0)
