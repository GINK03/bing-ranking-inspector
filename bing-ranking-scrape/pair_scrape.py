import pickle

import json

import requests

import concurrent.futures
term_data = pickle.loads(open('term_data.pkl', 'rb').read())

def _map(arg):
  term, data = arg
  try:
    print(term, data)
    top  = data[0]
    tail = data[1]
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    r = requests.get(top, headers=headers)
    r.encoding = r.apparent_encoding
    html = r.text
    open('htmls/{}_top'.format(term), 'w').write( html )
    
    r = requests.get(tail, headers=headers)
    r.encoding = r.apparent_encoding
    html = r.text
    open('htmls/{}_tail'.format(term), 'w').write( html )
  except Exception as ex:
    print(ex)

args = [(term, data) for term, data in term_data.items()]

with concurrent.futures.ProcessPoolExecutor(max_workers=128) as exe:
  exe.map(_map, args)
