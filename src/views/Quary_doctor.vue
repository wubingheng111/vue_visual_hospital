<template>
    <div id="app">
      <!-- 输入框供用户输入特征 -->
      <input v-model="searchInput" type="text" placeholder="输入患病特征，例如：肺炎" />
  
      <!-- 搜索按钮 -->
      <button @click="searchDoctor">查询医生</button>
  
      <!-- 展示医生结果 -->
      <div id="results" v-if="doctors.length > 0">
        <h2>查询结果：</h2>
        <ul>
          <li v-for="doctor in doctors" :key="doctor.name">
            <strong>姓名:</strong> {{ doctor.name }}<br />
            <strong>职称:</strong> {{ doctor.position }}<br />
            <strong>科室:</strong> {{ doctor.department }}<br />
            <strong>医院:</strong> {{ doctor.hospital }}<br />
            <strong>评分:</strong> {{ doctor.rating }}<br />
            <strong>擅长:</strong> {{ doctor.specialty }}<br />
            <strong>挂号费:</strong> {{ doctor.registrationFee }}<br />
            <strong>门诊费:</strong> {{ doctor.consultationFee }}<br />
            <a :href="doctor.url" target="_blank">查看详情</a>
            <hr />
          </li>
        </ul>
      </div>
  
      <!-- 如果没有医生结果，显示提示 -->
      <div v-else>
        <p class="no-results">没有符合条件的医生。</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchInput: '', // 用户输入的搜索特征
        doctors: [] // 存储返回的医生信息
      };
    },
    methods: {
      // 搜索医生的功能
      searchDoctor() {
        // 调用后端API，传入用户输入的特征
        console.log(this.searchInput);
        axios
          .post('http://localhost:8000/api/doctors', {
            search: this.searchInput
          })
          .then((response) => {
            this.doctors = response.data; // 将医生数据存储到doctors中
          })
          .catch((error) => {
            console.error('查询医生信息时发生错误:', error);
          });
      }
    }
  };
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    margin-top: 20px;
  }
  
  input {
    padding: 10px;
    margin-right: 10px;
    width: 250px;
  }
  
  button {
    padding: 10px 20px;
    cursor: pointer;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    text-align: left;
    margin-bottom: 20px;
    color: white; /* 将字体颜色改为白色 */
  }
  
  #results {
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
    flex-direction: column; /* 垂直排列 */
    max-height: 600px; /* 设置固定高度 */
    overflow-y: auto; /* 启用垂直滚动 */
    margin-top: 60px; /* 增加顶部外边距，将容器位置往下挪 */
  }
  
  .no-results {
    color: white; /* 将“没有符合条件的医生。”的颜色改为白色 */
  }
  </style>