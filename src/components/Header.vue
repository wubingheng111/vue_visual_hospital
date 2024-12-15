<template>
  <div class="dashboard">
    <div class="head">
      <div id="ksleft">
        <router-link to="/"><h3 id="kleft">可视化大屏</h3></router-link>
      </div>
      <div id="newsleft">
        <router-link to="/news"><h3 id="nleft">医疗助手</h3></router-link>
      </div>
      <div id="usleft">
        <router-link to="/quary-doctor"><h3 id="uleft">在线问诊系统</h3></router-link>
      </div>
      <h1>医慧之翼</h1>
      <div id="selfright">
        <router-link to="/personal"><h3 id="sright">个人信息</h3></router-link>
      </div>
      <div id="glright">
        <router-link to="/guanli/controluser"><h3 id="gright">管理员</h3></router-link>
      </div>
      <div id="loginright">
        <h3 id="lright" @click="Exit">登录</h3>
      </div>
      <div id="time">
        <span id="showTime">{{ currentDate }} {{ currentTime }}</span>
      </div>
    </div>
    
    <RouterView/>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useLoginStore } from '@/stores/login';
  const currentDate = ref('');
  const currentTime = ref('');
  const loginStore = useLoginStore();
  const router = useRouter();

  // 在组件挂载后更新时间
  onMounted(() => {
    updateTime(); // 确保组件挂载后立即更新时间
    setInterval(updateTime, 1000); // 每秒更新时间
  });
  
  function updateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    currentDate.value = `${year}-${month}-${day}`;
    currentTime.value = `${hours}:${minutes}:${seconds}`;
  }

  const Exit = () => {
  // 重置 person125Info
  loginStore.person125Info.role = '';  
  loginStore.person125Info.name = '';
  loginStore.person125Info.id = '';
  loginStore.person125Info.state = false;

  // 跳转到 /login
  router.push('/login');
};
  </script>
  
  <style scoped>
  .dashboard {
  height: 100vh; /* 让可视化大屏充满整个视口高度 */
}
  h1 {
    text-align: center;
    color: rgba(255, 255, 255);
    font-weight: bold;
    line-height: 8vh;
  }

  h2 {
    color: rgba(255, 255, 255);
    font-weight: bold;
    line-height: 8vh;
  }

  .head {
    height: 8vh;
    width: 100%;
    background: url(./images/head_bg.png) no-repeat center center;
    background-size: 100% 100%;
  }

  #ksleft {
    position: absolute;
    left: 5%;
    top: 0%;
    line-height: 8vh;
  }

  #kleft {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }

  #newsleft {
    position: absolute;
    left: 15%;
    top: 0%;
    line-height: 8vh;
  }

  #nleft {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }

  #usleft {
    position: absolute;
    left: 25%;
    top: 0%;
    line-height: 8vh;
  }

  #uleft {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }
  
  #selfright {
    position: absolute;
    right: 30%;
    top: 0%;
    line-height: 8vh;
  }

  #sright {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }

  #glright {
    position: absolute;
    right: 20%;
    top: 0%;
    line-height: 8vh;
  }

  #gright {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }

  #loginright {
    position: absolute;
    right: 12%;
    top: 0%;
    line-height: 8vh;
  }

  #lright {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
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
  </style>
  