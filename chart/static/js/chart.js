// Description: This file contains the code for the trading view chart.
let widget;
let FETCH_URL_DATA;
let fetchFirst = true;


// Get the date from the url 
function fetchChartData() {
  fetch(FETCH_URL_DATA)
    .then(response => response.json())
    .then(response => {
      const data = response.data;
      const source = response.source;
      if (source == "Yahoo Finance") {  // apiの仕様
        document.getElementById('sourceDisplay').textContent = "Loaded from " + source;
        document.getElementById("container").style.display = "block";
      }else{
        document.getElementById('sourceDisplay').textContent = source;
        document.getElementById("container").style.display = "none";
        alert(source)
        // return alert(source);
      }
      mainSeries.setData(data.map(item => ({
        time: item.time,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
      })));
      sma1Series.setData(data.map(item => ({
        time: item.time,
        value: item.sma1,
      })));
      sma2Series.setData(data.map(item => ({
        time: item.time,
        value: item.sma2,
      })));
      sma3Series.setData(data.map(item => ({
        time: item.time,
        value: item.sma3,
      })));
      bbUp2Series.setData(data.map(item => ({
        time: item.time,
        value: item.bb_up_2,
      })));
      bbDown2Series.setData(data.map(item => ({
        time: item.time,
        value: item.bb_down_2,
      })));
      bbUp3Series.setData(data.map(item => ({
        time: item.time,
        value: item.bb_up_3,
      })));
      bbDown3Series.setData(data.map(item => ({
        time: item.time,
        value: item.bb_down_3,
      })));
    });
}

// Create the Lightweight Chart within the container element
const chart = LightweightCharts.createChart(document.getElementById('container'),{
  markers: {
    visible: false,
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal, 
    vertLine: {
      visible: true,
      labelVisible: true,
    },
    horzLine: {
      visible: true,
      labelVisible: true,
    },
  },
});

// add
chart.timeScale().applyOptions({
  timeVisible: true,
  secondsVisible: false,
});

// Create the Main Series (Candlesticks)
const mainSeries = chart.addCandlestickSeries();

const sma1Series = chart.addLineSeries({
  color: '#B8860B',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const sma2Series = chart.addLineSeries({
  color: '#0000FF',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const sma3Series = chart.addLineSeries({
  color: '#006400',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const bbUp2Series = chart.addLineSeries({
  color: '#FF00FF',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const bbDown2Series = chart.addLineSeries({
  color: '#FF00FF',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const bbUp3Series = chart.addLineSeries({
  color: '#C71585',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const bbDown3Series = chart.addLineSeries({
  color: '#C71585',
  lineWidth: 1,
  lastValueVisible: false,
  priceLineVisible: false,
  priceFormat: {
    type: 'volume',
    precision: 0
  },
  crosshairMarkerVisible: false,
});

const timeframeSelect = document.getElementById('timeframeSelect');

function updateFetchUrl() {
  document.getElementById('sourceDisplay').textContent = 'Now Loading';
  const timeframe = timeframeSelect.value;
  FETCH_URL_DATA = `/api/get_latest_data_by_yf/${currentSymbol}/${timeframe}`;
  fetchChartData();
}

timeframeSelect.addEventListener('change', updateFetchUrl);

if (currentSource == "yahoo finance") {
  FETCH_URL_DATA = "/api/get_latest_data_by_yf/"+currentSymbol+"/1D/";
  fetchFirst = false;
  document.getElementById("selectForTradinfview").style.display = "none";
  document.getElementById("selectForYahooFinance").style.display = "block";
  document.getElementById("tradingview-widget-container").style.display = "none";
  document.getElementById("container").style.display = "block";
  fetchChartData();
} else if (currentSource == "tradingview") {
  widget = createWidget(currentSymbol, currentStudy, currentHeight);
  document.getElementById("selectForTradinfview").style.display = "block";
  document.getElementById("selectForYahooFinance").style.display = "none";
  document.getElementById("tradingview-widget-container").style.display = "block";
  document.getElementById("container").style.display = "none";
} else {
  aleart("none");
  document.getElementById("selectForTradinfview").style.display = "none";
  document.getElementById("selectForYahooFinance").style.display = "none";
  document.getElementById("tradingview-widget-container").style.display = "none";
  document.getElementById("container").style.display = "none";
}

// symbolをプルダウンで選択されたものに変更する
document.getElementById('currencyPairSelect').addEventListener('change', (e) => {
  const selectedInfo = e.target.value.replace('/', ':'); // OANDA/USDJPY -> OANDA:USDJPY
  const [selectedSource, selectedSymbol] = selectedInfo.split(',');
  if (selectedSymbol != currentSymbol || selectedSource != currentSource) {
    if ( currentSource === 'tradingview'){
      widget.remove(); // 古いウィジェットを削除
    }
    currentSymbol = selectedSymbol;
    currentSource = selectedSource;
    if ( selectedSource == 'tradingview' ) {
      document.getElementById("selectForTradinfview").style.display = "block";
      document.getElementById("selectForYahooFinance").style.display = "none";
      document.getElementById("tradingview-widget-container").style.display = "block";
      document.getElementById("container").style.display = "none";
      widget = createWidget(selectedSymbol, currentStudy, currentHeight); // 新しいウィジェットを作成
    }else if ( selectedSource == 'yahoo finance' ) {
      document.getElementById("selectForTradinfview").style.display = "none";
      document.getElementById("selectForYahooFinance").style.display = "block";
      document.getElementById("tradingview-widget-container").style.display = "none";
      document.getElementById("container").style.display = "block";
      FETCH_URL_DATA = "/api/get_latest_data_by_yf/"+selectedSymbol+"/1D/";
      if (fetchFirst) {
        fetchFirst = false;
        fetchChartData();
      }else{
        updateFetchUrl();
      }
    }else{
      alert("none");
      console.error('invalid source');
    }
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
  const tradingviewContainer = document.getElementById('tradingview-widget-container');
  const yfContainer = document.getElementById('container');
  const resizer = document.getElementById('resizer');

  resizer.addEventListener('mousedown', initDrag, false);

  let startY, startHeight;

  function initDrag(e) {
    startY = e.clientY;
    if ( currentSource === 'tradingview' ) {
      startHeight = parseInt(window.getComputedStyle(tradingviewContainer).height, 10);
    }else if ( currentSource === 'yahoo finance' ) {
      startHeight = parseInt(window.getComputedStyle(yfContainer).height, 10);
    }else{
      console.error('invalid source');
    }
    document.documentElement.addEventListener('mousemove', doDrag, false);
    document.documentElement.addEventListener('mouseup', stopDrag, false);
  }

  function doDrag(e) {
    if ( currentSource === 'tradingview' ) {
      const currentHeight = startHeight + e.clientY - startY;
      tradingviewContainer.style.height = currentHeight + 'px';
      // ウィジェットを再読み込みする
      widget.remove();
      widget = createWidget(currentSymbol, currentStudy, currentHeight);
    }else if ( currentSource === 'yahoo finance' ) {
      let newHeight = startHeight + e.clientY - startY;
      container.style.height = newHeight + 'px';
      // チャートのサイズをコンテナの新しいサイズに合わせて更新
      chart.applyOptions({ height: newHeight });
    }else{
      console.error('invalid source');
    }
  }

  function stopDrag() {
    document.documentElement.removeEventListener('mousemove', doDrag, false);
    document.documentElement.removeEventListener('mouseup', stopDrag, false);
  }
});
