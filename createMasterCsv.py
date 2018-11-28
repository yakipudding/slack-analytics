# channelsとusersのCSVを作成する
import pandas as pd
import json

files = ['channels','users']

for filename in files:
  with open('data/' + filename +'.json', 'r', encoding='utf-8') as f:
      d = json.loads(f.read())

  df = pd.io.json.json_normalize(d, sep='_')
  df.to_csv('output/' + filename +'.csv', encoding='utf_8_sig')
