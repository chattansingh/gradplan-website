import json

fname = 'plan.txt'
content = ''
with open(fname) as f:
    content = f.readlines()

plan = ''.join(content).replace('\n', '')
