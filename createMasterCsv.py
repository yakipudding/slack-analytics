# channelsとusersのCSVを作成する
import pandas as pd
import json

files = ['channels','users']

for filename in files:
  with open('data/' + filename +'.json', 'r', encoding='utf-8') as f:
      d = json.loads(f.read())

  df = pd.io.json.json_normalize(d, sep='_')
  if filename == 'users':
    df['display_name_custom'] = ""
    
    for index, row in df.iterrows():
        display_name_custom = row['name'] if row['profile_display_name_normalized'] == "" else row['profile_display_name_normalized']
        print(display_name_custom)
        df.at[index, 'display_name_custom'] = display_name_custom

  df.to_csv('output/' + filename +'.csv', encoding='utf_8_sig')
