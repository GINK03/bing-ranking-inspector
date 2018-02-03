import json

wakatis = json.load(open('./wakatis.json'))

feat_id = {}
for obj in wakatis:
  wakati = obj['wakati']
  for feat in wakati:
    if feat_id.get(feat) is None:
      feat_id[feat] = len(feat_id)

json.dump(feat_id, open('feat_id.json', 'w'), indent=2, ensure_ascii=False)
