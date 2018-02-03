import os

import glob

import bs4

import re

import json

import concurrent.futures
terms = set()
for name in glob.glob("bing-ranking-scrape/htmls/*"):
  term = re.search(r'htmls/(.*?)_', name).group(1)
  #print(term)
  terms.add( term )

def _map(arg):
  key, terms = arg

  objs = []
  for term in terms:
    for type in ["1", "2", "3"]:
      try:
        html = ( open('bing-ranking-scrape/htmls/{term}_{type}'.format(term=term, type=type)).read() )
      except Exception as ex:
        print(ex)
        continue 
      soup = bs4.BeautifulSoup( html, "lxml" )
      [s.extract() for s in soup('script')]
     
      obj = {}
      title = soup.title.text if soup.title else None
      print( title )
      obj["term"] = term
      obj["type"] = type
      obj["title"] = title
      desc,keywords = None,None
      for meta in soup.find_all("meta"):
        if meta.get("name") == "description":
          desc = meta.get("content")
        if meta.get("name") == "keywords":
          keywords = meta.get("content")
      obj["desc"] = desc
      obj["keywords"] = keywords

      obj["body"] = soup.find("body").text if soup.find("body") else None
      #print(body)
      objs.append(obj)
  return objs

args = {}
for index, term in enumerate(terms):
  key = index%16
  if args.get(key) is None:
    args[key] = []
  args[key].append(term)
args = [ (key,terms) for key,terms in args.items() ]

objs = []
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  for _objs in exe.map(_map, args):
    for obj in _objs:
      objs.append(obj)
open("entities.json", "w").write( json.dumps(objs, indent=2, ensure_ascii=False) )
