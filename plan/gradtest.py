from gradplan import *
import json

plans = getbaseplans()
print json.dumps(json.loads(plans[0]['plan']), indent=4)
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
#changeplan(plans[0], [], {})
#uncomment lines below to see example output for CS
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
# e = {'days':[], 'times':[], 'taken': []}
# a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
# print a
