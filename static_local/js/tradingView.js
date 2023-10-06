function fetchChartData() {
  fetch(FETCH_URL_DATA)
    .then(response => response.json())
    .then(data => {
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
const chart = LightweightCharts.createChart(document.getElementById('container'));

// add
chart.timeScale().applyOptions({
  timeVisible: true,
  secondsVisible: false,
});

// Create the Main Series (Candlesticks)
const mainSeries = chart.addCandlestickSeries();

// add
mainSeries.applyOptions({
  priceLineVisible: true,
  lastValueVisible: true
});

const sma1Series = chart.addLineSeries({
  color: '#B8860B',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const sma2Series = chart.addLineSeries({
  color: '#0000FF',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const sma3Series = chart.addLineSeries({
  color: '#FFD700',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const bbUp2Series = chart.addLineSeries({
  color: '#FF00FF',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const bbDown2Series = chart.addLineSeries({
  color: '#FF00FF',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const bbUp3Series = chart.addLineSeries({
  color: '#C71585',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
});

const bbDown3Series = chart.addLineSeries({
  color: '#C71585',
  lineWidth: 2,
  lastValueVisible: false,
  priceLineVisible: false,
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

// const dataSelect = document.getElementById('dataSelect');
// dataSelector.addEventListener('change', function() {
//   FETCH_URL_DATA = dataSelector.value;
//   fetchChartData();
// });
const currencyPairSelect = document.getElementById('currencyPairSelect');
const timeframeSelect = document.getElementById('timeframeSelect');
function updateFetchUrl() {
  const currencyPair = currencyPairSelect.value;
  const timeframe = timeframeSelect.value;
  FETCH_URL_DATA = `/api/get_data_by_date/${STR_DATE}/${currencyPair}/${timeframe}`;
  fetchChartData();
}
currencyPairSelect.addEventListener('change', updateFetchUrl);
timeframeSelect.addEventListener('change', updateFetchUrl);
