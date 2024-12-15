<template>
    <div class="dashboard">
      <div class="container">
        <ul class="main_box">
        <li class="left_box">
          <div class="left_box_top all_box box_head">
            <Chart title="全国医院经营方式雷达图" chart-id="ad" chart-width="600px" chart-height="400px" />
          </div>
          <div class="left_box_middle all_box box_head">
            <Chart title="全国医院数量分级" chart-id="ad1" chart-width="450px" chart-height="350px" />
          </div>
        </li>

        <li class="middle_box">
          <div class="right_box_top all_box box_head">
            <Chart title="医慧之翼问诊流程" chart-id="ad4" chart-width="600px" chart-height="350px" />
          </div>
          <div class="right_box_middle all_box box_head">
            <Chart title="各省(直辖市)三甲医院医院数量分布" chart-id="mapEchart" chart-width="600px" chart-height="350px" />
          </div>
        </li>

        <li class="right_box">
          <div class="right_box_top all_box box_head">
            <Chart title="线上问诊医生评分分布" chart-id="ad2" chart-width="450px" chart-height="320px" />
          </div>

          <div class="right_box_middle all_box box_head">
            <Chart title="患者年龄分布" chart-id="ad3" chart-width="400px" chart-height="300px" />
          </div>
        </li>
      </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import Chart from './Chart.vue';
  </script>
  
