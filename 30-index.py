import json

from collections import Counter
wakatis = json.loads(open("wakatis.json").read())

data = []
for obj in wakatis:
  type = obj["type"]
  
  if type == "top":
    rank = 4
  else:
    rank = 1
  wakati = dict(Counter(obj["wakati"]))
  data.append( (rank, wakati) )

term_index = {}
for rank, wakati in data:
  for term, freq in wakati.items():
    if term_index.get(term) is None:
      term_index[term] = 0
    term_index[term] += 1
open("term_index.json", "w").write( json.dumps(term_index, indent=2, ensure_ascii=False) )
for rank, wakati in data:
  line = " ".join( ["%d:%d"%(term_index[term], freq) for term, freq in wakati.items()] )
  print(rank, line)
