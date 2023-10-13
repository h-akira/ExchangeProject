// htmlに以下の記述があることを前提とする
/*
<select id="currencyPairSelect">
  <option value="OANDA/USDJPY" selected>USDJPY</option>
  <option value="OANDA/EURJPY">EURJPY</option>
  <option value="OANDA/EURUSD">EURUSD</option>
  <option value="OANDA/AUDJPY">AUDJPY</option>
  <option value="OANDA/GBPJPY">GBPJPY</option>
</select> 
<script type="text/javascript">
  let currentSymbol = "OANDA:USDJPY"; // 初期値
  const createWidget = (symbol) => {
    return new TradingView.widget({
      ...
      "symbol": symbol,
     ...
    });
  };
  let widget = createWidget(currentSymbol); // 初期ウィジェットの作成
</script>
*/
// symbolをプルダウンで選択されたものに変更する
document.getElementById('currencyPairSelect').addEventListener('change', (e) => {
  const selectedSymbol = e.target.value.replace('/', ':'); // OANDA/USDJPY -> OANDA:USDJPY
  if (selectedSymbol !== currentSymbol) {
    widget.remove(); // 古いウィジェットを削除
    widget = createWidget(selectedSymbol); // 新しいウィジェットを作成
    currentSymbol = selectedSymbol;
  }
});

