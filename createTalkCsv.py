# channelごと日付ごとのファイルを取得してCSV作成
# ※createMasterCsvを実行してから行うこと
import os
import pandas as pd
import json
import glob
import csv
channels = pd.read_csv('output/channels.csv', encoding='utf_8_sig')['name']

talk_cols = ['client_msg_id', 'ts', 'thread_ts', 'user','text','date']
# talk/reactions/users
reaction_cols = ['client_msg_id','talk_user','user','name']
# talk/text <@user>
mention_cols = ['client_msg_id','talk_user','mention_user']

for channel in channels:
    # 日付ごとのjsonファイル一覧を取得
    datefiles = glob.glob('data/' + channel + '/*.json')

    talks = []
    df_talk = pd.DataFrame(index=[], columns=talk_cols)
    df_reaction = pd.DataFrame(index=[], columns=reaction_cols)
    df_mention = pd.DataFrame(index=[], columns=mention_cols)

    for datefile in datefiles:
        # 日付ファイル取得
        df = pd.read_json(datefile, encoding='utf-8')
        
        # 日付列追加
        date = os.path.splitext(os.path.basename(datefile))[0]
        df['date'] = date

        # talk
        # 要素がない場合は追加
        if not 'subtype' in df.columns:
            df['subtype'] = ""
        if not 'client_msg_id' in df.columns:
            df['client_msg_id'] = ""
        if not 'thread_ts' in df.columns:
            df['thread_ts'] = ""

        # チャンネル参加を削除
        df = df[df['subtype'] != 'channel_join']

        # reaction
        if 'reactions' in df.columns:
            # name/users/user
            reactions = df['reactions']
            
        
        
        df_talk = pd.concat([df_talk,df[talk_cols]], ignore_index=True)




    df_talk.to_csv('output/channel/' + channel +'.csv', encoding='utf_8_sig')
    # df_talk.to_csv('output/channel/' + channel +'.csv', encoding='utf_8_sig')
    # with open('output/channel/' + channel +'.csv', 'w', encoding='utf_8_sig') as f:
    #     writer = csv.writer(f, lineterminator='\n')
    #     writer.writerow(talk_cols)
    #     writer.writerows(talks)

    # reactions
    # mention -> textから <@uid>を取る