<template>
    <div class="chart-container">
      <div class="one_title title">{{ title }}</div>
      <div :id="chartId" :style="{ width: chartWidth, height: chartHeight }"></div>
    </div>
  </template>
  
  
<script setup lang="ts">
import { ref, onMounted, nextTick, reactive } from 'vue';
import * as echarts from 'echarts';
import 'echarts-gl';
import geoJson from "../stores/中华人民共和国.json"; //该文件路径改成自己项目中的文件路径即可
import { ar } from 'element-plus/es/locale';
import { color } from '../../echarts';


  const props = defineProps({
    title: String,
    chartId: String,
    chartWidth: String,
    chartHeight: String
  });

  onMounted(() => {
  initeCharts(option);
  initeCharts1(option1);
  initeCharts2(option2);
  initeCharts3(option3);
  initeCharts4(option4);
  chartMap();
});
const ad = ref();
const option = {
  title: {
   
    text: '',
    left: 'left', // 设置标题水平居中
    top: 'top', // 设置标题在顶部
    textStyle: {
      color: '#FFFAFA', // 设置title的文字为白色
      fontsize: 20,
      
      
    }
  },
  legend: {
    data: ['国盈', '股份制'],
    left: 'left', // 设置图例在右侧  
    textStyle: {
      color: '#FFFAFA' // 设置图例文字颜色为白色
    }
  },
  radar: {
    // shape: 'circle',
    center: ['40%', '48%'], // 设置雷达图的中心位置
    radius: '70%', // 设置雷达图的半径
    indicator: [
      { name: '安徽', max: 500, color: '#FFFAFA' },
      { name: '北京', max: 500, color: '#FFFAFA' },
      { name: '重庆', max: 500, color: '#FFFAFA' },
      { name: '福建', max: 500, color: '#FFFAFA' },
      { name: '甘肃', max: 500, color: '#FFFAFA' },
      { name: '广东', max: 500, color: '#FFFAFA' },
      {name: '广西', max: 500, color: '#FFFAFA'},
      {name: '贵州', max: 500, color: '#FFFAFA'},
      {name: '海南', max: 500, color: '#FFFAFA'},
      {name: '河北', max: 500, color: '#FFFAFA'},
      {name: '河南', max: 500, color: '#FFFAFA'},
      {name: '黑龙江', max: 500, color: '#FFFAFA'},
      {name: '湖北', max: 500, color: '#FFFAFA'},
      {name: '湖南', max: 500, color: '#FFFAFA'},
      {name: '吉林', max: 500, color: '#FFFAFA'},
      {name: '江苏', max: 500, color: '#FFFAFA'},
      {name: '江西', max: 500, color: '#FFFAFA'},
      {name: '辽宁', max: 500, color: '#FFFAFA'},
      {name: '内蒙古', max: 500, color: '#FFFAFA'},
      {name: '宁夏', max: 500, color: '#FFFAFA'},
      {name: '青海', max: 500, color: '#FFFAFA'},
      {name: '山东', max: 500, color: '#FFFAFA'},
      {name: '山西', max: 500, color: '#FFFAFA'},
      {name: '陕西', max: 500, color: '#FFFAFA'},
      {name: '上海', max: 500, color: '#FFFAFA'},
      {name: '四川', max: 500, color: '#FFFAFA'},
      {name: '天津', max: 500, color: '#FFFAFA'},
      {name: '西藏', max: 500, color: '#FFFAFA'},
      {name: '新疆', max: 500, color: '#FFFAFA'},
      {name: '云南', max: 500, color: '#FFFAFA'},
      {name: '浙江', max: 500, color: '#FFFAFA'}

      
    ],
    axisName: {
      color: '#FFFAFA', // 设置坐标轴标签文字的颜色
      fontSize: 12 // 设置坐标轴标签文字的大小
    }
  },
  series: [
    {
      
      type: 'radar',
      data: [
        {
          value: [473, 432, 456, 464, 475, 485, 403, 190, 462, 488, 487, 492, 485, 474, 471, 475, 472, 485, 138, 218, 474, 463, 479, 474, 494, 380, 122, 497, 447, 456, 447, 473, 432, 456, 464, 475, 485, 403, 190, 462, 488, 487, 492, 485, 474, 471, 475, 472],
          name: '国盈',
        },
        {
          areastyle: {
            color: 'rgba(255, 255, 255, 0.5)' // 设置区域颜色为半透明白色
          }
        },
        {
          value: [227, 268, 244, 214, 225, 215, 243, 245, 238, 212, 213, 228, 215, 226, 229, 225, 228, 215, 213, 223, 226, 237, 221, 226, 226, 236, 202, 23, 161, 244, 253, 227, 268, 244, 214, 225, 215, 243, 245, 238, 212, 213, 228, 215, 226, 229, 225, 228],
          name: '股份制',
        }
      ]
    }
  ]
};
const initeCharts = (option) => {
  let myChart = echarts.init(document.getElementById('ad'));
  // 绘制图表
  myChart.setOption(option);
}

