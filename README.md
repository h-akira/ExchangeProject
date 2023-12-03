# ExchangeProject
## 概要
本リポジトリは
[FX-Note](https://github.com/h-akira/FX-Note)の分割した後継リポジトリの一つであり，
Djangoを用いて為替関係の情報の取りまとめや振り返り
ができるWebアプリケーションを開発しているものである．
無料取得可能な為替関連データで商用利用可能等なものが多くはないため，
現段階で一般公開は想定せず個人または身内内での利用を前提として開発している．

## 機能
実装済み
- ホーム
  - ウィジェットが貼ってあり最新の情報等を確認できる
- カレンダー・日記
  - 経済指標発表時刻等を表示
  - 各日付をクリックすると各日付の日記のページに推移
  - 日記の横にはその日の値動きのチャートが表示される

未実装
- リンク
  - 外部サイトへのリンクを追加や削除ができる

## データ取得
為替関連データ取得は
原則として管理者がPythonスクリプトを実行することで行い，
さらにそれをデータベースに反映するためにもPythonスクリプトを実行する必要がある．
しかし，前者はWebスクレイピングを伴うため別ディレクトリに置いて非公開とし，
後者のみ本リポジトリ内のディレクトリ`bin`に配置している．
- `bin/rate_csv2django.py`
- `bin/events_json2django.py`

なお，レートに関しては1分足も含めて`pandas_datareader`でYahoo Finenceから
取得可能であるため，
データベースにデータが無いときは
代わりにYahoo Financeのデータを用いる．

## 関連リポジトリ
- https://github.com/h-akira/FX-Note
- https://github.com/h-akira/PrivateChart
- https://github.com/h-akira/ExchangeData
