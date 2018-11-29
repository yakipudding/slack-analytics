# channelごと日付ごとのファイルを取得してCSV作成
# ※createMasterCsvを実行してから行うこと
import os
import pandas as pd
import json
import glob
import csv
import re
channels = pd.read_csv('output/channels.csv', encoding='utf_8_sig')

talk_cols = ['channel_id', 'client_msg_id', 'ts', 'thread_ts', 'user', 'text', 'date']
talk_cols_norequire = ['subtype', 'client_msg_id', 'thread_ts', 'reactions']
# talk/reactions/users
reaction_cols = ['channel_id', 'client_msg_id', 'ts', 'talk_user', 'reaction_user', 'emoji']
# talk/text <@user>
mention_cols = ['channel_id', 'client_msg_id', 'ts', 'talk_user', 'mention_user']

# 初期化
talk_reactions_all = []
talk_mentions_all = []
df_talk_all = pd.DataFrame(index=[], columns=talk_cols)
df_reaction_all = pd.DataFrame(index=[], columns=reaction_cols)
df_mention_all = pd.DataFrame(index=[], columns=mention_cols)

for index, channel in channels.iterrows():
    channel_id = channel['id']
    channel_name = channel['name']

    # 日付ごとのjsonファイル一覧を取得
    datefiles = glob.glob('data/' + channel_name + '/*.json')

    # 初期化
    talk_reactions = []
    talk_mentions = []
    df_talk = pd.DataFrame(index=[], columns=talk_cols)
    df_reaction = pd.DataFrame(index=[], columns=reaction_cols)
    df_mention = pd.DataFrame(index=[], columns=mention_cols)

    for datefile in datefiles:
        # 日付ファイル取得 + 欠損値補完
        df = pd.read_json(datefile, encoding='utf-8').fillna("")
        
        # channel_id追加
        df['channel_id'] = channel_id

        # 日付列追加
        date = os.path.splitext(os.path.basename(datefile))[0]
        df['date'] = date

        # 要素がない場合は追加
        for col in talk_cols_norequire: 
            if not col in df.columns:
                df[col] = ""

        # チャンネル参加を削除
        df = df[df['subtype'] != 'channel_join']

        # talk
        df_talk = pd.concat([df_talk,df[talk_cols]], ignore_index=True)

        # 1行ずつ
        for index, row in df.iterrows():
            talk_user = row['user']
            client_msg_id = row['client_msg_id']
            ts = row['ts']

            # reaction
            if row['reactions'] is not "":
                reactions = row['reactions']
                # name/users/user
                for reaction in reactions:
                    emoji = reaction['name']
                    users = reaction['users']
                    for user in users:
                        talk_reaction = [ channel_id, client_msg_id, ts, talk_user ,user ,emoji ]
                        talk_reactions.append(talk_reaction)
                        talk_reactions_all.append(talk_reaction)
        
            # mention
            mentions = re.findall('<@[0-9a-zA-Z_./?-]{9}>', row['text'])
            for mention in mentions:
                mention_user = mention[2:-1]
                talk_mention = [channel_id, client_msg_id, ts, talk_user, mention_user]
                talk_mentions.append(talk_mention)
                talk_mentions_all.append(talk_mention)

    df_talk_all = pd.concat([df_talk_all,df_talk], ignore_index=True)

    df_talk.to_csv('output/channel/' + channel_name +'.csv', encoding='utf_8_sig')
    with open('output/channel/' + channel_name +'_reaction.csv', 'w', encoding='utf_8_sig') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(reaction_cols)
        writer.writerows(talk_reactions)

    with open('output/channel/' + channel_name +'_mention.csv', 'w', encoding='utf_8_sig') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(mention_cols)
        writer.writerows(talk_mentions)


df_talk_all.to_csv('output/talk_all.csv', encoding='utf_8_sig')
with open('output/talk_reaction_all.csv', 'w', encoding='utf_8_sig') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(reaction_cols)
    writer.writerows(talk_reactions_all)

with open('output/talk_mention_all.csv', 'w', encoding='utf_8_sig') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(mention_cols)
    writer.writerows(talk_mentions_all)