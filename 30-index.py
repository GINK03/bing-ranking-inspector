import json

from collections import Counter

term_id = json.loads(open("term_id.json").read())
wakatis = json.loads(open("wakatis.json").read())

data = []
for obj in wakatis:
  type = obj["type"]
  term = obj["term"]

  if type == "top":
    rank = 4
  else:
    rank = 1
  wakati = dict(Counter(obj["wakati"]))
  data.append( (term, rank, wakati) )

term_index = {}
for term, rank, wakati in data:
  for term, freq in wakati.items():
    if term_index.get(term) is None:
      term_index[term] = 0
    term_index[term] += 1

open("term_index.json", "w").write( json.dumps(term_index, indent=2, ensure_ascii=False) )

g = open("./rank/train.data", "w")

query = set()
for term, rank, wakati in data:
  line = " ".join( ["%d:%d"%(term_index[term], freq) for term, freq in wakati.items()] )
  print(rank, line)
  g.write( str(rank) + " " + "qid:%d"%(term_id[term]) +  " " + line + "\n" )
