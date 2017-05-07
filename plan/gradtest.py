from gradplan import *
from plantest import *
import json

#plans = getbaseplans()
#print json.dumps(plans[0]['plan'], indent=4)
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
plan = {'plan': plan}
changeplan(plan, ['MATH 150A', 'MATH 150B', 'COMP 110', 'COMP 110L'], {})
print plan
#uncomment lines below to see example output for CS
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
# e = {'days':[], 'times':[], 'taken': []}
# a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
# print a
