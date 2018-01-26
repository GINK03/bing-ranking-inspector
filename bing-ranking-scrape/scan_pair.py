import glob

import os

import json

import re

import pickle

term_data = {}
for name in glob.glob('terms/*'):
  obj = json.loads( open(name).read() )

  obj = list(filter(lambda x: re.search(r'^.*?/$', x[3]) is not None and x[3].count('/') == 3, obj) )
  try:
    term = obj[0][0]
    top = obj[0][3]
    r1 = obj[0][1] 

    tail = obj[-1][3]
    r2 = obj[-1][1]
    if top == tail:
      continue
    print(term, top, tail, r1, r2)
    term_data[term] = (top, tail, r1, r2)
  except Exception as ex:
    #os.remove(name)
    ...

open('term_data.pkl', 'wb').write( pickle.dumps(term_data) )
