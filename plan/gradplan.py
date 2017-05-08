#first link is for metalab's bullshit api, the second link is to parse majors and road maps for our app

#http://curriculum.ptg.csun.edu
#http://catalog.csun.edu/programs/major

#TODO: find a way to get prereqs for class

import re
import json
import urllib2 as ul
import requests
import datetime
from bs4 import BeautifulSoup

classurl = 'http://curriculum.ptg.csun.edu/classes/'
top = 'http://catalog.csun.edu/programs/major/'

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

def getmajors():
  data = getpage(top)
  m = []
  majors = data.find_all('a', {'class': 'dept-item'})
  for i in majors:
    temp = {}
    temp['major'] = i.contents[0].split('\t'*3)[0]
    temp['link'] = i['href']
    m.append(temp)
  return m

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

def getprereqs(url):
  data = getpage(url)
  em = data.find_all('em')
  prereqs = []
  for e in em:
    a = e.find_all('a', {'title':True})
    for i in a:
      title = i['title'].split('.')
      if len(title) > 1:
        num = title[0].split(' ')[1]
        if 'L' in num:
          prereqs.append(title[0][:len(title[0])-2])
          prereqs.append(title[0][:len(title[0])-2]+'L')
        else:
          prereqs.append(title[0])
  return prereqs

"""The function below generates a basic plan (no modifications) to store
   in a database for future reference. The plan is an array of semesters,
   each semester has a field called "classes". Each classes field is an
   array of individual classes. Each individual class has the fields dept,
   number and prereqs. The plan structure looks as follows:
   [
     { 'classes': [
	 {'dept'    : "COMP",
	  'number'  : "110",
          'prereqs' : [ "MATH 150", "COMP 108"]
         }
        ]
     }
   ]
"""

def genplan(url):
  data = getpage(url)
  tables = data.find_all('table', {'summary': True})
  plan = []
  first = True

  for t in tables:

    classes = t.find_all('td')
    sem = {'classes': []}
    for j in classes:
      c = j.find('a')
      #TODO: need to parse class description for prereq links to build graph
      if c != None:
	csplit = c.contents[0].split(' ')
	dept = csplit[0]
	num = csplit[1:]
	link = []
	prereqs = []

	if dept != 'GE' and dept != 'Title':
          prereqs = getprereqs(c['href'])
	  n = ''
          # check if the class has a lab associated with it
          # if so, add to separate classes to the semester (one lecture and one lab)
          print num
          if '\L' in num or '/L' in num or '/L' in ''.join(num) or '\L' in ''.join(num):
	    n = ''.join(num)[:len(num)-3]
	    link.append(classurl + dept.lower() + '-' + n)
	    link.append(classurl + dept.lower() + '-' + n + 'L')
          else:
            link.append(classurl + dept.lower() + '-' + ' '.join(num))

          if len(link) > 1:
            #add lecture and lab to semester instead of just lecture
            cl = {'dept': dept, 'number': ''.join(num)[:len(num)-3], 'prereqs': prereqs, 'link': link[0], 'details': ''}
            if first:
              cl['details'] = getclasses(link[0])
	    sem['classes'].append(cl)
	    cl = {'dept': dept, 'number': ''.join(num)[:len(num)-3]+'L', 'prereqs': prereqs, 'link': link[1], 'details': ''}
            if first:
              cl['details'] = getclasses(link[1])
	    sem['classes'].append(cl)

          if len(link) == 1:
	    cl = {'dept': dept, 'number': ''.join(num), 'prereqs': prereqs, 'link': link[0], 'details': ''}
            if first:
              cl['details'] = getclasses(link[0])
	    sem['classes'].append(cl)
        else:
          #we dont append a link here because it is a GE or title 5 class
          cl = {'dept': dept, 'number': ' '.join(num), 'prereqs': [], 'link': '', 'details': ''}
          sem['classes'].append(cl)
      if first:
        first = False

    plan.append(sem)
  return plan
	  
