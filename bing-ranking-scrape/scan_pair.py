import glob

import os

import json

import re

import pickle

term_data = {}
for name in glob.glob('terms/*'):
  obj = json.loads( open(name).read() )

  obj = list(filter(lambda x: re.search(r'^.*?/$', x[3]) is not None and x[3].count('/') == 3, obj) )

  # print(len(obj))
  if len(obj) < 2:
    continue

  if len(obj) == 2:
    term = obj[0][0]
    r1url = obj[0][3]
    r1 = obj[0][1] 

    r2url = obj[-1][3]
    r2 = obj[-1][1]
    print(term, r1url, r2url, r1, r2)
    term_data[term] = (r1url, r2url, r1, r2)
  if len(obj) > 2:
    term = obj[0][0]
    r1url = obj[0][3]
    r1 = obj[0][1] 
    
    r2url = obj[1][3]
    r2 = obj[1][1] 

    r3url = obj[-1][3]
    r3 = obj[-1][1]

    print(term, r1url, r2url, r3url, r1, r2, r3)
    term_data[term] = (r1url, r2url, r3url, r1, r2, r3)

open('term_data.pkl', 'wb').write( pickle.dumps(term_data) )
