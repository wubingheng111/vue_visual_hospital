<template>
  <div class="register-container">
    <div class="register-card">
      <h2>用户注册</h2>
      <p class="subtitle">创建您的医慧之翼账户</p>

      <form class="register-form" @submit.prevent="register">
        <!-- 基本信息 -->
        <div class="form-section">
          <h3>基本信息</h3>

          <div class="form-group">
            <label for="name">
              <span class="label-icon">👤</span>
              真实姓名
            </label>
            <input
              type="text"
              id="name"
              v-model="form.name"
              placeholder="请输入您的真实姓名"
              required
            >
          </div>

          <div class="form-group">
            <label for="username">
              <span class="label-icon">🔑</span>
              用户名
            </label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              placeholder="请输入用户名（用于登录）"
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
              placeholder="请输入密码（至少6位）"
              required
              minlength="6"
            >
          </div>

          <div class="form-group">
            <label for="confirmPassword">
              <span class="label-icon">🔐</span>
              确认密码
            </label>
            <input
              type="password"
              id="confirmPassword"
              v-model="form.confirmPassword"
              placeholder="请再次输入密码"
              required
            >
          </div>
        </div>

        <!-- 联系方式 -->
        <div class="form-section">
          <h3>
            <span class="section-icon">📱</span>
            联系方式
          </h3>

          <div class="form-group">
            <label for="phone">
              <span class="label-icon">📱</span>
              手机号码
            </label>
            <input
              type="tel"
              id="phone"
              v-model="form.phone"
              placeholder="请输入手机号码"
              pattern="[0-9]{11}"
              required
            >
          </div>
        </div>

        <!-- 用户类型说明 -->
        <div class="form-section">
          <h3>
            <span class="section-icon">👥</span>
            用户类型
          </h3>

          <div class="role-display">
            <div class="role-info">
              <span class="role-badge">普通用户</span>
              <span class="role-desc">注册后可使用所有医疗服务功能</span>
            </div>
            <div class="role-features">
              <div class="feature-item">✅ 智能问诊服务</div>
              <div class="feature-item">✅ 在线医生咨询</div>
              <div class="feature-item">✅ 康复训练指导</div>
              <div class="feature-item">✅ 医院导航服务</div>
            </div>
          </div>
        </div>

        <!-- 协议同意 -->
        <div class="form-group agreement">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.agreeTerms"
              required
            >
            <span class="checkmark"></span>
            我已阅读并同意
            <a href="#" @click.prevent="showTerms">《用户协议》</a>
            和
            <a href="#" @click.prevent="showPrivacy">《隐私政策》</a>
          </label>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <button type="submit" class="register-btn" :disabled="isSubmitting">
            <span v-if="isSubmitting">注册中...</span>
            <span v-else>立即注册</span>
          </button>

          <div class="login-link">
            已有账户？
            <router-link to="/login">立即登录</router-link>
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
import { ElMessage } from 'element-plus'
import axios from 'axios'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

const router = useRouter()

// 简化的表单数据
const form = ref({
  name: '',           // 真实姓名
  username: '',       // 用户名（登录用）
  password: '',       // 密码
  confirmPassword: '', // 确认密码
  phone: '',          // 手机号码
  role: 'user',       // 固定为普通用户
  agreeTerms: false   // 协议同意
})

const isSubmitting = ref(false)

// 简化的表单验证
const validateForm = () => {
  // 检查必填字段
  if (!form.value.name.trim()) {
    ElMessage.error('请输入真实姓名')
    return false
  }

  if (!form.value.username.trim()) {
    ElMessage.error('请输入用户名')
    return false
  }

  if (form.value.username.length < 3) {
    ElMessage.error('用户名至少3个字符')
    return false
  }

  // 密码验证
  if (form.value.password.length < 6) {
    ElMessage.error('密码长度至少为6位')
    return false
  }

  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return false
  }

  // 手机号验证
  if (!/^1[3-9]\d{9}$/.test(form.value.phone)) {
    ElMessage.error('请输入正确的手机号码')
    return false
  }

  // 协议同意
  if (!form.value.agreeTerms) {
    ElMessage.error('请先同意用户协议和隐私政策')
    return false
  }

  return true
}

// 注册函数
const register = async () => {
  if (!validateForm()) return

  isSubmitting.value = true

  try {
    // 注册数据（包含后端必需的字段）
    const response = await axios.post('http://127.0.0.1:8000/register', {
      name: form.value.name.trim(),
      username: form.value.username.trim(),
      password: form.value.password,
      phone: form.value.phone,
      email: `${form.value.username}@temp.com`, // 临时邮箱，避免后端验证失败
      gender: 'unknown', // 默认性别
      age: null, // 可选字段
      location: '', // 可选字段
      role: form.value.role
    })

    if (response.data.code === 200) {
      ElMessage.success('注册成功！请登录')
      router.push('/login')
    } else {
      ElMessage.error(response.data.message || '注册失败')
    }
  } catch (error) {
    console.error('注册错误:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    isSubmitting.value = false
  }
}

// 显示用户协议
const showTerms = () => {
  ElMessage.info('用户协议功能待完善')
}

// 显示隐私政策
const showPrivacy = () => {
  ElMessage.info('隐私政策功能待完善')
}

// 处理语音命令
const handleVoiceCommand = (command) => {
  if (command.type === 'navigation' && command.action === '登录') {
    router.push('/login')
  }
}

// 处理语音回复
const handleVoiceResponse = (response) => {
  console.log('语音回复:', response)
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.register-card {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  backdrop-filter: blur(15px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  padding: 40px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.register-card h2 {
  text-align: center;
  color: #00ff88;
  margin-bottom: 10px;
  font-size: 28px;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
}

.subtitle {
  text-align: center;
  color: #ffffff;
  margin-bottom: 30px;
  font-size: 16px;
  opacity: 0.8;
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h3 {
  color: #ffffff;
  margin-bottom: 20px;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.section-icon {
  font-size: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.label-icon {
  font-size: 16px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
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

/* 角色显示样式 */
.role-display {
  padding: 20px;
  background: rgba(0, 255, 136, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  backdrop-filter: blur(5px);
}

.role-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.role-badge {
  color: #00ff88;
  font-weight: 700;
  font-size: 18px;
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.3);
}

.role-desc {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.4;
}

.role-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.feature-item {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
}

@media (max-width: 768px) {
  .role-features {
    grid-template-columns: 1fr;
  }
}

/* 角色显示样式 */
.role-display {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(0, 255, 136, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
}

.role-badge {
  color: #00ff88;
  font-weight: 600;
  font-size: 16px;
}

.role-desc {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.agreement {
  margin: 30px 0;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  line-height: 1.5;
  color: #ffffff;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.checkbox-label a {
  color: #00ff88;
  text-decoration: none;
  transition: all 0.3s ease;
}

.checkbox-label a:hover {
  color: #00cc6a;
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.5);
}

.form-actions {
  text-align: center;
  margin-top: 30px;
}

.register-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
  color: #1a1a2e;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 136, 0.4);
  background: linear-gradient(135deg, #00cc6a 0%, #00aa55 100%);
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-link {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.login-link a {
  color: #00ff88;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.login-link a:hover {
  color: #00cc6a;
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.5);
}

/* 滚动条样式 */
.register-card::-webkit-scrollbar {
  width: 6px;
}

.register-card::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.register-card::-webkit-scrollbar-thumb {
  background: #00ff88;
  border-radius: 3px;
}

.register-card::-webkit-scrollbar-thumb:hover {
  background: #00cc6a;
}
</style>
