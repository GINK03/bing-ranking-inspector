import json

term_freq = json.loads( open('bing-ranking-scrape/term_freq.json').read() )

term_id = {}

for index, term in enumerate(term_freq.keys()):
  term_id[term] = index

open('term_id.json', 'w').write( json.dumps(term_id, indent=2, ensure_ascii=False) )
