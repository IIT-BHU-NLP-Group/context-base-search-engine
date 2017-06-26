from nltk.stem import WordNetLemmatizer
from nltk.corpus import verbnet as vn
import sys

# verb = sys.argv[1]
lemmatizer = WordNetLemmatizer()
# verb = raw_input('enter verb')

with open('verb_count_result.csv','r') as f:
	for line in f:
		verb = line.strip().split(',')[1]
		if('/'in verb):
			verb = verb.replace('/','-')
		print verb
		vs = [vn.vnclass(i) for i in vn.classids(verb)]
		with open ('Aug-Verbnet/%s.txt'%(verb),'w') as vf:  # Augmented Verbnet
			for v in vs:
				frames = v.findall('FRAMES/FRAME')
				for i in frames:
					vf.write(vn.pprint_frame(i)+'\n')
					# print vn.pprint_frame(i)

		