import json

import MeCab

import re
m = MeCab.Tagger("-Owakati")
objs = json.loads(open("entities.json").read())

wakatis = []
for obj in objs:
  o = {}
  o["type"] = obj["type"]
  o["wakati"] = []
  o["term"] = obj["term"]

  title = obj["title"] if obj["title"] else "none"

  _terms = [ "title:%s"%term for term in m.parse(title).strip().split() ]
  [o["wakati"].append(term) for term in _terms]

  keywords = obj["keywords"] if obj["keywords"] else "none"
  _terms = [ "keyword:%s"%term for term in re.split(r"[,|、]", m.parse(keywords).strip()) ]
  [o["wakati"].append(term) for term in _terms]
  
  body = obj["body"] if obj["body"] else "none"
  _terms = [ "body:%s"%term for term in m.parse(keywords).strip().split() ]
  [o["wakati"].append(term) for term in _terms]

  wakatis.append( o )

open("wakatis.json", "w").write( json.dumps(wakatis, indent=2, ensure_ascii=False) )
