<template>
  <div class="login-container">
    <h2>用户登录</h2><br>
    <form class="login-form" @submit.prevent="login_func">
      <div class="form-group">
        <label for="username">用户名&nbsp;&nbsp;</label>
        <input type="text" id="username" v-model="form.username" required>
      </div>
      <div class="form-group">
        <label for="password">密码&nbsp;&nbsp;&nbsp;&nbsp;</label>
        <input type="password" id="password" v-model="form.password" required>
      </div>
      <div class="form-group">
        <label for="role">角色&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
        <select id="role" v-model="form.role" required>
          <option value="admin">管理员</option>
          <option value="user">用户</option>
        </select>
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// import { useLoginStore } from '@/stores/login';s
import axios from 'axios';

// const loginStore = useLoginStore();
const router = useRouter();
const url = 'http://127.0.0.1:8000'; // 后端API地址
const form = ref({
  username: '',
  password: '',
  role: 'user',
});

function login_func () {
  // 使用 POST 请求发送登录信息
  axios.post(url + '/login', form.value)
    .then((response) => {
      const code = response.data.code;
      const role = response.data.role;
      const message = response.data.message;
      alert("code:"+code+"role:"+role+"message:"+message);
      console.log(response.data);
      if (code === 200 && role === 'user' && message === '登录成功') {
        router.push({ path: '/personal' });

      } else if (code === 200 && role === 'admin' && message === '登录成功') {
        router.push({ path: '/guanli/controluser' });
      } else {
        alert("用户名、密码或角色不匹配！");
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
</script>



<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="password"],
select,
button {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  margin-left: auto;
  margin-right: auto;
}

button {
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
  border: none;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
