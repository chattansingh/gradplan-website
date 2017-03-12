#first link is for metalab's bullshit api, the second link is to parse majors and road maps for our app

#http://curriculum.ptg.csun.edu
#http://catalog.csun.edu/programs/major

import re
import json
import urllib2 as ul
import requests
from bs4 import BeautifulSoup

classurl = 'http://curriculum.ptg.csun.edu/classes/'

# 403 is returned if we don't inlcude this shit
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def getpage(url):
  page = requests.get(url, headers=headers)
  data = BeautifulSoup(page.text, 'lxml')
  return data

def getclasses(url):
  data = getpage(url)
  data = json.loads(data.find('p').contents[0])
  return data['classes']

#TODO: get prereqs for each class

#this gets the list of roadmap links for the selected major.
# the road map is later used to construct a plan for the student
def getroadmaplinks(url):
  data = getpage(url)
  a = data.find_all('a', {'title': True})
  maplinks = []
  for i in a:
    if 'Degree Road Map for' in i['title']:
      maplinks.append({'major': i['title'][20:], 'link': i['href']})
  return maplinks

def timeconvert(t):
  hour = t[:2]
  minutes = t[2:4]
  setting = 'AM'
  if hour == '12':
    setting = 'PM'
  if int(hour) > 12:
    setting = 'PM'
    hour = str(int(hour) - 12)
  return hour + ':' + minutes + ' ' + setting

def compatible(c, s):
  return True

def filter(cl):
  meetings = cl['meetings'][0]
  start = timeconvert(meetings[u'start_time'])
  end = timeconvert(meetings['end_time'])
  result = {'course_id': cl['course_id'], 'start_time': start, 'end_time': end, 'days': meetings['days'], 'location': meetings['location']}
  return result

def suggested(data, schedule):
  s = {'course_id': [], 'start_time': [], 'end_time': [], 'days': [], 'location': []}
  for c in data:
    temp = filter(c)
    if compatible(temp, schedule):
      s['start_time'].append(temp['start_time'])
      s['end_time'].append(temp['end_time'])
      s['course_id'].append(temp['course_id'])
      s['location'].append(temp['location'])
      s['days'].append(temp['days'])
  return s

#this shit returns an array of arrays. Each array contains a class dictionary with the keys name and link
#basically, it returns the roadmap for the selected major
def getroadmap(url, schedule):
  #we eventually need to prompt user what degree they want (i.e. Accounting has more than 1 roadmap)
  links = getroadmaplinks(url)
  link = links[0]
  mappage = getpage(link['link'])
  tables = mappage.find_all('table', {'summary': True})
  bp = [] #beer pong! (jk it's base plan)
  first = 0

  for i in tables:
    c = i.find_all('td')
    sem = {'classes': []}

    for j in c:
      cl = j.find('a')

      if cl != None:
        t = cl.contents[0].split(' ') #cl['title'].split('.')
        dept = t[0]
        num = t[1]
        name = dept + ' ' + num
        link = ''
        classes = {'name': name}

        if dept != 'GE' and dept != 'Title':
          n = num
          if '/L' in num:
            n = num[:len(num)-2]

          link = classurl + dept.lower() + '-' + n

        if link != '' and first == 0:
          classes = getclasses(link)
          classes = suggested(classes, schedule)
          classes['name'] = name

        sem['classes'].append(classes) 
    if first == 0:
      first = 1
    bp.append(sem)
  return bp

a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', {})
print a
