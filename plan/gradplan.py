#first link is for metalab's bullshit api, the second link is to parse majors and road maps for our app

#http://curriculum.ptg.csun.edu
#http://catalog.csun.edu/programs/major

import re
import json
import urllib2 as ul
import requests
from bs4 import BeautifulSoup

# 403 is returned if we don't inlcude this shit
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#TODO: gets a list of majors. this needs to be organized by colleges along with their links for the browse majors tab.
#      then we need to get the roadmap from selected major page and reorganize it for the user.

def getroadmap(url):
  page = requests.get(url,headers=headers)
  data = BeautifulSoup(page.text, 'lxml')
  d = data.find_all('a[title=Degree\sRoad\sMap\sFor]')
  for i in d:
    print i

getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science')
