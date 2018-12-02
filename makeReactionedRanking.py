# 被リアクションランキングCSV作成
# ※createTalkCsvを実行してから行うこと
import pandas as pd
import csv
import collections

ranking = []
ranking_cols = ['channel_name', 'user_name', 'talk_text', 'count', 'reaction']

df_channels = pd.read_csv('output/channels.csv', encoding='utf_8_sig', index_col=3) #index:channel_id
df_users = pd.read_csv('output/users.csv', encoding='utf_8_sig', index_col=3) #index:user_id
df_talks = pd.read_csv('output/talk.csv', encoding='utf_8_sig', index_col=1) #index:talk_id
df_reaction = pd.read_csv('output/reaction.csv', encoding='utf_8_sig')
reaction_count = collections.Counter(df_reaction['talk_id']).most_common(50)

for (talk_id, count) in reaction_count:
    talk = df_talks.loc[talk_id]
    channel_name = df_channels.at[talk['channel_id'],'name']
    user_name = df_users.at[talk['talk_user'],'profile_display_name_normalized']
    talk_text = talk['text']

    reactions = df_reaction[df_reaction['talk_id'] == talk_id]
    reactions_count = collections.Counter(reactions['emoji']).most_common()
    reaction = ""

    for (emoji, emoji_count) in reactions_count:
        reaction = reaction + ":" + emoji + ": " + str(emoji_count) + "件 "
    ranking.append([channel_name, user_name, talk_text, count, reaction])

with open('output/reactionedRanking' + '.csv', 'w', encoding='utf_8_sig') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(ranking_cols)
    writer.writerows(ranking)