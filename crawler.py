from google import search
from bs4 import BeautifulSoup 
import urllib2
import ssl
import regex
import pickle

# This restores the same behavior as before.
context = ssl._create_unverified_context()

 # 
cities = ['London', 'Barcelona', 'Paris', 'Vatican city', 'Agra', 'Jaipur', 'Banglore', 'Gangtok','Varanasi' , 'Kanpur', 'Goa', 'Nainital', 'Mathura', 'New York', 'Tokyo', 'Darjiling', 'Manali', 'Kullu', 'Ujjain', 'Mumbai', 'Amritsar', 'ooty']
search_queries = ['All about'+ q for q in cities]
search_urls = []
files = ['1'+city+'.txt' for city in cities]

for q in search_queries:
	urls = []
	for u in search(q,lang='en', num=20, stop = 20):
		urls.append(u)
		print u 
	search_urls.append(urls)

for i in xrange(len(search_urls)):
	city = cities[i]
	urls = search_urls[i]
	text = ""
	print "crawling :%s...."%(city)
	for u in urls:
		print '*********************************',u,'**********************************'
		req = urllib2.Request(u)
		try:
			page = urllib2.urlopen(req,context = context).read()
		except Exception,e:
			continue
		soup = BeautifulSoup(page)
		for para in soup.findAll('p'):
			temp = para.getText().encode('utf-8')
			text = text + temp
	with open(files[i],'w') as fw, open(files[i],'r') as fr, open(cities[i],'w')as pfw , open(cities[i],'r')as pfr:
		text = regex.sub(r'\[\d+\]',' ',text)
		# text = regex.sub(r'\(\w+.*\)',' ',text)
		text = regex.sub(r'\<.*\>',' ',text)
		text = regex.sub(r'[,""]',' ',text)
		# text = '.'.join([s.strip() for s in text.strip().split('.')])
		fw.write(text)


