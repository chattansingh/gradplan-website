#first link is for metalab's bullshit api, the second link is to parse majors and road maps for our app

#http://curriculum.ptg.csun.edu
#http://catalog.csun.edu/programs/major

#TODO: find a way to get prereqs for class. Make a better compatibility function

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

def splittime(t):
  h = t[:2]
  m = t[2:4]
  setting = t[5:]
  return [h, m, setting]

def check(t1, t2):
  print t1[0] + '==' + t2[0]
  print t1[0] == t2[0]
  print t1[2] + '==' + t2[2]
  print t1[2] == t2[2]
  if t1[0] == t2[0] and t1[2] == t2[2]:
    return True
  else:
    return False

def checktime(cl, day):
  result = False
  for t in day:
    start = splittime(cl[1])
    end = splittime(cl[2])
    busy = splittime(t)
    print cl[1] + '-' + cl[2] + ' ' + t
    print check(start, busy)
    print check(end, busy)
    if check(start, busy) or check(end, busy):
      result = True

  return result

def inrange(cl, s):
  if s[0] == []:
    return False
  c1 = cl[0]
  c1 = cl[1]
  c2 = '    '
  if len(cl[0]) > 2:
    c2 = cl[0]
    c2 = c2[1]
  s1 = s[0][0][:2]
  s2 = s[0][0][2:]

  if c1 == 'T':
    c1 = 'Tu'
  if c1 == 'M':
    c1 = 'Mo'
  if c2 == 'R':
    c2 = 'Th'
  if c2 == 'W':
    c2 = 'We'

  if c1 in s[0]:
    day = s[0].index(c1)
    busy = s[1][day]
    return checktime(cl, busy)
  elif c2 in s[0]:
    day = s[0].index(c2)
    busy = s[1][day]
    return checktime(cl, busy)
  else:
    return False

#this function is supposed to determine compatability of a class
#i.e. has the user taken this class and is it in their schedule range?
def compatible(c, s):
  if inrange([c['days'], c['start_time'], c['end_time']], [s['days'], s['times']]):
    return False
  else:
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

"""
the following function expects a url to the catalog majro page and
a schedule dictionary in the following format:
{
  'days': ['Sun', 'M', 'T',...'Sat'],          <------------Array of Days that they are busy

  'times': [                                   <------------Array of Arrays. Each array contains strings with the hour that hey are busy
             ['9:00 AM', '10:00 AM',...],
             ['6:00 PM', '7:00 PM', ...], 
           ],
  'taken': [ '152873', '168458', ...]          <------------Array of class id's
}

leave any of the fields as an empty array if there is no user input
i.e. 'times': [] means they are free all everyday
ONLY PASS IN DAYS AND TIMES THAT THEY ARE BUSY
"""
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
        link = []
        classes = {'name': name}

        if dept != 'GE' and dept != 'Title':
          n = num
          if '/L' in num:
            n = num[:len(num)-2]

          link.append( classurl + dept.lower() + '-' + n)
          link.append( classurl + dept.lower() + '-' + n + 'L')

        if link != [] and first == 0:
          classes = getclasses(link[0])
          classes = suggested(classes, schedule)
          classes['name'] = name
        sem['classes'].append(classes)
        """if classes['name'] in schedule['taken']:
          sem['classes'].append({})
        elif first == 0:
          sem['classes'].append(classes)
        else:
          #check previous semester for empty classes
          #if empty, add current class to previous semester
          presem = bp[len(bp)-1]['classes']
          for i in range(len(presem)):
            if presem[i] == {}:
              bp[len(bp)-1]['classes'][i] = classes
              sem['classes'].append({})
            else:
              sem['classes'].append(classes) 
         """
    for i in range(len(sem['classes'])):
      if sem['classes'][i]['name'] in schedule['taken']:
        sem['classes'][i] = {}

    if first == 0:
      first = 1
    else:
      prevsem = bp[len(bp)-1]['classes']

      for i in range(len(prevsem)):
        if prevsem[i] == {}:
          for j in range(len(sem['classes'])):
            if sem['classes'][j] != {}:
              bp[len(bp)-1]['classes'][i] = sem['classes'][j]
              sem['classes'][j] = {} 
              break
    bp.append(sem)
  return bp

#uncomment lines below to see example output for CS
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
e = {'days':[], 'times':[], 'taken': []}
a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
print a
