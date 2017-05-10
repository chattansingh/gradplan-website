from gradplan import *
from plantest import *
import json

#plans = getbaseplans()
#print json.dumps(plans[0]['plan'], indent=4)
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
plan = json.loads(plan)
print plan['plan']
plan['plan'] =  changeplan(plan, ['MATH 150A', 'MATH 150B', 'COMP 110', 'COMP 110L'])
#uncomment lines below to see example output for CS
print plan['plan']
e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
plan['plan'][0]['classes'] = filtertimes(plan['plan'][0]['classes'], e)
print json.dumps(plan['plan'], indent=4)
# e = {'days':[], 'times':[], 'taken': []}
# a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
# print a
