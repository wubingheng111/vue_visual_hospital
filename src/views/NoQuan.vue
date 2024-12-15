<template>
    <div class="container">
        <div class="no-access-page">
            <h1>权限不足</h1><br>
            <p>抱歉，您没有访问该页面的权限。</p><br>
            <button @click="goHome">返回</button>
        </div>
    </div>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { useLoginStore } from '@/stores/login';
const router = useRouter();
const loginStore = useLoginStore();
const goHome = () => {
  if(loginStore.person125Info.state==false){
    router.push('/');
  }else if(loginStore.person125Info.state==true){
    if(loginStore.person125Info.role=='user'){
    router.push('/personal');
      }else if(loginStore.person125Info.role=='admin'){
        router.push('/guanli/controluser');
      }
  }
};
</script>
<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: white;
    }

    .no-access-page {
        text-align: center;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        max-width: 300px;
    }

    h1 {
        color: #333;
        font-size: 24px;
    }

    p {
        color: #666;
        font-size: 18px;
    }
</style>
