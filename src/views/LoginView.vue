<template>
  <div class="login-container">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- 头部 -->
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🏥</span>
          <h1>医慧之翼</h1>
        </div>
        <p class="subtitle">智能医疗服务平台</p>
      </div>

      <!-- 登录表单 -->
      <form class="login-form" @submit.prevent="login_func">
        <div class="form-group">
          <label for="username">
            <span class="label-icon">👤</span>
            用户名
          </label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            placeholder="请输入用户名"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">
            <span class="label-icon">🔒</span>
            密码
          </label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="请输入密码"
            required
          >
        </div>

        <!-- 移除角色选择，统一为用户身份 -->

        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner">⏳</span>
          <span v-else>🚀</span>
          {{ isLoading ? '登录中...' : '立即登录' }}
        </button>

        <div class="form-footer">
          <div class="register-link">
            还没有账户？
            <router-link to="/register">立即注册</router-link>
          </div>

          <div class="guest-access">
            <router-link to="/" class="guest-link">
              👁️ 游客访问（仅可查看数据大屏）
            </router-link>
          </div>
        </div>
      </form>
    </div>

    <!-- 智能交互组件 -->
    <VoiceInteraction
      @voiceCommand="handleVoiceCommand"
      @voiceResponse="handleVoiceResponse"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/login'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

const router = useRouter()
const loginStore = useLoginStore()
const url = 'http://127.0.0.1:8000' // 后端API地址

const form = ref({
  username: '',
  password: '',
  role: 'user', // 统一设置为用户角色
})

const isLoading = ref(false)

// 登录函数
const login_func = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.error('请填写完整的登录信息')
    return
  }

  isLoading.value = true

  try {
    const response = await axios.post(url + '/login', form.value)
    const { code, role, message, data } = response.data

    if (code === 200 && message === '登录成功') {
      // 保存登录状态到store
      loginStore.person125Info.id = data?.id || ''
      loginStore.person125Info.name = data?.name || form.value.username
      loginStore.person125Info.role = 'user' // 统一设置为用户角色
      loginStore.person125Info.status = 'active'
      loginStore.person125Info.state = true

      ElMessage.success('登录成功！欢迎使用医慧之翼智能医疗平台')

      // 登录成功后跳转到康复训练页面（作为用户主页）
      router.push('/personal')
    } else {
      ElMessage.error(message || '登录失败，请检查用户名和密码')
    }
  } catch (error) {
    console.error('登录错误:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  } finally {
    isLoading.value = false
  }
}

// 处理语音命令
const handleVoiceCommand = (command) => {
  if (command.type === 'navigation') {
    if (command.action === '注册') {
      router.push('/register')
    } else if (command.action === '游客访问') {
      router.push('/')
    }
  } else if (command.type === 'form') {
    if (command.field === 'username') {
      form.value.username = command.value
    } else if (command.field === 'password') {
      form.value.password = command.value
    }
  }
}

// 处理语音回复
const handleVoiceResponse = (response) => {
  console.log('语音回复:', response)
}
</script>



<style scoped>
.login-container {
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
  background: linear-gradient(45deg, rgba(0, 255, 136, 0.1), rgba(0, 136, 255, 0.1));
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 30%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 30%;
  animation-delay: 1s;
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

/* 登录卡片 */
.login-card {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  padding: 40px;
  max-width: 450px;
  width: 100%;
  backdrop-filter: blur(15px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 2;
}

/* 头部样式 */
.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 10px;
}

.logo-icon {
  font-size: 32px;
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

.logo h1 {
  color: #00ff88;
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
}

.subtitle {
  color: #ffffff;
  font-size: 16px;
  margin: 0;
  opacity: 0.8;
}

/* 表单样式 */
.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ffffff;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 14px;
}

.label-icon {
  font-size: 16px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
  background: rgba(255, 255, 255, 0.15);
}

.form-group select option {
  background: #1a1a2e;
  color: #ffffff;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
  color: #1a1a2e;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4);
  background: linear-gradient(135deg, #00cc6a 0%, #00aa55 100%);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 表单底部 */
.form-footer {
  text-align: center;
}

.register-link {
  margin-bottom: 15px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.register-link a {
  color: #00ff88;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.register-link a:hover {
  color: #00cc6a;
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.5);
}

.guest-access {
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.guest-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.guest-link:hover {
  color: #0088ff;
  text-shadow: 0 0 5px rgba(0, 136, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-card {
    margin: 20px;
    padding: 30px 25px;
  }

  .logo h1 {
    font-size: 24px;
  }

  .form-group input,
  .form-group select {
    padding: 12px 16px;
    font-size: 14px;
  }

  .login-btn {
    padding: 12px;
    font-size: 16px;
  }
}
</style>
