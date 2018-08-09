<template>
    <div style="width:100%;height:100%;" id="user_flow"></div>
</template>

<script>
import echarts from 'echarts';

const option = {
    tooltip: {
        formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
        {
            name: '入流量',
            type: 'gauge',
            min: 0,
            max: 100,
            detail: {
                formatter: '{value}%+',
                fontSize: 14,
                offsetCenter: [0, '50px']
            },
            data: [{value: 50, name: 'active GPUs(%)'}],
            center: ['50%', '50%'],  //圖形顯示的位置
            radius: '100%',//圓弧的半徑
            title: {
                offsetCenter: [0, '120px']  //后一個屬性表示標題顯示的位置
            },
            axisLine: {
                lineStyle: {
                    // color: [],
                    width: 20  //圓弧半徑
                }
            },
            splitLine: {
                length: 20  //中間的灰色間隔長度
            }
        },
    ]
};

export default {
    name: 'userFlow',
    mounted () {
        let userFlow = echarts.init(document.getElementById('user_flow'));
        option.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;  //設置的百分數，到時候胡通過api調取相應的數值
        // option.series[1].data[0].value = (Math.random() * 1000).toFixed(2) - 0;
        userFlow.setOption(option);

        window.addEventListener('resize', function () {
            userFlow.resize();
        });
    }
};
</script>
