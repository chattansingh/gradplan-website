from gradplan import *
from plantest import *
import json

#plans = getbaseplans()
#print json.dumps(plans[0]['plan'], indent=4)
#e = { 'days': ['Tu','Th'], 'times':[['09:00 AM'], ['09:00 AM']], 'taken':['MATH 150A']}
plan = json.loads(plan)
#plan['plan'] =  changeplan(plan, ['COMP 110', 'COMP 110L'])
#uncomment lines below to see example output for CS 
#print json.dumps(plan['plan'], indent=4)
e = { 'days': ['R'], 'times':[['0800h', '0900h', '1000h', '1100h', '1200h', '1300h', '1400h', '1500h', '1600h', '1700h']]}
plan['plan'][0]['classes'] = filtertimes(plan['plan'][0]['classes'], e)
print json.dumps(plan['plan'][0], indent=4)
# e = {'days':[], 'times':[], 'taken': []}
# a = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', e)
# print a
