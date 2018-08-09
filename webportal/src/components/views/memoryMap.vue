<template>
 <div style="width:100%;height:100%;" id="memory_map"></div>
</template>


<script>
  import echarts from 'echarts';

 const option = {
    title : {
      text: 'Memory',
      subtext: '',
      x:'center'
    },
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
      x : 'center',
      y : 'bottom',
      data:['usage','free','buff/cache']
    },
    toolbox: {
      show : true,
      feature : {
        mark : {show: false},
        dataView : {show: false, readOnly: true},//這個是右上角的圖標數據視圖的icon控制
        magicType : {
          show: true,
          type: ['pie', 'funnel']
        },
        restore : {show: false},//右上角存儲的控制
        saveAsImage : {show: false}//右上角控制
      }
    },
    calculable : false,
    series : [
      {
        name:'Memory',
        type:'pie',
        radius : [20, 50],
        center : ['50%', '50%'],
        roseType : 'area',
        data:[
          {value:10, name:'usage'},
          {value:5, name:'free'},
          {value:15, name:'buff/cache'},

        ]
      }
    ]
  };

  export default {
        name: "memoryMap",
    mounted () {
      let memoryMap = echarts.init(document.getElementById('memory_map'));
      memoryMap.setOption(option);

      window.addEventListener('resize', function () {
        memoryMap.resize();
      });
    }
    }
</script>

<style scoped>

</style>
