from gradplan import *

plans = getbaseplans()
for p in plans:
  print p
  print ''

#uncomment lines below to see example output for CS
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
# e = {'days':[], 'times':[], 'taken': []}
# a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
# print a
