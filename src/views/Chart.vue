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
  nextTick(() => {
    if (props.chartId === 'ad') {
      initeCharts(option);
    } else if (props.chartId === 'ad1') {
      initeCharts1(option1);
    } else if (props.chartId === 'ad2') {
      initeCharts2(option2);
    } else if (props.chartId === 'ad3') {
      initeCharts3(option3);
    } else if (props.chartId === 'ad4') {
      initeCharts4(option4);
    } else if (props.chartId === 'mapEchart') {
      chartMap();
    } else if (props.chartId === 'left_down_echarts') {
      initLeftDownChart();
    } else if (props.chartId === 'right_down_echarts') {
      initRightDownChart();
    }
  });
});
const ad = ref();
const option = {
  title: {
    text: '',
    left: 'center',
    top: 'top',
    textStyle: {
      color: '#00ff88',
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  legend: {
    data: ['国营', '股份制'],
    left: 'center',
    bottom: '5%',
    orient: 'horizontal',
    textStyle: {
      color: '#ffffff',
      fontSize: 12
    },
    itemStyle: {
      borderColor: '#00ff88'
    }
  },
  radar: {
    shape: 'polygon',
    center: ['50%', '45%'],
    radius: '65%',
    splitNumber: 5,
    startAngle: 90,
    indicator: [
      { name: '北京', max: 500 },
      { name: '上海', max: 500 },
      { name: '广东', max: 500 },
      { name: '江苏', max: 500 },
      { name: '浙江', max: 500 },
      { name: '山东', max: 500 },
      { name: '河南', max: 500 },
      { name: '四川', max: 500 },
      { name: '湖北', max: 500 },
      { name: '湖南', max: 500 },
      { name: '河北', max: 500 },
      { name: '福建', max: 500 },
      { name: '安徽', max: 500 },
      { name: '辽宁', max: 500 },
      { name: '陕西', max: 500 },
      { name: '江西', max: 500 }
    ],
    axisName: {
      color: '#00ff88',
      fontSize: 10,
      fontWeight: 'bold',
      backgroundColor: 'rgba(0, 0, 0, 0.6)',
      borderRadius: 3,
      padding: [2, 4]
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(0, 255, 136, 0.3)',
        width: 1
      }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: [
          'rgba(0, 255, 136, 0.02)',
          'rgba(0, 255, 136, 0.05)',
          'rgba(0, 255, 136, 0.08)',
          'rgba(0, 255, 136, 0.12)',
          'rgba(0, 255, 136, 0.15)'
        ]
      }
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(0, 255, 136, 0.6)',
        width: 2
      }
    }
  },
  series: [
    {

      type: 'radar',
      data: [
        {
          value: [473, 432, 456, 464, 475, 485, 403, 190, 462, 488, 487, 492, 485, 474, 471, 475],
          name: '国营',
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: '#00ff88',
            borderColor: '#fff',
            borderWidth: 2
          },
          lineStyle: {
            color: '#00ff88',
            width: 3,
            type: 'solid'
          },
          areaStyle: {
            color: 'rgba(0, 255, 136, 0.25)'
          }
        },
        {
          value: [227, 268, 244, 214, 225, 215, 243, 245, 238, 212, 213, 228, 215, 226, 229, 225],
          name: '股份制',
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: '#4ecdc4',
            borderColor: '#fff',
            borderWidth: 2
          },
          lineStyle: {
            color: '#4ecdc4',
            width: 3,
            type: 'solid'
          },
          areaStyle: {
            color: 'rgba(78, 205, 196, 0.25)'
          }
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
    formatter: '{a} <br/>{b}: {c} ({d}%)',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderColor: '#00ff88',
    borderWidth: 1,
    textStyle: {
      color: '#fff'
    }
  },
  legend: {
    orient: 'horizontal',
    left: 'center',
    bottom: '5%',
    textStyle: {
      color: '#fff',
      fontSize: 12
    },
    itemStyle: {
      borderColor: '#00ff88'
    }
  },
  series: [
    {
      name: '医院分级',
      type: 'pie',
      radius: ['30%', '60%'],
      center: ['50%', '45%'],
      data: [
        {
          value: 214,
          name: '三甲医院',
          itemStyle: {
            color: '#00ff88',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          value: 351,
          name: '二甲医院',
          itemStyle: {
            color: '#4ecdc4',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          value: 462,
          name: '普通医院',
          itemStyle: {
            color: '#45b7d1',
            borderColor: '#fff',
            borderWidth: 2
          }
        }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 15,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 255, 136, 0.5)',
          borderColor: '#00ff88',
          borderWidth: 3
        },
        scale: true,
        scaleSize: 5
      },
      label: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
        formatter: '{b}\n{d}%',
        lineHeight: 16
      },
      labelLine: {
        length: 15,
        length2: 20,
        lineStyle: {
          color: '#00ff88'
        }
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
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderColor: '#00ff88',
    borderWidth: 1,
    textStyle: {
      color: '#fff'
    }
  },
  legend: {
    data: ['评分分布'],
    left: 'center',
    top: '5%',
    textStyle: {
      color: '#fff',
      fontSize: 12
    }
  },
  grid: {
    left: '10%',
    right: '10%',
    bottom: '15%',
    top: '20%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ["5-6分","6-7分","7-8分","8-9分","9-10分"],
    axisLabel: {
      color: '#00ff88',
      fontSize: 11,
      fontWeight: 'bold'
    },
    axisLine: {
      lineStyle: {
        color: '#00ff88'
      }
    },
    axisTick: {
      lineStyle: {
        color: '#00ff88'
      }
    }
  },
  yAxis: {
    type: 'value',
    max: 100,
    interval: 20,
    axisLabel: {
      color: '#00ff88',
      fontSize: 11,
      formatter: '{value}%'
    },
    axisLine: {
      lineStyle: {
        color: '#00ff88'
      }
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(0, 255, 136, 0.2)',
        type: 'dashed'
      }
    }
  },
  series: [
    {
      name: '评分分布',
      data: [100, 97.1, 93.5, 82.4, 38.4],
      type: 'bar',
      barWidth: '50%',
      label: {
        show: true,
        position: 'top',
        color: '#fff',
        fontSize: 11,
        fontWeight: 'bold',
        formatter: '{c}%'
      },
      itemStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: '#00ff88' },
            { offset: 1, color: '#4ecdc4' }
          ]
        },
        borderRadius: [4, 4, 0, 0]
      },
      emphasis: {
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#4ecdc4' },
              { offset: 1, color: '#00ff88' }
            ]
          }
        }
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
    data: ['年龄分布'],
    left: 'center',
    top: '5%',
    textStyle: {
      color: '#fff',
      fontSize: 12
    }
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderColor: '#00ff88',
    borderWidth: 1,
    textStyle: {
      color: '#fff'
    },
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '15%',
    right: '10%',
    bottom: '10%',
    top: '20%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    boundaryGap: [0, 0.01],
    min: 0,
    max: 50,
    interval: 10,
    axisLabel: {
      formatter: '{value}%',
      color: '#00ff88',
      fontSize: 11
    },
    axisLine: {
      show: true,
      lineStyle: {
        color: '#00ff88'
      }
    },
    splitLine:{
      show: true,
      lineStyle: {
        color: 'rgba(0, 255, 136, 0.2)',
        type: 'dashed'
      }
    },
    axisTick: {
      lineStyle: {
        color: '#00ff88'
      }
    }
  },
  yAxis: {
    type: 'category',
    data: ['50岁以下', '50-59岁', '60-69岁', '70-79岁', '80岁及以上'],
    axisTick: {
      show: false
    },
    axisLine: {
      show: true,
      lineStyle: {
        color: '#00ff88'
      }
    },
    axisLabel: {
      color: '#00ff88',
      fontSize: 11,
      fontWeight: 'bold'
    }
  },
  series: [
    {
      name: '年龄分布',
      type: 'bar',
      data: [6.6, 14.7, 28.9, 33.2, 16.6],
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        color: '#fff',
        fontSize: 11,
        fontWeight: 'bold',
        formatter: '{c}%'
      },
      itemStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 1,
          y2: 0,
          colorStops: [
            { offset: 0, color: '#45b7d1' },
            { offset: 1, color: '#00ff88' }
          ]
        },
        borderRadius: [0, 4, 4, 0]
      },
      emphasis: {
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: '#00ff88' },
              { offset: 1, color: '#45b7d1' }
            ]
          }
        }
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
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderColor: '#00ff88',
    borderWidth: 1,
    textStyle: {
      color: '#fff'
    }
  },
  series: [
    {
      name: '问诊流程',
      type: 'graph',
      layout: 'none',
      symbolSize: 80,
      roam: true,
      label: {
        show: true,
        fontSize: 11,
        fontWeight: 'bold',
        color: '#fff'
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [6, 12],
      edgeLabel: {
        fontSize: 12,
        color: '#00ff88'
      },
      data: [
        {
          name: '症状描述',
          x: 100,
          y: 60,
          itemStyle: {
            color: '#00ff88',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          name: '信息填写',
          x: 300,
          y: 60,
          itemStyle: {
            color: '#4ecdc4',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          name: 'AI智能分析',
          x: 500,
          y: 60,
          itemStyle: {
            color: '#45b7d1',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          name: '医生匹配',
          x: 300,
          y: 180,
          itemStyle: {
            color: '#f39c12',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          name: '在线咨询',
          x: 150,
          y: 300,
          itemStyle: {
            color: '#9b59b6',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
        {
          name: '线下就诊',
          x: 450,
          y: 300,
          itemStyle: {
            color: '#e74c3c',
            borderColor: '#fff',
            borderWidth: 2
          }
        },
      ],
      links: [
        { source: '症状描述', target: '信息填写', lineStyle: { color: '#00ff88', width: 3 } },
        { source: '信息填写', target: 'AI智能分析', lineStyle: { color: '#4ecdc4', width: 3 } },
        { source: 'AI智能分析', target: '医生匹配', lineStyle: { color: '#45b7d1', width: 3 } },
        { source: '医生匹配', target: '在线咨询', lineStyle: { color: '#f39c12', width: 3 } },
        { source: '医生匹配', target: '线下就诊', lineStyle: { color: '#f39c12', width: 3 } },
      ],
      lineStyle: {
        opacity: 0.8,
        width: 3,
        curveness: 0.2
      },
      emphasis: {
        focus: 'adjacency',
        itemStyle: {
          borderColor: '#00ff88',
          borderWidth: 3
        },
        lineStyle: {
          width: 4
        }
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
  var myChart5 = echarts.init(document.getElementById("mapEchart"));
  // 重点：不要遗漏这句代码！！
  echarts.registerMap("china", geoJson);
  // 图表配置项
  let option5 = {
    tooltip: {
      show: true,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: '#00ff88',
      borderWidth: 1,
      textStyle: {
        color: '#fff',
        fontSize: 12
      },
      formatter: function(params) {
        if (params.componentType === 'geo3D') {
          return `${params.name}<br/>医院数量: ${params.value[2]}家`;
        } else if (params.componentType === 'series' && params.seriesType === 'bar3D') {
          return `${params.name}<br/>医院数量: ${params.value[2]}家`;
        }
        return `${params.name}`;
      }
    },
    //热力图配置项
    visualMap: [
      {
        type: "continuous",
        text: ["医院数量"],
        calculable: true,
        max: 150,
        min: 0,
        left: '35%',
        bottom: '15%',
        orient: 'vertical',
        itemWidth: 15,
        itemHeight: 120,
        inRange: {
          color: ["#001a2e", "#00ff88", "#4ecdc4", "#45b7d1"],
        },
        textStyle: {
          color: '#00ff88',
          fontSize: 11,
          fontWeight: 'bold'
        },
        controller: {
          inRange: {
            color: '#00ff88'
          }
        }
      },
    ],
    //3D地图配置项
    geo3D: {
      map: "china",
      roam: true,
      left: 'center',
      top: 'middle',
      boxWidth: 80,
      boxHeight: 60,
      boxDepth: 40,
      regionHeight: 3,
      itemStyle: {
        color: "#001a2e",
        opacity: 0.9,
        borderWidth: 1,
        borderColor: "#00ff88",
        metalness: 0.1,
        roughness: 0.8
      },
      viewControl: {
        autoRotate: true,
        autoRotateAfterStill: 3,
        distance: 60,
        center: [0, 0, 0], // 设置视角中心点
        minAlpha: 5, // 上下旋转的最小 alpha 值。即视角能旋转到达最上面的角度。[ default: 5 ]
        maxAlpha: 90, // 上下旋转的最大 alpha 值。即视角能旋转到达最下面的角度。[ default: 90 ]
        minBeta: -180, // 左右旋转的最小 beta 值。即视角能旋转到达最左的角度。[ default: -80 ]
        maxBeta: 360, // 左右旋转的最大 beta 值。即视角能旋转到达最右的角度。[ default: 80 ]
        animation: true, // 是否开启动画。[ default: true ]
        animationDurationUpdate: 1000, // 过渡动画的时长。[ default: 1000 ]
        animationEasingUpdate: "cubicInOut", // 过渡动画的缓动效果。[ default: cubicInOut ]
      },

      emphasis: {
        disabled: false,
        label: {
          show: true,
          color: "#00ff88",
          fontSize: 16,
          fontWeight: 'bold'
        },
        itemStyle: {
          color: "#4ecdc4",
          borderColor: "#00ff88",
          borderWidth: 2
        },
      },
      label: {
        show: true,
        position: "top",
        color: "#00ff88",
        fontSize: 11,
        fontWeight: 'bold',
        lineHeight: 14,
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
        barSize: 4,
        shading: "lambert",
        opacity: 0.9,
        bevelSize: 0.3,
        itemStyle: {
          color: function(params) {
            // 根据数值大小设置渐变色
            const value = params.value[2];
            if (value > 80) return '#00ff88';
            if (value > 60) return '#4ecdc4';
            if (value > 40) return '#45b7d1';
            if (value > 20) return '#74b9ff';
            return '#a29bfe';
          },
          metalness: 0.2,
          roughness: 0.6
        },
        label: {
          show: false, // 隐藏数字标签
          formatter: "{c}",
          color: '#00ff88',
          fontSize: 10,
          fontWeight: 'bold'
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
    if (myChart5) {
      myChart5.resize();
    }
  });
};

  </script>

  <style scoped>
  .chart-container {
    margin-bottom: 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .chart-header {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .title {
    height: auto;
    font-size: 16px;
    font-weight: bold;
    color: #00ff88;
    text-align: center;
    padding: 15px 0;
    margin-bottom: 10px;
    position: relative;
    z-index: 2;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    background: linear-gradient(90deg,
      transparent 0%,
      rgba(0, 255, 136, 0.1) 50%,
      transparent 100%);
    border-radius: 8px;
  }

  .title::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg,
      transparent 0%,
      #00ff88 50%,
      transparent 100%);
  }

  /* 确保图表容器占满剩余空间 */
  .chart-container > div:last-child {
    flex: 1;
  }
  </style>
