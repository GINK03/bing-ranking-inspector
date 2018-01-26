import json

import requests

import urllib

import bs4, lxml

import pickle

import json

import os

import concurrent.futures
encode = urllib.parse.quote

term_freq = json.loads(open('./term_freq.json').read())

url = 'https://www.bing.com/search?q={}'

def _map(arr):
  key, terms = arr
  for term in terms:
    if os.path.exists('terms/{}.json'.format(term)) is True:  
      continue
    print(term, encode(term), freq)
    r = requests.get( url.format(encode(term)) )
    html = r.text
    soup = bs4.BeautifulSoup(html)

    data = []
    for index, h2 in enumerate(soup.find_all('h2')):
      page_name = h2.text
      if h2.find('a') is None:
        continue
      _url = h2.find('a').get('href')

      print(term, index, page_name, _url)
      data.append( (term, index, page_name, _url) )
    open('terms/{}.json'.format(term), 'w').write( json.dumps(data, indent=2, ensure_ascii=False) )

arrs = {}
for index, (term, freq) in enumerate(sorted(term_freq.items(), key=lambda x:x[1]*-1)):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append(term)
arrs = [(key, terms) for key, terms in arrs.items()]
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_map, arrs)
