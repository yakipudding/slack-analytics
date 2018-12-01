# slack-analytics

## 環境
- Python3.X
- pandas

## 使い方
1. Slackからログをダウンロードする（設定と権限＞データのインポート／エクスポート）
2. dataフォルダを作成し、1を解凍したものを置く
3. createMasterCsv.pyを実行
4. createTalkCsv.pyを実行

## createMasterCsv.py
channels.json、users.jsonからcsv作成
- output
	- channels.csv
	- users.csv

## createTalkCsv.py
チャンネルごと日付ごとのログからメッセージ、リアクション、メンションcsvを作成
- output
	- talk.csv
	- reaction.csv
	- mention.csv
	- チャンネル名ディレクトリ
		- talk.csv
		- reaction.csv
		- mention.csv

### メッセージ
|channel_id|talk_id|talk_user|text|
|:--|:--|:--|:--|
|C5XXXXXXX|XX1|U9XXXXXXX|`<@U8YYYYYYY>`こんにちは|
|C5XXXXXXX|XX2|U8YYYYYYY|帰りたい|
|C5XXXXXXX|XX3|U9XXXXXXX|しごおわ|

### リアクション
|channel_id|talk_id|talk_user|reaction_user|emoji|
|:--|:--|:--|:--|:--|
|C5XXXXXXX|XX1|U9XXXXXXX|U8YYYYYYY|ok_woman|
|C5XXXXXXX|XX1|U9XXXXXXX|U7ZZZZZZZ|iine|
|C5XXXXXXX|XX2|U8YYYYYYY|U9XXXXXXX|wakaru|
|C5XXXXXXX|XX2|U9XXXXXXX|U7ZZZZZZZ|otukare|

### メンション
|channel_id|talk_id|talk_user|mention_user|
|:--|:--|:--|:--|
|C5XXXXXXX|XX1|U9XXXXXXX|U8YYYYYYY|

