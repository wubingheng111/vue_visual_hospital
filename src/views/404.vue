<template>
  <div class="not-found">
    <img src="../assets/404.gif" alt="404 Not Found" @click="goHome">
    <button class="overlay-button" @click="goHome">返回首页</button>

    <!-- 智能交互组件 -->
    <GestureControl
      @navigationGesture="handleNavigationGesture"
    />
    <VoiceInteraction
      @voiceCommand="handleVoiceCommand"
      @voiceResponse="handleVoiceResponse"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useLoginStore } from '@/stores/login';
import GestureControl from '@/components/GestureControl.vue';
import VoiceInteraction from '@/components/VoiceInteraction.vue';
const router = useRouter();
const loginStore = useLoginStore();

const goHome = () => {
  if(loginStore.person125Info.state==false){
    router.push('/');
  }else if(loginStore.person125Info.state==true){
    if(loginStore.person125Info.role=='user'){
    router.push('/personal');
      }else if(loginStore.person125Info.role=='admin'){
        router.push('/health-analytics');
      }
  }
};

// 处理导航手势
const handleNavigationGesture = (action) => {
  switch (action) {
    case 'confirm_action':
    case 'scroll_top':
      goHome();
      break;
    case 'zoom_in':
      document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString();
      break;
    case 'zoom_out':
      document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString();
      break;
  }
};

// 处理语音命令
const handleVoiceCommand = (command) => {
  if (command.type === 'navigation') {
    if (command.action === '首页' || command.action === '主页' || command.action === '返回首页') {
      goHome();
    }
  }
};

// 处理语音回复
const handleVoiceResponse = (response) => {
  console.log('语音回复:', response);
};
</script>

<style scoped>
.not-found {
  position: relative;
  text-align: center;
  margin-top: 15px;
  height: 100vh; /* 设置高度为视口高度 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.not-found img {
  width: 100vw; /* 设置宽度为视口宽度 */
  height: 100%; /* 高度自适应 */
  max-width: 100%; /* 图片最大宽度为100% */
  object-fit: cover; /* 图片按比例填充容器 */
}

.overlay-button {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 5px;
  cursor: pointer;
}
</style>
