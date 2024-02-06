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
    var secid = document.getElementById('jsonData').getAttribute('secid')
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        animation: false,
        xAxis: [
            {
                type: 'category',
                data: data.categoryData,
                boundaryGap: false,
                minorTick: {
                    show: true
                },
                minorSplitLine: {
                    show: true
                },
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                },
                boundaryGap: ['20%', '20%'],
            },
        ],
        yAxis: [
            {
                scale: true,
                boundaryGap: ['20%', '5%'],
                minorTick: {
                    show: true
                },
                minorSplitLine: {
                    show: true
                },
            },
        ],
        series: [
            {
                name: secid,
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
                top: '92%',
                start: 50,
                end: 100
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
                },
            borderWidth: 0,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
            color: '#000'
            },
            backgroundColor: 'rgba(255, 255, 255, 0)',
            shadowColor: 'rgba(255, 255, 255, 0)',
            shadowBlur: 0,
            position: ['5%', '3%'],
            formatter: function(params) {
                var data = params[0].data; // Получаем данные из серии
                var date = params[0].name
                var special = ['<strong style="color: BLUE;">' + secid + ' </strong>: ', '<strong>Открытие: </strong>', ', <strong>Закрытие: </strong>',
                    ', <strong>Макс: </strong>', ', <strong>Мин: </strong>', ', <strong>Объем: </strong>', '<i>' + date + '</i> ']
                return special[0] + special[6] + special[1] + data[1] + special[2] + data[2] + special[3] + data[3] + special[4] + data[4] + special[5] + data[5] + " &#8381";
            }
        },
        grid: {
            left: '4%',
            right: '2%',
            top: '2%',
            bottom: '3%',
        },
    };

    option && myChart.setOption(option);
});