const ad1 = ref()
const option1 = reactive({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)' // 修改提示框内容
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    textStyle: {
      color: '#fff' // 将图例名字颜色修改为白色
    }
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 214, name: '三甲医院',itemStyle: { color: '#6A5ACD' } },
        { value: 351, name: '二甲医院',itemStyle: { color: '#00FA9A' } },
        { value: 462, name: '普通医院',itemStyle: { color: '#ff0000' } }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      label: {
        color: '#fff', // 将标签颜色修改为白色
        formatter: '{b}:{d}%\n{c}', // 修改标签内容，将所占百分比和数值放在同一行
        lineHeight: 20 // 设置标签行高
      },
      labelLine: {
        length: 10, // 标签线长度
        length2: 15 // 标签线第二段长度
      }
    }
  ]
});
const initeCharts1 = (option1) => {
  let myChart1 = echarts.init(document.getElementById('ad1'));
  // 绘制图表
  myChart1.setOption(option1);
}

const ad2 = ref();
const option2 = reactive({
  legend: {
    data: ['数据'],
    textStyle: {
      color: '#fff' // 将图例名字颜色修改为白色
    }
  },
  xAxis: {
    type: 'category',
    data: ["5-6分","6-7分","7-8分","8-9分","9-10分"],
    axisLabel: {
      color: '#FFFAFA' // y 轴标签文字颜色
    },
  },
  yAxis: {
    type: 'value',
    max: 100,
    interval: 20,
    axisLabel: {
      color: '#FFFAFA' // y 轴标签文字颜色
      
    },
  },
  series: [
    {
      name: '数据',
      data: [100, 97.1, 93.5, 82.4, 38.4],
      type: 'bar',
      label: {
        show: true,
        position: 'top',
        color: '#fff',
        formatter: '{c}%'
      },
      itemStyle: {
      color: 'pink'
    }
    }
  ]
});
const initeCharts2 = (option2) => {
  let myChart2 = echarts.init(document.getElementById('ad2'));
  // 绘制图表
  myChart2.setOption(option2);
}

