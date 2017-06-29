import spacy
nlp = spacy.load('en')
with open('new_verb_count_result.csv','r')as f:
	for l in f:
		print l 
