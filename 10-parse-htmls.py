import os

import glob

import bs4

import re
for name in glob.glob("bing-ranking-scrape/htmls/*"):
  term = re.search(r'htmls/(.*?)_', name).group(1)
  print(term)
