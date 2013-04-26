# -*- coding: utf-8 -*-
import urllib2
import csv
import re
import sqlite3
from bs4 import BeautifulSoup


class address_data(object):



address = "http://www.nolruwa.com/bbs/board.php?bo_table=A_sub01&wr_id=61&page=1" 
website = urllib2.urlopen(address) 
website_html = website.read() 
print (website_html)

title_index = website_html.find('상호')
phone_index = website_html.find('전화번호')

title_substring = website_html[title_index:phone_index-title_index]

match = re.search('<td>[.]+</td>', title_substring)
if (match):
	print (match)
	print (match.group()) 



# print (website_html)

# matches = sre.findall('<img .*src="?(.*?)"?', website_text) 

# dir = website_handle.geturl().rsplit('/',1)[0] 
# if (dir == "http:/"):
# 	dir = website_handle.geturl()


# soup.prettify()
# print soup.prettify()


# csvfile = csv.writer(open('eggs.csv', 'wb'))

# for page_num in range(1, 25):
# 	print (page_num)
# 	address = "http://www.hungryboarder.com/index.php?mid=Movie&listStyle=list&sort_index=voted_count&order_type=desc&page=%d" % page_num  #"http://www.hungryboarder.com/index.php?mid=Movie&listStyle=list"
# 	website = urllib2.urlopen(address) 
# 	website_html = website.read() 

# 	soup = BeautifulSoup(website_html)

# 	count = 0
# 	table_row = soup("tr", {'class' : ['bg1', 'bg2'] })
# 	for row in table_row:
# 		# print (row.td['class'][0])
# 		# print (row)
# 		for td in row.find_all('td'):
# 			# print (td['class'])
# 			# print (td)
# 			if td['class'][0] == u'title':
# 				entry = td
# 				# print (entry)

# 				if (entry.strong) :
# 					category = entry.strong.string.encode("utf-8")
# 				else:
# 					category = ""
# 					print (entry)

# 				title = entry.a.string.encode("utf-8")
# 				link = entry.a['href']
# 				link_match = re.search('document_srl=[0-9]+', link)
# 				link_url=""
# 				if (link_match):
# 					# print (link_match)
# 					link_url = link_match.group()
# 				# print (link_url)
# 			elif td['class'][0] == u'recommend':
# 				entry = td
# 				recommend = entry.string.encode("utf-8")
# 			elif td['class'][0] == u'date':
# 				entry = td
# 				date = entry.string.encode("utf-8")

# 		csvfile.writerow([category, link_url, recommend, date])
# 		count += 1

# 	print ("page row => %d" % count)

# csvfile.close()





#<td class="title"> 검색
# table = soup("td", {'class' : 'title' })
# for entry in table:
#      # print entry.strong.contents
#      print entry.strong.string.encode("utf-8")
#      print entry.a['href']
#      print entry.a.string.encode("utf-8")

     # for child in entry.contents:
     # table_soup = BeautifulSoup(entry.string)
     # table_content = table_soup("strong", {'class' : 'category'})
     # print(table_content[0])

     # for child in entry.children:
     # 	print(child)
     	# if child['class'] == "category":
     		# print child

     # try:
         # print entry.string
     # except AttributeError:
         # print 'No string'