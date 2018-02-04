# ranking-specre

## 目的
spectre (ある複雑な量を単純な成分に分け、ある特定の量の大小によって分布を示したもの。)   

Intel CPUなどに内在する投機実行のspectreとは用法が違いますのでご注意ください。  

ランキングアルゴリズムは日々進化しています。Googleのサーチエンジンは[200以上の特徴量を用いたり](https://backlinko.com/google-ranking-factors)色々しています。  

これらはGoogleでないと手に入らない特徴量も多数存在しており、容易に、ユーザが最適化できるものではなかったりします  

わかりやすいものでは、ドメイン以内にコンテンツが十分に存在し、それがある程度参照されるものであれば、以前やったようにWelqさんのようにコンテンツの内容の是非によらず、ランクアップしてしまうような意図しない問題もございました。  


## お題
Rankingエンジンのランクの傾向を、検索クエリ結果から、ランキンされたサイトの自然言語的特徴から、獲得しようという意図です。  

これを行うにあたって２つの制約があります。  
- 1. ランキングエンジンのリバースエンジニアリングのような行為は認められるのか
- 2. すべての特徴量を用意することはできないので、自然言語的な特徴量で近似することはできないか


## ランキングアルゴリズム一覧
- lambdarank
- lambdamart

## 読むべき論文
- [From RankNet to LambdaRank to LambdaMART: An Overview](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf)

## よく見る評価指標
- [NDCG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain)

## 目的関数
- [PairWise(xgb)](https://github.com/dmlc/xgboost/tree/master/demo/rank)

## ranksvmフォーマット
資料が全くなく、調査して理解するまで結構かかりました。  
ranksvmフォーマットはgroup fileというのが別途必要になっている
<p align="center">
  <img width="550px" src="https://user-images.githubusercontent.com/4949982/35681621-45722bd0-07a1-11e8-9008-b10c1fdd3082.png">
</p>

## bingのデータクローン
- neologdで一般単語をとりだす
- bingでクエリを作成して、ひたすら大量に集める
- 1位=4, ２位=3, 3位=2, ４位=1で、単一ページでないドメイントップのサイトをランキングする  
- 言語処理的にtitle, meta, bodyの自然言語でランキングしてみる

(本当はこれ+DeepLearningでやってもいい)

## オペレーション

### ランククエリ生成
neologdなどからnoun（名詞）を取り出して、それを検索クエリ群にする  
```python
import glob
import pickle                                                                                                                                                                                                     import json                                                                                                                                                                                        nouns = []
for name in glob.glob('mecab-ipadic-neologd/build/*/*.csv'):
   f = open(name)
   for line in f:
     ents = line.strip().split(',')
     if '名詞' not in ents:
       continue
     term = ents[0]
     nouns.append(term)
open('nouns.json', 'w').write( json.dumps(nouns, indent=2, ensure_ascii=False) )
```

#### bingをスクレイピング
```console
$ python3 scrape.py
```

#### フルドメインが入っているリンクをパース
```console
$ python3 scan_pair.py
```

#### bingの結果からフルドメインをスクレイピング
```console
$ python3 pair_scrape.py
```
#### フルドメインのHTMLをパース
```console
$ python3 10-parse-htmls.py
```
#### 分かち書きして特徴量化
```console
$ python3 20-make-vector.py
```
#### 疎行列で表現してranksvm形式のファイルを出力
```console
$ python3 30-index.py
```