<style scoped>
  .dashboard {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    height: 100vh; /* 让可视化大屏充满整个视口高度 */
  }
  
  .visualization {
    width: 80%; /* 设置可视化大屏内容宽度 */
    height: 80%; /* 设置可视化大屏内容高度 */
    border: 1px solid #ccc; /* 添加边框 */
    border-radius: 10px; /* 添加圆角 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  }
  
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'PingFangSC-Regular', 'helvetica neue', tahoma, 'PingFang SC', 'microsoft yahei', arial, 'hiragino sans gb', sans-serif;
      overflow: hidden;
  }
  
  #page-3 {
      background: #000d4a url(./images/bg3.jpg) center top;
      background-size: cover;
      color: #666;
      font-family: "微软雅黑";
      height: 100vh;
      font-size: 1rem;
  }
  
  .head {
      height: 8vh;
      width: 100%;
      background: url(./images/head_bg.png) no-repeat center center;
      background-size: 100% 100%;
  }
  
  h1 {
      text-align: center;
      color: rgba(255, 255, 255);
      font-weight: bold;
      line-height: 8vh;
  }
  
  #time {
      position: absolute;
      right: 0.33%;
      top: 0%;
      line-height: 8vh;
  }
  
  #showTime {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }
  
  .main_box {
      list-style: none;
      display: flex;
      justify-content: center;
      margin-top: 0.33rem;
      padding: 0.05rem;
  }
  
  .main_box>li {
      display: inline;
  }
  
  .container>ul>:nth-child(1),
  .container>ul>:nth-child(3) {
      width: 30vw;
      height: 100vh;
      float: left;
      padding: 0rem 0.005rem;
  }
  
  .container>ul>:nth-child(2) {
      width: 40vw;
      height: 100vh;
      float: left;
      padding: 0rem 0.005rem;
  }
  
  .all_box {
      border: .0625rem solid rgba(25, 186, 139, .17);
      padding: 0rem .2rem .4rem .15rem;
      background: rgba(255, 255, 255, .04) url(./images/line.png);
      background-size: 100% auto;
      position: relative;
      margin-bottom: .15rem;
      z-index: 10;
  }
  
  .left_box_top {
      height: 45%;
      width: 100%;
      margin: auto;
  }
  
  .title {
      height: 4.3vh;
      font-size: 1rem;
      color: white;
      text-align: center;
      line-height: 4.3vh;
  }
  
  .m_v_ul {
      list-style: none;
      display: flex;
      justify-content: center;
      justify-content: space-between;
      flex-wrap: nowrap;
      text-align: center;
  }
  
  .m_v_ul>li {
      font-size: 0.9rem;
      padding: 0.9rem;
  }
  
  h2 {
      margin: 0;
      padding: 0;
      color: #c5ccff;
  }
  
  .m_v_ul>li>span {
      font-size: 0.5rem;
      color: #fff;
      opacity: 0.5;
  }
  
  .first_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 70%;
      top: 30%;
  }
  
  .second_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 30%;
      top: 30%;
  }
  
  ._first_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 70%;
      top: 68%;
  }
  
  ._second_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 30%;
      top: 68%;
  }
  
  .box_head::before {
      position: absolute;
      width: 0.5rem;
      height: 0.5rem;
      content: "";
      border-top: 0.125rem solid #02a6b5;
      border-left: 0.125rem solid #02a6b5;
      top: 0;
      left: 0;
  }
  
  .box_head::after {
      position: absolute;
      width: 0.5rem;
      height: 0.5rem;
      content: "";
      border-top: 0.125rem solid #02a6b5;
      border-right: 0.125rem solid #02a6b5;
      top: 0;
      right: 0;
  }
  
  .box_foot::before {
      position: absolute;
      width: 0.5rem;
      height: 0.5rem;
      content: "";
      border-bottom: 0.125rem solid #02a6b5;
      border-left: 0.125rem solid #02a6b5;
      bottom: 0;
      left: 0;
  }
  
  .box_foot::after {
      position: absolute;
      width: 0.5rem;
      height: 0.5rem;
      content: "";
      border-bottom: 0.125rem solid #02a6b5;
      border-right: 0.125rem solid #02a6b5;
      bottom: 0;
      right: 0;
  }
  
  .left_box_middle {
      height: 45%;
      width: 100%;
      margin: auto;
      margin-top: 1.25rem;
  }
  
  #left_middle_echarts {
      height: 100%;
      width: 100%;
  }
  
  .left_box_down {
      height: 28%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }
  
  #left_down_echarts {
      height: 100%;
      width: 100%;
      margin-top: -.9rem;
      margin-left: -.6rem;
  }
  
  .middle_up {
      width: 100%;
      height: 100%;
      margin: auto;
  }
  
  .middle_box_up {
      display: flex;
      justify-content: center;
      height: 15%;
      width: 100%;
      margin: auto;
      text-align: center;
      z-index: 100;
  }
  
  .money_show {
      position: absolute;
      text-align: center;
      width: 39vw;
      margin: auto;
      background: rgba(101, 132, 226, .1);
      padding: 0.8rem;
  }
  
  .middle_up_up_box {
      height: 4.5rem;
      width: 100%;
      margin: auto;
      border: .0655rem solid rgba(25, 186, 139, .17);
      position: relative;
  }
  
  .now_money {
      display: flex;
      height: 4.5rem;
      margin: auto;
      line-height: 4.5rem;
      text-align: center;
      justify-content: space-around;
      overflow: hidden;
      margin-top: -0.3rem;
  }
  
  @font-face {
      font-family: electronicFont;
      src: url('./libs/font/Open-24-Display-St-1.ttf');
  }
  
  .in_money,
  .out_money {
      font-family: electronicFont;
      font-size: 3rem;
      letter-spacing: .1875rem;
      color: #ffeb7b;
      overflow: hidden;
      display: inline-block;
      width: 12.5rem;
  }
  
  .in_money::after {
      position: absolute;
      content: "";
      height: 1.875rem;
      width: .0625rem;
      background-color: #3e4f8d;
      right: 50%;
      top: 30%;
  }
  
  .middle_middle_box {
      height: 60%;
      width: 100%;
      margin: auto;
  }
  
  ._middle_middle_box {
      height: 100%;
      width: 100%;
      margin-top: -3rem;
      overflow: visible;
  }
  
  #middle_down_echarts {
      height: 100%;
      width: 39vw;
  }
  
  .middle_down_box {
      height: 5%;
      width: 100%;
      position: relative;
      margin-top: 10%;
      overflow: hidden;
      text-align: center;
      /* display: flex;
      justify-content: center; */
  }
  
  #tips {
      position: relative;
      width: 40.625rem;
      /* line-height: 3.125rem; */
      height: 3.125rem;
      margin: auto;
      overflow: hidden;
      color: #6faac8;
      text-align: center;
  }
  
  #tips span {
      position: absolute;
      left: 0;
      margin: 0.5rem .625rem;
      font-size: 1rem;
      white-space: nowrap;
  }
  
  @keyframes around1 {
      from {
          left: 0;
      }
      to {
          left: -100%;
      }
  }
  
  @keyframes around2 {
      from {
          left: 100%;
      }
      to {
          left: 0%;
      }
  }
  
  #tips .span1 {
      animation: around1 9s linear infinite;
  }
  
  #tips .span2 {
      animation: around2 9s linear infinite;
  }
  
  .middle_up_down_box {
      display: flex;
      margin: auto;
      margin-top: .25rem;
      font-size: 1rem;
      color: rgba(255, 255, 255, .7);
      justify-content: space-around;
  }
  
  .middle_up_up_box::before {
      position: absolute;
      width: 1rem;
      height: .5rem;
      content: "";
      border-top: .125rem solid #02a6b5;
      border-left: .125rem solid #02a6b5;
      top: 0;
      left: 0;
  }
  
  .now_money_foot::after {
      position: absolute;
      width: 1rem;
      height: .5rem;
      content: "";
      border-bottom: .125rem solid #02a6b5;
      border-right: .125rem solid #02a6b5;
      bottom: 0;
      right: 0;
  }
  
  .right_box {
      overflow: hidden;
  }
  
  .right_box_top {
      height: 45%;
      width: 96%;
      margin: auto;
  }
  
  #right_up_echarts {
      height: 100%;
      width: 100%;
      overflow: hidden;
  }
  
  .right_box_middle {
      height: 45%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }
  
  #right_middle_echarts {
      height: 100%;
      width: 100%;
      overflow: hidden;
  }
  
  .right_box_down {
      height: 45%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }
  
  #right_down_echarts {
      height: 100%;
      width: 100%;
  }
  
  </style>