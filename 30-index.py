import json

from collections import Counter

wakatis = json.loads(open("wakatis.json").read())

query_data = {}
for obj in wakatis:
  type = obj["type"]
  term = obj["term"]

  if type == "1":
    rank = 4
  elif type == "2":
    rank = 2
  else:
    rank = 0
  wakati = dict(Counter(obj["wakati"]))
  if query_data.get(term) is None:
    query_data[term] = []
  query_data[term].append( (rank, wakati) )

term_index = {}
for query, data in query_data.items():
  for rank, wakati in data:
    for term, freq in wakati.items():
      if term_index.get(term) is None:
        term_index[term] = 0
      term_index[term] += 1

open("term_index.json", "w").write( json.dumps(term_index, indent=2, ensure_ascii=False) )

fdata = open("./rank/train.data", "w")
fgroup = open("./rank/train.group", "w")

for query, data in query_data.items():
  size = len(data)
  fgroup.write( '%d\n'%(size) )
  for rank, wakati in data:
    line = " ".join( ["%d:%d"%(term_index[term], freq) for term, freq in wakati.items()] )
    print(rank, line)
    fdata.write( str(rank) + " " + line + "\n" )