def getbaseplans():
  busy = {}
  now = datetime.datetime.now()
  #p = json.loads(plan['plan'])
  first = 0
  month, year = getSem()
  season = ''
  if month < 6:
    season = 'Spring'
  else:
    season = 'Fall'
  majors = getmajors()
  plans = []
  for m in majors:
    roadmaplink = getroadmaplinks(m['link'])
    if len(roadmaplink) > 0:
      roadmaplink = roadmaplink[0]['link']
      #plans.append({'major': m['major'], 'plan': json.dumps(genplan(roadmaplink))})
      p = genplan(roadmaplink)
      for i in range(len(p)):
        sem = p[i]['classes']
        if first == 0:
          first += 1
          p[i]['semester'] = season + '-' + str(year)
        else:
          if season == 'Fall':
            season = 'Spring'
            year += 1
          else:
            season = 'Fall'
          p[i]['semester'] = season + '-' + str(year)
        for j in range(len(sem)):
          cl = sem[j]
          if cl['link'] != '' and i == 0:
            #p[i]['classes'][j]['details'] = getclasses(cl['link'])
            print cl['link']
            if '/F' in cl['link']:
              cl['link'] = cl['link'][:len(cl['link'])-2] + cl['link'][len(cl['link'])-1]
            classes = getclasses(cl['link'])
            classes = suggested(classes, busy)
            p[i]['classes'][j]['details'] = classes
      plans.append({'major': m['major'], 'plan': p})
  return plans

def filtertimes(sem, busy):
  s = []
  for i in range(len(sem)):
    cl = sem[i]
    if cl['dept'] != 'GE' or cl['dept'] != 'Title' and cl['link'] != u'':
      classes = getclasses(cl['link'])
      classes = suggested(classes, busy)
      clcopy = cl
      clcopy['details'] = classes
      s.append(clcopy)
    else:
      s.append(cl)
  return s

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
  print cl
  c1 = cl[0]
  #c1 = cl[1]
  c2 = '    '
  if len(cl[0]) > 2:
    c2 = cl[0]
    c2 = c2[1]
  s1 = s[0][0][:2]
  s2 = s[0][0][2:]

  if 'Mo' not in c1 and 'Tu' not in c1 and 'Th' not in c1 and 'We' not in c1 and 'S' not in c1 and 'F' not in c1:
    c1 = c1.replace('M', 'Mo')
    c1 = c1.replace('T', 'Tu')
    c1 = c1.replace('R', 'Th')
    c1 = c1.replace('W', 'We')
    c2 = c1[2:]
    c1 = c1[:2]
  else:
    if 'S' not in c1 and 'F' not in c1:
      c2 = c1[2:]
      c1 = c1[:2]
  """if c1 == 'T':
    c1 = 'Tu'
  if c1 == 'M':
    c1 = 'Mo'
  if c2 == 'R':
    c2 = 'Th'
  if c2 == 'W':
    c2 = 'We'"""


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
  print c
  if s == {} or c['start_time'] == '':
    return True
  if inrange([c['days'], c['start_time'], c['end_time']], [s['days'], s['times']]):
    return False
  else:
    return True

def filter(cl):
  meetings = {'days': [], 'location': []}
  start = ''
  end = ''
  if len(cl['meetings']) > 0:
    meetings = cl['meetings'][0]
    start = timeconvert(meetings[u'start_time'])
    end = timeconvert(meetings['end_time'])
  result = {'course_id': cl['course_id'], 'start_time': start, 'end_time': end, 'days': meetings['days'], 'location': meetings['location']}
  return result

def suggested(data, schedule):
  s = {'course_id': [], 'start_time': [], 'end_time': [], 'days': [], 'location': [], 'details': data}
  for c in data:
    temp = filter(c)
    if compatible(temp, schedule):
      s['start_time'].append(temp['start_time'])
      s['end_time'].append(temp['end_time'])
      s['course_id'].append(temp['course_id'])
      s['location'].append(temp['location'])
      s['days'].append(temp['days'])
  return s

