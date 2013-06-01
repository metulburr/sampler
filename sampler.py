

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import glob
import webbrowser
import re

PAGES = 2 #number of pages to scan

def main(mainurl):
	
	byter = urllib.request.urlopen(mainurl)
	html = byter.read().decode()
	soup = BeautifulSoup(html)
	content = soup.find('div', {"class": "content-main"})
	sections = content.find_all('div', {"class": re.compile('post-')})

	for add in sections:
		title = add.find('h2',{'class','entry-title'}).text
		status = add.find('span', {'class':'cat-links'}).text.strip()
		for p in add.findAll('p'):
			lister = p.findAll('a')
			for index in lister:
				if index.text in ['Click here', 'click here', 'Click Here']: #updated to add caps/lowercase, possible bug by doing so to get funky links and comments
					link = index['href']
					comment = p.text
					
		#check for existance
		try:
			type(link)
		except UnboundLocalError:
			link = 'Could not find link'
			
		try:
			type(comment)
		except UnboundLocalError:
			comment = 'Could not find comment'
		
		#excludes
		if 'expired' in status: #exclude expired
			continue
		elif 'Amazon Deal:' in title: #exclude Amazon deals
			continue
		elif 'when you purchase' in comment: #exclude freebies/cheaper with purchase
			continue
		else:
			print('TITLE: {}'.format(title))
			print('STATUS: {}'.format(status))
			print('LINK: {}'.format(link))
			print('COMMENT: {}'.format(comment))
			print('\n' + ('-'*25) + '\n') #spacer
			
			savefile(title,status,link,comment)
			
def savefile(t, s, l, c):
	filename = 'samplestuff.txt'
	f = open(filename,'a')
	f.write('TITLE: {}\n'.format(t))
	f.write('STATUS: {}\n'.format(s))
	f.write('LINK: {}\n'.format(l))
	f.write('COMMENT: {}\n'.format(c))
	f.write('\n' + ('-'*25) + '\n')
	f.close()

#iterate over pages
for num in range(1,PAGES + 1):
	url = 'http://www.samplestuff.com/page/{}/'.format(num)
	main(url)


