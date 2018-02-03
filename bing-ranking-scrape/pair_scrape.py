import pickle

import json

import requests

import concurrent.futures

import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

term_data = pickle.loads(open('term_data.pkl', 'rb').read())

def _map(arg):
  term, data = arg
  try:
    if len(data) == 6:
      args = [(1, 0), (2, 1), (3, 2)]
    elif len(data) == 4:
      args = [(1, 0), (2, 1)]

    for rank, index in args:
      if os.path.exists(f'htmls/{term}_{rank}'):
        continue
      print(term, data)
      url = data[index]
      headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

      r = requests.get(url, headers=headers, verify=False)
      r.encoding = r.apparent_encoding
      html = r.text
      open(f'htmls/{term}_{rank}', 'w').write( html )
      
  except Exception as ex:
    print(ex)

args = [(term, data) for term, data in term_data.items()]

with concurrent.futures.ProcessPoolExecutor(max_workers=528) as exe:
  exe.map(_map, args)
