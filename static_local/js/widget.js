// 通貨ペアを変更する
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
  let currentStudy = "Bollinger_SMA"; // 初期値
  let currentHeight = "600"; // 初期値，px
  const createWidget = (symbol, study, height) => {
    let studiesArray = [];
    if (study === "Ichimoku") {
      studiesArray = ["STD;Ichimoku%1Cloud"];
    } else if (study === "Bollinger_SMA") {
      studiesArray = ["STD;Bollinger_Bands", "STD;SMA"];
    }
    return new TradingView.widget({
      ...
      "height": height + "px",
      "symbol": symbol,
      "studies": studiesArray,
     ...
    });
  };
  let widget = createWidget(currentSymbol, currentStudy, currentHeight); // 初期ウィジェットの作成
</script>
*/

// symbolをプルダウンで選択されたものに変更する
document.getElementById('currencyPairSelect').addEventListener('change', (e) => {
  const selectedSymbol = e.target.value.replace('/', ':'); // OANDA/USDJPY -> OANDA:USDJPY
  if (selectedSymbol !== currentSymbol) {
    widget.remove(); // 古いウィジェットを削除
    widget = createWidget(selectedSymbol, currentStudy, currentHeight); // 新しいウィジェットを作成
    currentSymbol = selectedSymbol;
  }
});

// indicatorをプルダウンで選択されたものに変更する
document.getElementById('indicatorSelect').addEventListener('change', (e) => {
  const selectedStudy = e.target.value;
  if (selectedStudy !== currentStudy) {
    widget.remove(); // 古いウィジェットを削除
    widget = createWidget(currentSymbol, selectedStudy, currentHeight); // 新しいウィジェットを作成
    currentStudy = selectedStudy;
  }
});

// ウィジェットの高さを変更する
// htmlに以下の記述があることを前提とする
// <div class="tradingview-widget-container" id="tradingview-container">
//  <!-- TradingViewウィジェットのコンテンツ -->
// </div>
// <div id="resizer" style="height: 10px; background: #ccc; cursor: ns-resize;"></div>

document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('tradingview-widget-container');
  const resizer = document.getElementById('resizer');

  resizer.addEventListener('mousedown', initDrag, false);

  let startY, startHeight;

  function initDrag(e) {
    startY = e.clientY;
    startHeight = parseInt(window.getComputedStyle(container).height, 10);
    document.documentElement.addEventListener('mousemove', doDrag, false);
    document.documentElement.addEventListener('mouseup', stopDrag, false);
  }

  function doDrag(e) {
    currentHeight = startHeight + e.clientY - startY;
    container.style.height = currentHeight + 'px';
    // ウィジェットを再読み込みする
    widget.remove();
    widget = createWidget(currentSymbol, currentStudy, currentHeight);
  }

  function stopDrag() {
    document.documentElement.removeEventListener('mousemove', doDrag, false);
    document.documentElement.removeEventListener('mouseup', stopDrag, false);
  }
});
