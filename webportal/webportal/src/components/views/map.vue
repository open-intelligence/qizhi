<template>
    <div style="width:calc(100% - 10px);height:305px;" id="home_page_map"></div>
</template>

<script>
import echarts from 'echarts';
import geoData from '../../assets/js/get-geography-value.js';
export default {
    name: 'homeMap',
    props: {
        cityData: Array
    },
    mounted () {
        var convertData = function (data) {
            let res = [];
            let len = data.length;
            for (var i = 0; i < len; i++) {
                var geoCoord = geoData[data[i].name];
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value)
                    });
                }
            }
            return res;
        };

        var map = echarts.init(document.getElementById('home_page_map'));
        const chinaJson = require('../../assets/china.json');
        echarts.registerMap('china', chinaJson);
        map.setOption({
            backgroundColor: '#404a59',//'#FFF',
          title: {
            text: '随便写点啥把',
            subtext: 'data from PM25.in',
            sublink: 'http://www.pm25.in',
            left: 'center',
            textStyle: {
              color: '#fff'
            }
          },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        areaColor:'#323c48',// '#EFEFEF',
                        borderColor: '#111'// '#CCC'
                    },
                    emphasis: {
                        areaColor:  '#2a333d'//'#E5E5E5'
                    }
                }
            },
            grid: {
                top: 0,
                left: '2%',
                right: '2%',
                bottom: '0',
                containLabel: true
            },
            series: [{
                type: 'scatter',
                coordinateSystem: 'geo',
                data: convertData(this.cityData),
                symbolSize: function (val) {
                    return val[2] / 10;
                },
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'right',
                        show: false  //显示地名
                    },
                    emphasis: {
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#cc242d'
                    }
                }
            }]

        });
        window.addEventListener('resize', function () {
            map.resize();
        });
    }
};
</script>


