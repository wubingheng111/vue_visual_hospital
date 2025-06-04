<template>
  <div class="no-access-container">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- 无权限卡片 -->
    <div class="no-access-card">
      <div class="icon-container">
        <span class="access-icon">🚫</span>
      </div>

      <h1>访问受限</h1>
      <p class="message">抱歉，您没有访问该页面的权限</p>

      <div class="user-info" v-if="loginStore.person125Info.state">
        <div class="info-item">
          <span class="info-label">当前用户：</span>
          <span class="info-value">{{ loginStore.person125Info.name || '未知用户' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">用户角色：</span>
          <span class="info-value">{{ getRoleText(loginStore.person125Info.role) }}</span>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="goHome" class="primary-btn">
          <span class="btn-icon">🏠</span>
          返回主页
        </button>
        <button @click="logout" class="secondary-btn">
          <span class="btn-icon">🚪</span>
          重新登录
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/login'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginStore = useLoginStore()

// 获取角色文本
const getRoleText = (role) => {
  const roleMap = {
    'user': '普通用户',
    'admin': '管理员',
    'doctor': '医生'
  }
  return roleMap[role] || '未知角色'
}

// 返回主页
const goHome = () => {
  if (!loginStore.person125Info.state) {
    // 未登录用户返回可视化大屏
    router.push('/')
  } else {
    // 已登录用户返回康复训练页面（用户主页）
    router.push('/personal')
  }
}

// 退出登录
const logout = () => {
  // 清除登录状态
  loginStore.person125Info.id = ''
  loginStore.person125Info.name = ''
  loginStore.person125Info.role = ''
  loginStore.person125Info.status = ''
  loginStore.person125Info.state = false

  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>
<style scoped>
.no-access-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* 背景动画 */
.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 107, 107, 0.1), rgba(255, 136, 0, 0.1));
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 15%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 20%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 30%;
  left: 70%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 0.6;
  }
}

/* 无权限卡片 */
.no-access-card {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(255, 107, 107, 0.3);
  border-radius: 20px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  backdrop-filter: blur(15px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 2;
  text-align: center;
}

.icon-container {
  margin-bottom: 20px;
}

.access-icon {
  font-size: 64px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.no-access-card h1 {
  color: #ff6b6b;
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 15px 0;
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
}

.message {
  color: #ffffff;
  font-size: 18px;
  margin: 0 0 30px 0;
  opacity: 0.9;
  line-height: 1.5;
}

/* 用户信息 */
.user-info {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin: 30px 0;
  text-align: left;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.info-value {
  color: #ffffff;
  font-weight: 600;
  font-size: 14px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.primary-btn,
.secondary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
  justify-content: center;
}

.primary-btn {
  background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
  color: #1a1a2e;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4);
  background: linear-gradient(135deg, #00cc6a 0%, #00aa55 100%);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
}

.btn-icon {
  font-size: 18px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .no-access-card {
    margin: 20px;
    padding: 30px 25px;
  }

  .no-access-card h1 {
    font-size: 28px;
  }

  .message {
    font-size: 16px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .primary-btn,
  .secondary-btn {
    width: 100%;
    max-width: 200px;
  }
}
</style>
