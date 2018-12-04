# Jupyter Notebookでネットワーク図を出力します
# createTalkCsvを先に実行していること

#%%
import collections
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# 発言量が多い順
talks_count = collections.Counter(pd.read_csv('output/talk.csv', encoding='utf_8_sig')['talk_user']).most_common()
df_mentions = pd.read_csv('output/mention.csv', encoding='utf_8_sig')
df_users = pd.read_csv('output/users.csv', encoding='utf_8_sig', index_col=3) #index:user_id

# ネットワーク図の作成
## ノードの生成：発言数で円を大きくする
G = nx.Graph()
G.add_nodes_from([(df_users.at[user,'display_name_custom'], {"count":count}) for user, count in talks_count])

## エッジの追加：メンション関係でエッジを追加する
for index, mention in df_mentions.iterrows():
    talk_user = df_users.at[mention['talk_user'],'display_name_custom']
    mention_user = df_users.at[mention['mention_user'],'display_name_custom']
    if not G.has_node(talk_user) or not G.has_node(mention_user):
        continue
    if G.has_edge(talk_user, mention_user):
        G[talk_user][mention_user]["weight"] += 1
    else:
        G.add_edge(talk_user, mention_user, weight=1)

# 描画
## グラフのサイズを定義
plt.figure(figsize=(15,15), facecolor='white')
## ノード間の反発力を定義。値が小さいほど密集する
pos = nx.spring_layout(G, k=1.5)

## ノードの大きさを調整
node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)]
## ノードのスタイルを定義
nx.draw_networkx_nodes(G, pos, node_color='#f50057', alpha=0.3, node_size=node_size)
nx.draw_networkx_labels(G, pos, fontsize=14, font_weight="bold", font_family='Yu Mincho')

## エッジの太さを調整
edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)]
## エッジのスタイル
nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='#f8bbd0', width=edge_width)

plt.axis('off')