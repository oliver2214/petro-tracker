const upColor = '#22884F';
const downColor = '#E9003A';

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

function splitData(rawData) {
  let categoryData = [];
  let values = [];
  let volumes = [];
  for (let i = 0; i < rawData.length; i++) {
    categoryData.push(rawData[i].splice(0, 1)[0]);
    values.push(rawData[i]);
    volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]);
  }
  return {
    categoryData: categoryData,
    values: values,
    volumes: volumes
  };
}

document.addEventListener('DOMContentLoaded', function () {
    var data = splitData(loadJson("#jsonData"));
    var chartDom = document.getElementById('candlestick_frame');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        animation: false,
        xAxis: [
            {
                type: 'category',
                data: data.categoryData,
                boundaryGap: false,
                axisLine: { onZero: false },
                splitLine: { show: false },
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                }
            },
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
        ],
        series: [
            {
                name: 'Dow-Jones index',
                type: 'candlestick',
                data: data.values,
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: undefined,
                    borderColor0: undefined
                }
            },
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0],
                start: 0,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0],
                type: 'slider',
                top: '85%',
                start: 98,
                end: 100
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
            type: 'cross'
            },
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
            color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
            const obj = {
                top: 10
            };
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj;
        }
      },
    };

    option && myChart.setOption(option);
});