const ad3 = ref();
const option3 = reactive({
  legend: {
    data: ['数据'],
    textStyle: {
      color: '#fff' // 将图例名字颜色修改为白色
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    boundaryGap: [0, 0.01],
    min: 0, // 设置最小值为0
    max: 50, // 设置最大值为50
    interval: 10, // 设置刻度间隔为10
    axisLabel: {
      formatter: '{value}%' // 设置刻度标签格式为百分比
    },
    axisLine: {
      show: true, // 只显示 X 轴
      lineStyle: {
        color: '#fff' // 设置 X 轴颜色为白色
      }
    },
    splitLine:{
         show:false // 不显示网格线
    },
  },
  yAxis: {
    type: 'category',
    data: ['50岁以下', '50-59岁', '60-69岁', '70-79岁', '80岁及以上'],
    axisTick: {  
      show: false  
    },
    axisLine: {
      show: true, // 只显示 Y 轴
      lineStyle: {
        color: '#fff' // 设置 Y 轴颜色为白色
      }
    }
  },
  series: [
    {
      name: '数据',
      type: 'bar',
      data: [6.6, 14.7, 28.9, 33.2, 16.6],
      label: {
        show: true,
        position: 'right',
        color: '#fff',
        formatter: '{c}%'
      },
      itemStyle: {
        color: '#FFDAB9'
      }
    }
  ]
});
const initeCharts3 = (option3) => {
  let myChart3 = echarts.init(document.getElementById('ad3'));
  // 绘制图表
  myChart3.setOption(option3);
}

const ad4 = ref();
const option4 = reactive({
  tooltip: {
    trigger: 'item',
    position: 'left'
  },
  series: [
    {
      name: '阶段',
      type: 'graph',
      layout: 'none',
      symbolSize:100,
      roam: true,
      label: {
        show: true,
        fontSize: 10
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 10],
      edgeLabel: {
        fontSize: 20
      },
      data: [
        { name: '向小助手描述问题', x: 200, y: 400, itemStyle: { color: '#ff7f50' } },
        { name: '填写信息', x: 600, y: 400, itemStyle: { color: '#87cefa' } },
        { name: '获得就诊科室与医院信息', x: 1000, y: 400, itemStyle: { color: '#da70d6' } },
        { name: '可选择线上进行初诊', x: 1400, y: 400, itemStyle: { color: '#32cd32' } },
        { name: '可选择线下就诊', x: 1800, y: 400, itemStyle: { color: '#6495ed' } },
      ],
      links: [
        { source: '向小助手描述问题', target: '填写信息', lineStyle: { color: '#ff7f50' } },
        { source: '填写信息', target: '获得就诊科室与医院信息', lineStyle: { color: '#87cefa' } },
        { source: '获得就诊科室与医院信息', target: '可选择线上进行初诊', lineStyle: { color: '#da70d6' } },
        { source: '可选择线上进行初诊', target: '可选择线下就诊', lineStyle: { color: '#32cd32' } },
      ],
      lineStyle: {
        opacity: 0.9,
        width: 2,
        curveness: 0
      }
    }
  ]
});
  
const initeCharts4 = (option4) => {
  let myChart4 = echarts.init(document.getElementById('ad4'));
  // 绘制图表
  myChart4.setOption(option4);
}


const chartMap = () => {
  var myChart5 = echarts.init(document.getElementById("mapEchart"), null, {width: '600px', height: '300px'});
  // 重点：不要遗漏这句代码！！
  echarts.registerMap("china", geoJson);
  // 图表配置项
  let option5 = {
    tooltip: {
      show: true,
    },
    //热力图配置项
    visualMap: [
      {
        type: "continuous",
        text: ["医院数量"],
        calculable: true,
        max: 150,
        inPange: {
          color: ["#87aa66", "#eba438", "#d94d4c"],
        },
        textStyle: {
          color: '#fff' // 设置字体颜色为白色
        }
      },
    ],
    //3D地图配置项
    geo3D: {
      map: "china",
      roam: true,
      left: '1px',
      itemStyle: {
        color: "#007aff",
        opacity: 0.8,
        borderWidth: 0.4,
        borderColor: "#000",
        // areaColor: '#fff'
      },
      viewControl: {
        autoRotate: true,
        autoRotateAfterStill: 3,
        distance: 60,
        minAlpha: 5, // 上下旋转的最小 alpha 值。即视角能旋转到达最上面的角度。[ default: 5 ]
        maxAlpha: 90, // 上下旋转的最大 alpha 值。即视角能旋转到达最下面的角度。[ default: 90 ]
        minBeta: -180, // 左右旋转的最小 beta 值。即视角能旋转到达最左的角度。[ default: -80 ]
        maxBeta: 360, // 左右旋转的最大 beta 值。即视角能旋转到达最右的角度。[ default: 80 ]
        animation: true, // 是否开启动画。[ default: true ]
        animationDurationUpdate: 1000, // 过渡动画的时长。[ default: 1000 ]
        animationEasingUpdate: "cubicInOut", // 过渡动画的缓动效果。[ default: cubicInOut ]
      },

      emphasis: {
        disabled: true, //是否可以被选中
        label: {
          //移入时的高亮文本
          show: true,
          color: "#333", //显示字体颜色变淡
          fontSize: 18, //显示字体变大
        },
        itemStyle: {
          color: "#ff7aff", //显示移入的区块变粉色
        },
      },
      label: {
        show: true,
        position: "top",
        color: "#111", //地图初始化区域字体颜色
        fontSize: 14,
        lineHeight: 16,
      },
      shading: "lambert",
      light: {
        //光照阴影
        main: {
          // color: "#fff", //光照颜色
          intensity: 1, //光照强度
          //shadowQuality: 'high', //阴影亮度
          shadow: true, //是否显示阴影
          shadowQuality: "medium", //阴影质量 ultra //阴影亮度
          alpha: 55,
          beta: 10,
        },
        ambient: {
          intensity: 0.7,
        },
      },
    },
    series: [
    //3D柱状图配置项
      {
        name: "医院数量分布",
        type: "bar3D",
        coordinateSystem: "geo3D",
        barSize: 3,
        shading: "lambert",
        opacity: 1,
        bevelSize: 0.2,
        label: {
          show: false,
          formatter: "{a}",
        },
        //自定义的data数组 value中数组的含义:[杭州的经度or纬度，要展示的3d柱状图数值大小]
        //3d柱状图配置 上海市医院数量：500


//根据医院数量大小调整value值大小
        data: [
          { name: "北京", value: [116.407526, 39.90403,58] },
          { name: "天津", value: [117.200983, 39.084158,55] },
          { name: "上海", value: [121.473701, 31.230416,43] },
          { name: "重庆", value: [106.551643, 29.562849,25] },
          { name: "河北", value: [115.661434, 38.61384,64] },
          { name: "山西", value: [112.562398, 37.873532,25] },
          { name: "辽宁", value: [123.431475, 41.836175,96] },
          { name: "吉林", value: [125.32568, 43.897016,43] },
          { name: "黑龙江", value: [126.661665, 71] },
          { name: "江苏", value: [118.763232, 32.061707,76] },
          { name: "浙江", value: [120.152792, 30.267447,45] },
          { name: "安徽", value: [117.283042, 31.86119,36] },
          { name: "福建", value: [119.296494, 26.074507,29] },
          { name: "江西", value: [115.910043, 28.674209,36] },
          { name: "山东", value: [117.020359, 36.66853,84] },
          { name: "河南", value: [113.753394, 34.765869,60] },
          { name: "湖北", value: [114.298572, 30.584355,88] },
          { name: "湖南", value: [112.982279, 28.19409,50] },
          { name: "广东", value: [113.280637, 23.125178,102] },
          { name: "海南", value: [110.33119, 20.031971,11] },
          { name: "四川", value: [104.065735, 30.659462,34] },
          { name: "贵州", value: [106.713478, 26.578343,18] },
          { name: "云南", value: [102.710002, 25.045806,21] },
          { name: "陕西", value: [108.948024, 34.263161,42] },
          { name: "甘肃", value: [103.826308, 36.059421,19] },
          { name: "青海", value: [101.780268, 36.620939,16] },
          { name: "台湾", value: [121.509062, 25.044332,null] },
          { name: "内蒙古", value: [111.76629, 15] },
          { name: "广西", value: [108.320007, 22.82402,61] },
          { name: "西藏", value: [91.132212, 29.660361,5] },
          { name: "宁夏", value: [106.278179, 38.46637,5] },
          { name: "新疆", value: [87.627704, 43.793026,23] },
          { name: "香港", value: [114.173355, 22.320048,null] },
          { name: "澳门", value: [113.549088, 22.198951,null] }
        ],
      },
    ],
  };
  myChart5.setOption(option5);
  //让可视化地图跟随浏览器大小缩放
  window.addEventListener("resize", () => {
    echarts.resize();
  });
};

  </script>
  
  <style scoped>
  .chart-container {
    margin-bottom: 20px;
  }
  .chart-header {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .title {
    height: 4.3vh;
    font-size: 1rem;
    color: white;
    text-align: center;
    line-height: 4.3vh;
}
  </style>
  