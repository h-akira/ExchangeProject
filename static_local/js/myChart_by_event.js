// Description: This file contains the code for the trading view chart.

// Get the date from the url 
function fetchChartData() {
  fetch(FETCH_URL_DATA)
    .then(response => response.json())
    .then(response => {
      const data = response.data;
      const source = response.source;
      document.getElementById('sourceDisplay').textContent = source;
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

// Fetch chart data
fetchChartData();

// Adding a window resize event handler to resize the chart when
// the window size changes.
window.addEventListener("resize", () => {
  const parentElement = document.getElementById('includeChart');
  const width = parentElement.clientWidth;
  chart.resize(width, 600);
});

// Add event listener to the date input
const currencyPairSelect = document.getElementById('currencyPairSelect');
const timeframeSelect = document.getElementById('timeframeSelect');
function updateFetchUrl() {
  const currencyPair = currencyPairSelect.value;
  const timeframe = timeframeSelect.value;
  FETCH_URL_DATA = `/api/get_data_by_event/${STR_ID}/${currencyPair}/${timeframe}`;
  fetchChartData();
}
currencyPairSelect.addEventListener('change', updateFetchUrl);
timeframeSelect.addEventListener('change', updateFetchUrl);

document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('container');
  const resizer = document.getElementById('resizer');

  resizer.addEventListener('mousedown', initDrag, false);

  let startY, startHeight;

  function initDrag(e) {
    startY = e.clientY;
    startHeight = parseInt(window.getComputedStyle(container).height, 10);

    document.documentElement.addEventListener('mousemove', doDrag, false);
    document.documentElement.addEventListener('mouseup', stopDrag, false);
  }

  // チャートのサイズ変更
  function doDrag(e) {
    let newHeight = startHeight + e.clientY - startY;
    container.style.height = newHeight + 'px';
    // チャートのサイズをコンテナの新しいサイズに合わせて更新
    chart.applyOptions({ height: newHeight });
  }

  function stopDrag() {
    document.documentElement.removeEventListener('mousemove', doDrag, false);
    document.documentElement.removeEventListener('mouseup', stopDrag, false);
  }
});