def getSem():
  now = datetime.datetime.now()
  return now.month, now.year

def meetsPrereqs(taken, cl):
  if cl['prereqs'] == []:
    return True
  for c in cl['prereqs']:
    if c not in taken:
      return False
  return True

# we pass in a plan to this func. it then gives suggested classes
# based off already taken classes and schedule
def changeplan(plan, taken):
  now = datetime.datetime.now()
  p = plan['plan']
  #plan['plan'] = p
  for i in range(len(p)):
    for j in p[i]['classes']:
      #check if class has been taken
      #find next class and replace it if so
      #be sure to replace the classes moved
      name = j['dept'] + ' ' + j['number']
      if name in taken:
        nextclass = {}
        for k in range(i, len(p)):
          s = len(p[k]['classes'])
          for h in p[k]['classes']:
            if meetsPrereqs(taken, h): #p[k]['classes'][h]):
              nextclass = h
              ind = -1
              for x in range(len(p[i]['classes'])):
                n = p[i]['classes'][x]['dept'] + ' ' + p[i]['classes'][x]['number']
                if name == n:
                  ind = x
              p[k]['classes'].remove(h)
              if nextclass != {}:
                p[i]['classes'][ind] = nextclass
              else:
                p[i]['classes'].remove(p[i]['classes'][ind])
                s -= 1
  #plan['plan'] = json.dumps(p)
  return p

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


def get_major_url(major):
  """if major == 'Computer Science':
    return 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
  elif major == 'Math (General)':
    return'http://catalog.csun.edu/academics/math/programs/ba-mathematics-i/general/'
  else:
    return 'http://catalog.csun.edu/academics/ece/programs/bs-electrical-engineering/'"""
  m = getmajors()
  for i in m:
    if i['major'] == major:
      return i['link']
    #return 'http://catalog.csun.edu/academics/ece/programs/bs-electrical-engineering/'

def format_gradplan(road_map):
    counter = 1
    year1 = []
    year2 = []
    year3 = []
    year4 = []

    for semester in road_map:
        if counter == 1 or counter == 2:
            year1.append(semester)
        elif counter == 3 or counter == 4:
            year2.append(semester)
        elif counter == 5 or counter == 6:
            year3.append(semester)
        elif counter == 7 or counter == 8:
            year4.append(semester)
        counter = counter + 1

    return {'year1':year1, 'year2':year2,'year3':year3, 'year4':year4}

def filtered_time(time_form):
    filtered_dictionary = {'days': [], 'times': []}

    # Time and Day filter
    monday = time_form.cleaned_data['monday']
    tuesday = time_form.cleaned_data['tuesday']
    wednesday = time_form.cleaned_data['wednesday']
    thursday = time_form.cleaned_data['thursday']
    friday = time_form.cleaned_data['friday']
    saturday = time_form.cleaned_data['saturday']

    if monday:
        filtered_dictionary['days'] = 'Mo'
        filtered_dictionary['times'].append([str(t) for t in monday])
    if tuesday:
        filtered_dictionary['days'] = 'Tu'
        filtered_dictionary['times'].append([str(t) for t in tuesday])
    if wednesday:
        filtered_dictionary['days'] = 'We'
        filtered_dictionary['times'].append([str(t) for t in wednesday])
    if thursday:
        filtered_dictionary['days'] = 'Th'
        filtered_dictionary['times'].append([str(t) for t in thursday])
    if friday:
        filtered_dictionary['days'] = 'Fr'
        filtered_dictionary['times'].append([str(t) for t in friday])
    if saturday:
        filtered_dictionary['days'] = 'Sa'
        filtered_dictionary['times'].append([str(t) for t in saturday])

    return filtered_dictionary


def get_class_info(url):
  response = ul.urlopen(url)
  return json.loads(response.read())
