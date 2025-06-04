<template>
  <div class="dashboard">
    <!-- 现代化Header -->
    <header class="modern-header">
      <!-- 左侧Logo和品牌 -->
      <div class="header-left">
        <div class="logo-container">
          <div class="logo-icon">🏥</div>
          <h1 class="brand-title">医慧之翼</h1>
          <span class="brand-subtitle">智慧医疗平台</span>
        </div>
      </div>

      <!-- 中央导航菜单 -->
      <nav class="header-nav">
        <div class="nav-container">
          <router-link
            v-for="item in navigationItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ 'active': $route.path === item.path }"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-text">{{ item.name }}</span>
            <div class="nav-indicator"></div>
          </router-link>
        </div>
      </nav>

      <!-- 右侧功能区 -->
      <div class="header-right">
        <!-- 搜索框 -->
        <div class="search-container" v-if="showSearch">
          <input
            type="text"
            placeholder="搜索功能..."
            class="search-input"
            v-model="searchQuery"
            @keyup.enter="handleSearch"
          >
          <span class="search-icon">🔍</span>
        </div>

        <!-- 通知中心 -->
        <div class="notification-container">
          <div class="notification-icon" @click="toggleNotifications">
            <span>🔔</span>
            <div class="notification-badge" v-if="notificationCount > 0">
              {{ notificationCount }}
            </div>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="user-container">
          <div class="user-info" @click="toggleUserMenu">
            <div class="user-avatar">
              <span>{{ isLoggedIn ? userInitial : '👤' }}</span>
            </div>
            <div class="user-details" v-if="isLoggedIn">
              <span class="user-name">{{ userName }}</span>
              <span class="user-role">{{ userRole }}</span>
            </div>
            <span class="dropdown-arrow">▼</span>
          </div>

          <!-- 用户下拉菜单 -->
          <div class="user-dropdown" v-show="showUserMenu">
            <div class="dropdown-item" v-if="!isLoggedIn" @click="handleAuth">
              <span class="dropdown-icon">🔑</span>
              <span>登录</span>
            </div>
            <template v-else>
              <div class="dropdown-item" @click="goToProfile">
                <span class="dropdown-icon">👤</span>
                <span>个人中心</span>
              </div>
              <div class="dropdown-item" @click="goToSettings">
                <span class="dropdown-icon">⚙️</span>
                <span>系统设置</span>
              </div>
              <div class="dropdown-divider"></div>
              <div class="dropdown-item logout" @click="handleAuth">
                <span class="dropdown-icon">🚪</span>
                <span>退出登录</span>
              </div>
            </template>
          </div>
        </div>

        <!-- 实时时间 -->
        <div class="time-container">
          <div class="time-display">
            <div class="time-date">{{ currentDate }}</div>
            <div class="time-clock">{{ currentTime }}</div>
          </div>
        </div>
      </div>
    </header>

    <!-- 面包屑导航 -->
    <div class="breadcrumb-container" v-if="showBreadcrumb">
      <nav class="breadcrumb">
        <span class="breadcrumb-item" v-for="(crumb, index) in breadcrumbs" :key="index">
          <router-link v-if="crumb.path" :to="crumb.path" class="breadcrumb-link">
            {{ crumb.name }}
          </router-link>
          <span v-else class="breadcrumb-current">{{ crumb.name }}</span>
          <span v-if="index < breadcrumbs.length - 1" class="breadcrumb-separator">></span>
        </span>
      </nav>
    </div>

    <RouterView/>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useLoginStore } from '@/stores/login';
import { ElMessage } from 'element-plus';

const currentDate = ref('');
const currentTime = ref('');
const loginStore = useLoginStore();
const router = useRouter();
const route = useRoute();

