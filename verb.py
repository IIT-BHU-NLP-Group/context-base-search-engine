from nltk.stem import WordNetLemmatizer
from nltk.corpus import verbnet as vn
import sys

verb = sys.argv[1]
lemmatizer = WordNetLemmatizer()
# verb = raw_input('enter verb')
verb = sys.argv[1]
print verb
vs = [vn.vnclass(i) for i in vn.classids(verb)]
for v in vs:
	#print 'v:%s'%v
	frames = v.findall('FRAMES/FRAME')
	for i in frames:
		print vn.pprint_frame(i)
	
