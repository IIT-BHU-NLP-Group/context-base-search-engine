import os
from copy import deepcopy

def prepcfg(root,t):
	for j in xrange(t):
		print '\t',
	print '%s{%s}'%(root.data,root.phrase),
	if root.relation!=['']:
		print '<<%s>>'%(root.relation), 
	if root.tag!=set(['']):
	 	print '<%s>'%(root.tag),
	print '\n',

	if root.children==None:
		return
	t=t+1	
	for i in root.children:

		prepcfg(i,deepcopy(t))	


path_to_parser = '/home/krishnkant/Desktop/Semester 4/Artificial Intelligence Assignments/Lab6/stanford-parser-full-2016-10-31'
path_back_to_repo = '/media/krishnkant/ACCC5095CC505BA0/Users/Krishnakanth/git/context-base-search-engine'

os.chdir(path_to_parser)
sent = raw_input('Enter Sentence : ')

f = open('./data/testsent.txt','w')
f.write(sent)
f.close()

os.system('./lexparser.sh data/testsent.txt > output.txt')
f = open('./output.txt','r')
pcfg = ''
for line in f:
	if(line.strip()==''):
		break
	pcfg += line
f.close()

os.chdir(path_back_to_repo)
f = open('input.txt','w')
f.write(pcfg)
f.close()





import verb_tree as vtree

level = dict()
os.system('python final_graph.py > structure_output.txt')
f = open('structure_output.txt','r')
g = vtree.GraphNode('parent')
level[-1] = g
for line in f:
	l = line.strip().split('|')	
	g = vtree.GraphNode()
	for i in l:
		key,val = [j.strip() for j in i.split(':')]
		if(key == 'TAG'):
			g.tag = val.strip()
		if(key == 'PHRASE'):
			g.phrase = val.strip()
		if(key == 'HEAD'):
			g.head = val.strip()
		if(key == 'TAG'):
			g.tag = set([i.strip().strip('\'') for i in  val.strip()[5:-1].split(',')])
		if(key == 'RELATION'):
			g.relation = [i.strip().strip('\'') for i in val.strip()[1:-1].split(',')]
		if(key == 'LEVEL'):
			lvl = val.strip()
			# print lvl
			level[int(lvl)] = g
			level[int(lvl)-1].children.append(g)
			# if(lvl == 0):
			# 	print 'HELLO'
			# 	print level[-1].children

root = level[-1].children[0]
prepcfg(root,0)
f.close()








