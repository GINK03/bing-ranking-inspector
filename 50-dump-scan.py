import json

import re
term_index = json.load(open('term_index.json'))
index_term = {index:term for term, index in term_index.items()}

feat_freq = {}
for line in open('rank/dump.txt'):
  ms = re.findall(r'\[(.*?)\]', line.strip())
  ms = [re.search(r'(\d{1,})<', m).group(1) for m in ms if re.search(r'(\d{1,})<', m)]

  for f in ms:
    if feat_freq.get(f) is None:
      feat_freq[f] = 0
    feat_freq[f] += 1

for feat,freq in sorted(feat_freq.items(), key=lambda x:-x[1]):
  print(index_term[int(feat)], freq)