// 导航菜单配置
const navigationItems = ref([
  {
    path: '/',
    name: '可视化大屏',
    icon: '📊',
    description: '数据可视化展示'
  },
  {
    path: '/intelligent-consultation',
    name: '智能问诊',
    icon: '🤖',
    description: 'AI智能医疗咨询'
  },
  {
    path: '/quary-doctor',
    name: '在线问诊',
    icon: '👨‍⚕️',
    description: '在线医生咨询'
  },
  {
    path: '/personal',
    name: '康复训练',
    icon: '💪',
    description: '智能康复训练'
  },
  {
    path: '/health-analytics',
    name: '医院导航',
    icon: '🏥',
    description: '医院位置导航'
  }
]);

// UI状态管理
const showSearch = ref(true);
const showUserMenu = ref(false);
const showBreadcrumb = ref(true);
const searchQuery = ref('');
const notificationCount = ref(3);

// 用户信息
const isLoggedIn = computed(() => loginStore.person125Info.state);
const userName = computed(() => loginStore.person125Info.name || '用户');
const userRole = computed(() => loginStore.person125Info.role || '访客');
const userInitial = computed(() => {
  const name = loginStore.person125Info.name;
  return name ? name.charAt(0).toUpperCase() : 'U';
});

// 面包屑导航
const breadcrumbs = computed(() => {
  const pathMap = {
    '/': [{ name: '首页', path: '/' }],
    '/intelligent-consultation': [
      { name: '首页', path: '/' },
      { name: '智能问诊' }
    ],
    '/quary-doctor': [
      { name: '首页', path: '/' },
      { name: '在线问诊' }
    ],
    '/personal': [
      { name: '首页', path: '/' },
      { name: '康复训练' }
    ],
    '/health-analytics': [
      { name: '首页', path: '/' },
      { name: '医院导航' }
    ],
    '/login': [
      { name: '首页', path: '/' },
      { name: '用户登录' }
    ]
  };

  return pathMap[route.path] || [{ name: '首页', path: '/' }];
});

// 时间更新
onMounted(() => {
  updateTime();
  setInterval(updateTime, 1000);

  // 点击外部关闭下拉菜单
  document.addEventListener('click', handleClickOutside);
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

// 事件处理函数
const handleAuth = () => {
  if (isLoggedIn.value) {
    loginStore.person125Info.role = '';
    loginStore.person125Info.name = '';
    loginStore.person125Info.id = '';
    loginStore.person125Info.status = '';
    loginStore.person125Info.state = false;

    ElMessage.success('已退出登录');
    router.push('/login');
  } else {
    router.push('/login');
  }
  showUserMenu.value = false;
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const toggleNotifications = () => {
  ElMessage.info('通知功能开发中...');
};

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    ElMessage.info(`搜索功能开发中: ${searchQuery.value}`);
  }
};

const goToProfile = () => {
  ElMessage.info('个人中心功能开发中...');
  showUserMenu.value = false;
};

const goToSettings = () => {
  ElMessage.info('系统设置功能开发中...');
  showUserMenu.value = false;
};

const handleClickOutside = (event) => {
  if (!event.target.closest('.user-container')) {
    showUserMenu.value = false;
  }
};

// 监听路由变化，自动关闭菜单
watch(() => route.path, () => {
  showUserMenu.value = false;
});
</script>

<style scoped>
/* 全局样式 */
.dashboard {
  height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* 现代化Header */
.modern-header {
  height: 80px;
  width: 100%;
  background: linear-gradient(135deg, rgba(15, 15, 35, 0.98) 0%, rgba(26, 26, 46, 0.98) 50%, rgba(22, 33, 62, 0.98) 100%);
  backdrop-filter: blur(25px);
  border-bottom: 2px solid rgba(0, 212, 255, 0.2);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 2px 8px rgba(0, 212, 255, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem 0 2rem; /* 左边保持2rem，右边减少到1.5rem */
  transition: all 0.3s ease;
}

.modern-header:hover {
  box-shadow:
    0 12px 40px rgba(0, 0, 0, 0.5),
    0 4px 12px rgba(0, 212, 255, 0.15);
}

/* 左侧Logo区域 */
.header-left {
  display: flex;
  align-items: center;
  min-width: 280px;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: 12px;
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.1);
  transition: all 0.3s ease;
}

.logo-container:hover {
  background: rgba(0, 212, 255, 0.1);
  transform: translateY(-2px);
}

.logo-icon {
  font-size: 32px;
  filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.3));
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #00d4ff 0%, #ffffff 50%, #00d4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  letter-spacing: 1px;
}

