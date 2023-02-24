# e-license

e-license.jpのシステムを用いている教習所で技能予約に空き時間ができた場合通知してくれるシステムです。（現時点ではmacOSにのみ対応。）



![スクリーンショット 2023-02-24 12.09.32](https://i.imgur.com/ap1MlGm.png)



## Install

### packageのインストール

このレポジトリをCloneしたディレクトリの直下で以下のコマンドを実行してください。

```
pip install -r requirements.txt
```



### terminal-notifierのインストール

```
brew install terminal-notifier
```



### .envファイルの作成

このレポジトリをCloneしたディレクトリの直下に `.env` という名称のファイルを作成してください。

 `.env` ファイル内には以下の3つを記載してください

- ELICENSE_USERNAME：ユーザー名
- ELICENSE_PASSWORD：パスワード
- ELICENSE_LOGIN：ログインページのURL

```
ELICENSE_USERNAME="xxxxx"
ELICENSE_PASSWORD="xxxxx"
ELICENSE_LOGIN="https://www.e-license.jp/xxxxxx/xxxxxx"
```



### cronの設定

このコマンドを自動実行するためにcrontabを設定します。詳細は `crontab` で検索してください。

#### 設定の例

##### 8時から23時までの間、10分ごとに確認

```
*/10 8-23 * * * path/to/python path/to/e-license/main.py 2>&1 
```

##### 30分ごとに確認

```
*/30 * * * * path/to/python path/to/e-license/main.py 2>&1 
```



## 動かない時

- 直接 `main.py` を実行してエラーを確認してください。
- Chromeのバージョンが最新か確認してください。
- macOS以外はサポートしていません。
- Pythonのバージョンが3.9以上であるかを確認してください。
- cronの設定では python への絶対パスを指定してください。
- cronの設定では `main.py` への絶対パスを指定してください。





