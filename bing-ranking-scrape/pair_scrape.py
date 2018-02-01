import pickle

import json

import requests

import concurrent.futures
term_data = pickle.loads(open('term_data.pkl', 'rb').read())

def _map(arg):
  term, data = arg
  try:
    print(term, data)

    if len(data) == 3:
      args = [(1, 0), (2, 1), (3, 0)]
    else:
      args = [(1, 0), (2, 1)]

    for rank, index in args:
      url = data[index]
      headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

      r = requests.get(url, headers=headers)
      r.encoding = r.apparent_encoding
      html = r.text
      open(f'htmls/{term}_{rank}', 'w').write( html )
      
  except Exception as ex:
    print(ex)

args = [(term, data) for term, data in term_data.items()]

with concurrent.futures.ProcessPoolExecutor(max_workers=128) as exe:
  exe.map(_map, args)
