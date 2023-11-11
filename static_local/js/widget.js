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
    widget = createWidget(selectedSymbol, currentStudy); // 新しいウィジェットを作成
    currentSymbol = selectedSymbol;
  }
});

document.getElementById('indicatorSelect').addEventListener('change', (e) => {
  const selectedStudy = e.target.value;
  if (selectedStudy !== currentStudy) {
    widget.remove(); // 古いウィジェットを削除
    widget = createWidget(currentSymbol, selectedStudy); // 新しいウィジェットを作成
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
    let newHeight = startHeight + e.clientY - startY;
    container.style.height = newHeight + 'px';
    // ウィジェットを再読み込みする
    widget.remove();
    widget = createWidget(currentSymbol, currentStudy, newHeight);
  }

  function stopDrag() {
    document.documentElement.removeEventListener('mousemove', doDrag, false);
    document.documentElement.removeEventListener('mouseup', stopDrag, false);
  }
});
