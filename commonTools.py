# channelごと日付ごとのファイルを取得してCSV作成
# ※createMasterCsvを実行してから行うこと
import os
import pandas as pd
import json
import glob
import csv
import re
import uuid

class CommonTools:
    def outputCsv(self, filename, header, contents):
        write_encoding = 'utf_8_sig' #excelとかで見るからbom付ける
        with open(filename + '.csv', 'w', encoding=write_encoding) as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            writer.writerows(contents)

    def convertTalkText(self, text, df_users):
        #df_usersのindexはuser_idにすること
        #emojiは変換しません
        repDict = {
            '<!here>': '`@here`',
            '<!channel>': '`@channel`'
        }
        #ユーザーメンションの置換
        mentions = re.findall('<@[0-9a-zA-Z_./?-]{9}>', text)
        for mention in mentions:
            mention_user = mention[2:-1]
            mention_user_name = df_users.at[mention_user,'display_name_custom']
            if mention_user not in repDict:
                repDict[mention] = '`@' + mention_user_name + '`'
        
        for key, value in repDict.items():
            text = text.replace(key, value)

        return text
        

