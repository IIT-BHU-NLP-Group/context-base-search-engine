import pickle as pk
SM = None
if(False):
	import spacy
	nlp = spacy.load('en')
	verbList = []
	with open('new_verb_count_result.csv','r')as f:
		for l in f:
			verbList.append(l.split(',')[1].strip())
	vl = list(enumerate(verbList))
	vl_dict = dict()
	for i in vl:
		vl_dict[i[0]] = i[1]#.decode('utf-8')
	# print vl_dict

	SM = [[0.0 for i in xrange(len(vl))] for j in xrange(len(vl))] # Similarity Metric
	for a in xrange(len(vl)):
		print a
		for b in xrange(len(vl)):
			A = vl_dict[a]
			B = vl_dict[b]
			SM[a][b] = nlp(u'%s'%A).similarity(nlp(u'%s'%B))
	
	f = open('pickled-data','w')
	pk.dump(SM,f)
	f.close()
else:
	f = open('pickled-data','r')
	SM = pk.load(f)
	f.close()
if(False):
	import matplotlib.pyplot as plt
	from matplotlib import cm
	import numpy as np
	SMa = np.array(SM)
	fig,ax = plt.subplots()
	cax = ax.imshow(SMa, interpolation='nearest', cmap=cm.coolwarm)
	cbar = fig.colorbar(cax, ticks=[0,0.5, 1])
	cbar.ax.set_yticklabels(['< 0', '0.5', '> 1'])  # vertically oriented colorbar
	plt.show()
if(True):
	verbList = []
	with open('new_verb_count_result.csv','r')as f:
		for l in f:
			verbList.append(l.split(',')[1].strip())
	vl = list(enumerate(verbList))
	vl_dict = dict()
	for i in vl:
		vl_dict[i[0]] = i[1]
	for a in xrange(len(vl)):
		for b in xrange(a+1,len(vl)):
			if(SM[a][b])>0.4:
				print vl_dict[a],vl_dict[b], SM[a][b]