.brand-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 400;
  margin-left: 8px;
  padding: 2px 8px;
  background: rgba(0, 212, 255, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(0, 212, 255, 0.2);
}

/* 中央导航菜单 */
.header-nav {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
}

.nav-container {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: rgba(0, 212, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 255, 0.1);
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  overflow: hidden;
}

.nav-item:hover {
  color: #00d4ff;
  background: rgba(0, 212, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
}

.nav-item.active {
  color: #00d4ff;
  background: rgba(0, 212, 255, 0.15);
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3);
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: scaleX(1);
}

.nav-icon {
  font-size: 16px;
  filter: drop-shadow(0 0 4px rgba(0, 212, 255, 0.3));
}

.nav-text {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #00d4ff, #ffffff, #00d4ff);
  border-radius: 2px;
  opacity: 0;
  transform: scaleX(0);
  transition: all 0.3s ease;
}

/* 右侧功能区 */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 450px;
  justify-content: flex-end;
  padding-right: 20px; /* 整体向左移动 */
}

/* 搜索框 */
.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 200px;
  height: 36px;
  padding: 0 40px 0 16px;
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 18px;
  color: #ffffff;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.3);
  width: 240px;
}

.search-icon {
  position: absolute;
  right: 12px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  pointer-events: none;
}

/* 通知中心 */
.notification-container {
  position: relative;
}

.notification-icon {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-icon:hover {
  background: rgba(0, 212, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 18px;
  height: 18px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  font-size: 10px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(15, 15, 35, 0.98);
}

/* 用户信息区域 */
.user-container {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(0, 212, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #00d4ff, #ffffff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: #1a1a2e;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.dropdown-arrow {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.6);
  transition: transform 0.3s ease;
}

.user-info:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* 用户下拉菜单 */
.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  min-width: 200px;
  background: rgba(15, 15, 35, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  z-index: 1001;
  overflow: hidden;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background: rgba(0, 212, 255, 0.1);
  color: #00d4ff;
}

.dropdown-item.logout:hover {
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
}

.dropdown-icon {
  font-size: 16px;
}

.dropdown-divider {
  height: 1px;
  background: rgba(0, 212, 255, 0.1);
  margin: 4px 0;
}

/* 时间显示 */
.time-container {
  display: flex;
  align-items: center;
  margin-right: 10px; /* 增加右边距，进一步向左移动 */
}

.time-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 10px 16px; /* 增加内边距，让时间区域更宽一些 */
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 10px;
  min-width: 100px; /* 设置最小宽度，保持一致性 */
}

.time-date {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 400;
}

.time-clock {
  font-size: 14px;
  color: #00d4ff;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

/* 面包屑导航 */
.breadcrumb-container {
  margin-top: 80px;
  padding: 12px 2rem;
  background: rgba(0, 212, 255, 0.02);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.breadcrumb-link:hover {
  color: #00d4ff;
}

.breadcrumb-current {
  color: #00d4ff;
  font-size: 14px;
  font-weight: 500;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-right {
    min-width: 300px;
  }

  .search-container {
    display: none;
  }

  .user-details {
    display: none;
  }
}

@media (max-width: 768px) {
  .modern-header {
    padding: 0 1rem;
  }

  .header-left {
    min-width: 200px;
  }

  .brand-subtitle {
    display: none;
  }

  .nav-text {
    display: none;
  }

  .nav-item {
    padding: 12px;
  }

  .header-right {
    min-width: 150px;
  }

  .notification-container {
    display: none;
  }
}
  </style>
