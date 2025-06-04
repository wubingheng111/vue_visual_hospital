<template>
  <el-container class="layout-container-demo">
    <el-aside width="200px" class="custom-aside">
      <el-scrollbar wrap-class="scrollbar-wrap">
        <el-menu :default-openeds="['1','2','3']" class="custom-menu">
          <!-- 用户管理 -->
          <el-sub-menu index="1">
            <template #title>
              <i class="el-icon-document"></i>用户管理
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/controluser">
                <el-menu-item index="1-1">用户信息管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlblack">
                <el-menu-item index="1-2">黑名单管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlnews">
                <el-menu-item index="1-3">新闻管理</el-menu-item>
              </router-link>
              <router-link to="/guanli/controlzice">
              <el-menu-item index="1-4">自测管理</el-menu-item>
            </router-link>
            </el-menu-item-group>
          </el-sub-menu>

          <!-- 医生管理 -->
          <el-sub-menu index="2">
            <template #title>
              <i class="el-icon-suitcase"></i>医生管理
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/controldoctor">
                <el-menu-item index="2-1">医生信息管理</el-menu-item>
              </router-link>
            </el-menu-item-group>
          </el-sub-menu>

          <el-sub-menu index="3">
            <template #title>
              <i class="el-icon-suitcase"></i>管理员信息
            </template>
            <el-menu-item-group>
              <router-link to="/guanli/manageself">
                <el-menu-item index="3-1">个人信息修改</el-menu-item>
              </router-link>
                <el-menu-item index="3-2" @click="Exit">退出登录</el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>
    <el-main>
      <router-view />
    </el-main>

    <!-- 智能交互组件 -->
    <GestureControl
      @navigationGesture="handleNavigationGesture"
    />
    <VoiceInteraction
      @voiceCommand="handleVoiceCommand"
      @voiceResponse="handleVoiceResponse"
    />
  </el-container>
</template>

  <script setup>
  import { useLoginStore } from '@/stores/login';
  import { useRouter } from 'vue-router';
  import GestureControl from '@/components/GestureControl.vue';
  import VoiceInteraction from '@/components/VoiceInteraction.vue';
  const loginStore = useLoginStore();
  const router = useRouter();
const Exit = () => {
  // 重置 person125Info
  loginStore.person125Info.role = '';
  loginStore.person125Info.name = '';
  loginStore.person125Info.id = '';
  loginStore.person125Info.state = false;

  // 跳转到 /login
  router.push('/login');
};

// 处理导航手势 - 优化版（避免重复执行）
const handleNavigationGesture = (action) => {
  console.log('管理后台导航手势:', action);

  switch (action) {
    case 'zoom_in':
      document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString();
      ElMessage.success('🤲 手势控制：页面已放大');
      break;
    case 'zoom_out':
      document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString();
      ElMessage.success('🤲 手势控制：页面已缩小');
      break;
    case 'scroll_top':
      window.scrollTo({ top: 0, behavior: 'smooth' });
      ElMessage.success('🤲 手势控制：已返回页面顶部');
      break;
    case 'scroll_bottom':
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      ElMessage.success('🤲 手势控制：已滚动到页面底部');
      break;
    case 'confirm_action':
      // 在管理后台，确认手势可以用于刷新页面
      location.reload();
      ElMessage.success('🤲 手势控制：页面已刷新');
      break;
    case 'stop_action':
      // 停止当前操作
      ElMessage.info('🤲 手势控制：已停止当前操作');
      break;
    default:
      console.log('未处理的手势动作:', action);
  }
};

// 处理语音命令 - 增强版
const handleVoiceCommand = (command) => {
  console.log('管理后台语音命令:', command);

  if (command.type === 'navigation') {
    switch (command.action) {
      case '用户管理':
      case '管理用户':
      case '用户':
        router.push('/guanli/controluser');
        ElMessage.success('正在跳转到用户管理页面');
        break;
      case '黑名单管理':
      case '黑名单':
      case '管理黑名单':
        router.push('/guanli/controlblack');
        ElMessage.success('正在跳转到黑名单管理页面');
        break;
      case '新闻管理':
      case '管理新闻':
      case '新闻':
      case '资讯管理':
        router.push('/guanli/controlnews');
        ElMessage.success('正在跳转到新闻管理页面');
        break;
      case '医生管理':
      case '管理医生':
      case '医生':
        router.push('/guanli/controldoctor');
        ElMessage.success('正在跳转到医生管理页面');
        break;
      case '个人信息':
      case '个人设置':
      case '我的信息':
        router.push('/guanli/manageself');
        ElMessage.success('正在跳转到个人信息页面');
        break;
      case '退出登录':
      case '登出':
      case '退出':
        ElMessageBox.confirm('确定要退出登录吗？', '确认退出', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          Exit();
          ElMessage.success('已退出登录');
        }).catch(() => {
          ElMessage.info('已取消退出');
        });
        break;
    }
  } else if (command.type === 'system') {
    // 处理系统级语音命令
    switch (command.action) {
      case '刷新':
      case '更新':
        location.reload();
        break;
      case '返回顶部':
        window.scrollTo({ top: 0, behavior: 'smooth' });
        break;
    }
  }
};

// 处理语音回复
const handleVoiceResponse = (response) => {
  console.log('语音回复:', response);
};
  </script>

  <style scoped>
  .layout-container-demo {
    height: 100%;
    background-color: #f0f5ff;
  }

  .custom-aside {
    height: 100%;
    background-color: #c6e2ff;
  }

  .custom-menu {
    border-right: none;
  }

  .scrollbar-wrap {
    height: 100%;
  }

  /* // 根据实际需求调整图标样式 */
  .el-icon-document, .el-icon-suitcase, .el-icon-setting {
    font-size: 18px;
    margin-right: 10px;
  }
  </style>
