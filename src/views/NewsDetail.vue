<template>
    <main class="main-container">
      <div class="user-details" style="max-height: 600px; overflow: auto;">
        <h2>新闻详情</h2><br>
        <div class="details-container">
          <div class="poster">
            <img :src="ndetail.image_url" alt="新闻图片"/>
          </div>
          <div class="details">
            <table>
              <tr>
                <td class="label">新闻标题：</td>
                <td>{{ ndetail.title }}</td>
              </tr>
              <tr>
                <td class="label">新闻日期：</td>
                <td>{{ ndetail.date }}</td>
              </tr>
              <tr>
                <td class="label">新闻详情：</td>
                <td>{{ ndetail.content }}</td>
              </tr>
            </table>
          </div>
        </div><br>
        <button @click="goback" class="back-button">返回</button>
      </div>
    </main>
  </template>
  
  <script setup>
  import axios from 'axios';
  import router from '@/router';
  import { ref } from 'vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const nid = route.params.nid;
  const url = "http://localhost:3000/news/" + nid;
  const ndetail = ref({});
  axios.get(url)
    .then((response) => {
      // console.log(response.data);
      ndetail.value = response.data;
      console.log("====");
      console.log(ndetail);
    })
    .catch((error) => {
      console.log("error");
    });

    const goback = () => {
  router.go(-1); // 返回上一页
};
  </script>
  
  <style scoped>
  .user-details {
    background-color: #fff;
    border: 1px solid #ccc;
    width: 100%;
    max-width: 800px;
    padding: 30px;
  }
  
  h2 {
    background-color: #d9acff;
    color: #fff;
    border-radius: 5px;
    text-align: center;
    margin: 0;
    padding: 10px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }
  
  td {
    padding: 15px;
    border-bottom: 1px solid #eee;
  }
  
  .label {
    width:100px;
    font-weight: bold;
    color: #555;
  }
  
  .main-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .user-details img {
    width: 100%;
    height: 300px;
    border-radius: 5px;
    margin-bottom: 10px;
  }
  
  .back-button {
  background-color: #d9acff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}
  
  </style>
  