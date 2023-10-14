function fetchChartData() {
  fetch(FETCH_URL_DATA)
    .then(response => response.json())
    .then(data => {
      const chartData = data.map(item => ({
        time: item.time,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
      }));

      // メインのデータをセット
      mainSeries.setData(chartData);

      // SMAを計算してセット
      const smaData = calculateSMA(chartData, 14); // 例: 14日の移動平均
      smaLine.setData(smaData);

      // ボリンジャーバンドを計算してセット
    //   const bandsData = calculateBollingerBands(chartData, 14, 2); // 例: 14日のボリンジャーバンドと2倍の標準偏差
    //   upperBandLine.setData(bandsData.map(d => ({ time: d.time, value: d.upper })));
    //   lowerBandLine.setData(bandsData.map(d => ({ time: d.time, value: d.lower })));
    });
}

function calculateSMA(data, windowSize) {
    let sma = [];
    for (let i = windowSize - 1; i < data.length; i++) {
        let sum = 0;
        for (let j = 0; j < windowSize; j++) {
            sum += data[i - j].close;
        }
        sma.push({ time: data[i].time, value: sum / windowSize });
    }
    return sma;
}

// 1. チャートの初期化
// const chart = LightweightCharts.createChart(document.getElementById('container'), { width: 800, height: 600 });
const chart = LightweightCharts.createChart(document.getElementById('container'), {
    width: 800,
    height: 600,
    markers: {
        visible: false,  // このオプションを追加
    },
    // crosshair: {
    //     vertLine: {
    //         visible: false,
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal, // この行を追加
        vertLine: {
            visible: true, // この行をtrueに変更
            labelVisible: true,
        },
        horzLine: {
            visible: true, // この行をtrueに変更
            labelVisible: true,
        },
    },
   // labelVisible: true  // このオプションを追加
   //      },
   //      horzLine: {
   //          visible: false,
   // labelVisible: true  // このオプションを追加
   //      },
   //  },
});

// 2. メインのシリーズと関連するラインシリーズの作成
const mainSeries = chart.addCandlestickSeries();
// const smaLine = chart.addLineSeries({ color: 'blue' }); // SMAのためのラインシリーズ
// const smaLine = chart.addLineSeries({
//     color: 'blue',
//     priceLineVisible: false,  // このオプションを追加
// });
// const upperBandLine = chart.addLineSeries({ color: 'red' }); // ボリンジャーバンドの上限ライン
// const lowerBandLine = chart.addLineSeries({ color: 'green' }); // ボリンジャーバンドの下限ライン
const smaLine = chart.addLineSeries({
    color: 'blue',
    lineWidth: 1,
    priceFormat: {
        type: 'volume',
        precision: 0
    },
    priceLineVisible: false,
    lastValueVisible: false,
    priceLineWidth: 1,
    priceLineStyle: 1,
    crosshairMarkerVisible: false,  // このオプションを追加
});

// 3. データの取得とセット
fetchChartData();

// 必要に応じて他のロジックやイベントリスナを追加





// const smaLine = chart.addLineSeries({ color: 'red' });
// smaLine.setData(calculateSMA(yourData, 14));  // 14日の移動平均。windowSizeを変更することで期間を調整可能。
//
// // Create the Lightweight Chart within the container element
// const chart = LightweightCharts.createChart(document.getElementById('container'));
//
// // add
// chart.timeScale().applyOptions({
//   timeVisible: true,
//   secondsVisible: false,
// });
//
// // Create the Main Series (Candlesticks)
// const mainSeries = chart.addCandlestickSeries();
//
// // add
// mainSeries.applyOptions({
//   priceLineVisible: true,
//   lastValueVisible: true
// });
//
// const sma1Series = chart.addLineSeries({
//   color: '#B8860B',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const sma2Series = chart.addLineSeries({
//   color: '#0000FF',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const sma3Series = chart.addLineSeries({
//   color: '#FFD700',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const bbUp2Series = chart.addLineSeries({
//   color: '#FF00FF',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const bbDown2Series = chart.addLineSeries({
//   color: '#FF00FF',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const bbUp3Series = chart.addLineSeries({
//   color: '#C71585',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// const bbDown3Series = chart.addLineSeries({
//   color: '#C71585',
//   lineWidth: 2,
//   lastValueVisible: false,
//   priceLineVisible: false,
// });
//
// // Fetch chart data
// fetchChartData();
//
// // Adding a window resize event handler to resize the chart when
// // the window size changes.
// window.addEventListener("resize", () => {
//   const parentElement = document.getElementById('includeChart');
//   const width = parentElement.clientWidth;
//   chart.resize(width, 600);
// });
//
// // const dataSelect = document.getElementById('dataSelect');
// // dataSelector.addEventListener('change', function() {
// //   FETCH_URL_DATA = dataSelector.value;
// //   fetchChartData();
// // });
// const currencyPairSelect = document.getElementById('currencyPairSelect');
// const timeframeSelect = document.getElementById('timeframeSelect');
// function updateFetchUrl() {
//   const currencyPair = currencyPairSelect.value;
//   const timeframe = timeframeSelect.value;
//   FETCH_URL_DATA = `/api/get_data_by_date/${STR_DATE}/${currencyPair}/${timeframe}`;
//   fetchChartData();
// }
// currencyPairSelect.addEventListener('change', updateFetchUrl);
// timeframeSelect.addEventListener('change', updateFetchUrl);
