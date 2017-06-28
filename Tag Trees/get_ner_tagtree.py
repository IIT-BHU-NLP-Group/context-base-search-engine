import math
def get_ontology_by_level():
	f_ont = open('ontology.txt','r')
	ont = []
	for line in f_ont:
		l = line.strip().split()
		# print l
		if len(l)==2:		
			if(len(l[1].strip().split(':')) == 2 ):
				ont.append( [ l[1].strip().split(':')[1] , l[0].count('.')] )
			else:
				ont.append( [ l[1].strip() , l[0].count('.')] )
	f_ont.close()
	return ont
if __name__ == '__main__':
	for i in get_ontology_by_level():
		print i[1]*'\t', i[0]
