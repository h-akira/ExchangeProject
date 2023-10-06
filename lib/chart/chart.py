def resample(df, rule):
  # 1分足からN分足など変換する
  # ruluは5Tなど
  # NaNの行は削除されてしまうので他の行を追加している場合は注意
  df_old = df.copy()
  df["Open"] = df_old["Open"].resample(rule).first()
  df["High"] = df_old["High"].resample(rule).max()
  df["Low"] = df_old["Low"].resample(rule).min()
  df["Close"] = df_old["Close"].resample(rule).last()
  df = df.dropna(how="any")
  return df

# def add_BBands(df,period=20,nbdev=2,matype=0, name={"up":"bb_up", "middle":"bb_middle", "down":"bb_down"}):
#   # mplfinanceのデータフレームにボリンジャーバンドの列を追加する．
#   bb_up, bb_middle, bb_down = talib.BBANDS(numpy.array(df['Close']), timeperiod=period, nbdevup=nbdev, nbdevdn=nbdev, matype=matype)
#   df[name['up']]=bb_up
#   df[name['middle']]=bb_middle
#   df[name['down']]=bb_down
#   return df
#
# def add_SMA(df, period, name):
#   df[name]=talib.SMA(df["Close"], timeperiod=period)
#   return df

## GPT先生にtalibを使わないように仕様変更してもらう:
def add_BBands(df, period=20, nbdev=2, matype=0, name={"up":"bb_up", "middle":"bb_middle", "down":"bb_down"}):
  # 移動平均を計算
  df[name['middle']] = df['Close'].rolling(window=period).mean()
  # 標準偏差を計算
  rolling_std = df['Close'].rolling(window=period).std(ddof=0)
  # ボリンジャーバンドの上部と下部を計算
  df[name['up']] = df[name['middle']] + (rolling_std * nbdev)
  df[name['down']] = df[name['middle']] - (rolling_std * nbdev)
  return df

def add_SMA(df, period, name):
  # 移動平均を計算
  df[name] = df["Close"].rolling(window=period).mean()
  return df
