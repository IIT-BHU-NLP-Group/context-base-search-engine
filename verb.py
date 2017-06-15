from nltk.stem import WordNetLemmatizer
from nltk.corpus import verbnet as vn

lemmatizer = WordNetLemmatizer()
verb = raw_input()
print verb
vs = [vn.vnclass(i) for i in vn.classids(verb)]
for v in vs:
	#print 'v:%s'%v
	frames = v.findall('FRAMES/FRAME')
	for i in frames:
		print vn.pprint_frame(i)
	
