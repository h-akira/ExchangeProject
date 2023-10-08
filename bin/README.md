# スクリプト
## `events_json2django.py`
### 概要
経済指標発表などのイベント情報をデータベースに追加する．
### 準備
以下のようなフォーマットでデータが記載されたJsonファイルを用意する．
```
[
  {
    "date": "2023-09-09",
    "time": "10:30",
    "country": "China",
    "importance": 2,
    "name": "消費者物価指数（前年比）",
    "previous": "-0.3％",
    "prediction": "+0.1％",
    "result": "+0.1％"
  },
  {
    "date": "2023-09-11",
    "time": "16:00",
    "country": "Turkey",
    "importance": 2,
    "name": "経常収支",
    "previous": "+6.7億USD ⇒ +6.5億USD",
    "prediction": "-45.0億USD",
    "result": "-54.7億USD"
  },
.
.
.
]
```
ただし，`country`は以下に含まれていないとその他に分類されてしまうので注意．
```
Japan
EU
USA
Germany
UK
France
Canada
Australia
NewZealand
Swiss
TurkeyChina
Mexico
```
### オプション
- `file`: 用意したJsonファイル
- `--encoding`：エンコーディング
- `-u`：ユーザーネームを指定
  - 指定した場合はそのユーザーにしか見えない
  - 指定しない場合はすべてのユーザーから見える
### 利用例
```
./events_json2django.py ../data/events/20231008015758.json
```

## `rate_csv2django.py`
### 概要
1分足の為替データをデータベースに追加する．
### 準備
GMOクリック証券からヒストリカルデータをダウンロードして
以下のようなディレクトリ構造で配置する
（`BASE_DIR/data`は`-i`オプションで指定すればこれに従わなくて良い）．
```
BASE_DIR(defined in settings.py)
  |-...
  |-data
    |-...
    |-rate
      |-USDJPY
      | |-202303
      | | |-USDJPY_20230301.csv
      | | |-USDJPY_20230302.csv
      | | |-USDJPY_20230303.csv
      | | |-...
      | |-202304
      | | |-...
      | |-202305
      |   |-...
      |-EURJPY
        |-...
```
### オプション
- `i`：起点となるディレクトリ
  - 指定しなかった場合は`settings.py`を読み`BASE_DIR/data/rate`が指定される
- `-s`：`2023-10-06`のような形式で日付を指定することでその日付以降のみ追加
- `p`：通貨ペアを複数指定できる．
  - デフォルトではUSDJPY，EURJPY，EURUSD，GBPJPY，AUDJPYが指定されている

### 利用例
```
./rate_csv2django.py -i ../data/rate -s 2023-10-06 -p USDJPY EURJPY 
```
