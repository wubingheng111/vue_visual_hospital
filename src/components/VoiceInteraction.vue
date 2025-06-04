<template>
  <div class="voice-interaction">
    <!-- 语音控制面板 -->
    <div class="voice-panel" v-show="showPanel">
      <h3>🎤 智能语音助手</h3>
      <div class="voice-status">
        <div class="status-item">
          <span class="status-label">状态:</span>
          <span class="status-value" :class="statusClass">{{ voiceStatus }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">识别:</span>
          <span class="status-value">{{ recognizedText || '等待语音输入...' }}</span>
        </div>
        <div class="status-item" v-if="isProcessing">
          <span class="status-label">处理:</span>
          <div class="loading-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- 对话历史 -->
      <div class="conversation-history" v-if="conversationHistory.length > 0">
        <h4>对话记录</h4>
        <div class="history-list">
          <div
            v-for="(item, index) in conversationHistory.slice(-3)"
            :key="index"
            class="history-item"
          >
            <div class="user-message">
              <span class="message-icon">👤</span>
              <span class="message-text">{{ item.user }}</span>
            </div>
            <div class="ai-message" v-if="item.ai">
              <span class="message-icon">🤖</span>
              <span class="message-text">{{ item.ai }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷命令 -->
      <div class="quick-commands">
        <h4>快捷命令</h4>
        <div class="command-grid">
          <button
            v-for="command in quickCommands"
            :key="command.text"
            @click="executeCommand(command.action)"
            class="command-btn"
            :title="command.description"
          >
            {{ command.text }}
          </button>
        </div>
      </div>
    </div>

    <!-- 语音控制按钮 -->
    <div class="voice-controls">
      <button
        @click="toggleListening"
        class="voice-btn"
        :class="{
          'listening': isListening,
          'processing': isProcessing,
          'disabled': !isSupported
        }"
        :disabled="!isSupported"
      >
        <span class="btn-icon">
          {{ isListening ? '🔴' : (isProcessing ? '⏳' : '🎤') }}
        </span>
        <span class="btn-text">
          {{ isListening ? '停止录音' : (isProcessing ? '处理中...' : '开始语音') }}
        </span>
      </button>

      <button @click="togglePanel" class="panel-toggle-btn">
        {{ showPanel ? '隐藏面板' : '显示面板' }}
      </button>

      <button @click="clearHistory" class="clear-btn" v-if="conversationHistory.length > 0">
        清除记录
      </button>
    </div>

    <!-- 语音波形动画 -->
    <div class="voice-wave" v-show="isListening">
      <div class="wave-bar" v-for="i in 5" :key="i"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/login'
import axios from 'axios'

const router = useRouter()
const loginStore = useLoginStore()
const emit = defineEmits(['voiceCommand', 'voiceResponse'])

// 权限检查函数
const checkLoginStatus = () => {
  return loginStore.person125Info.state === true
}

const checkAdminStatus = () => {
  return loginStore.person125Info.state === true && loginStore.person125Info.role === 'admin'
}

const checkUserRole = () => {
  return loginStore.person125Info.role
}

// 响应式数据
const isSupported = ref(false)
const isListening = ref(false)
const isProcessing = ref(false)
const showPanel = ref(true)
const voiceStatus = ref('未初始化')
const recognizedText = ref('')
const conversationHistory = ref([])

// 语音识别相关
let recognition = null
let speechSynthesis = null

// 计算属性
const statusClass = computed(() => {
  switch (voiceStatus.value) {
    case '就绪': return 'status-ready'
    case '监听中': return 'status-listening'
    case '处理中': return 'status-processing'
    case '错误': return 'status-error'
    default: return 'status-default'
  }
})

// 快捷命令配置 - 增强医疗专业功能
const quickCommands = ref([
  // 导航功能
  { text: '🏠 数据大屏', action: 'navigate_home', description: '返回医疗数据可视化大屏' },
  { text: '👨‍⚕️ 医生查询', action: 'navigate_doctors', description: '查找专业医生进行咨询' },
  { text: '🏥 医院搜索', action: 'navigate_analytics', description: '搜索附近医院和导航' },
  { text: '🏃‍♂️ 康复训练', action: 'navigate_rehabilitation', description: '开始康复训练打卡（数据大屏）' },
  { text: '🤖 AI问诊', action: 'navigate_ai_consultation', description: '智能AI健康问诊' },
  { text: '👤 个人中心', action: 'navigate_personal', description: '查看个人信息和设置' },
  { text: '🔐 登录', action: 'navigate_login', description: '跳转到登录页面' },
  { text: '📝 注册', action: 'navigate_register', description: '跳转到注册页面' },
  { text: '⚙️ 管理后台', action: 'navigate_admin', description: '跳转到管理后台（管理员）' },

  // 医疗专业功能
  { text: '💬 健康咨询', action: 'health_consultation', description: '开始专业健康咨询对话' },
  { text: '🏥 附近医院', action: 'find_nearby_hospital', description: '查找附近的医院' },
  { text: '🚨 紧急求助', action: 'emergency_help', description: '紧急情况快速求助' },
  { text: '🔍 症状检查', action: 'symptom_check', description: 'AI辅助症状分析' },
  { text: '💊 用药提醒', action: 'medication_reminder', description: '设置用药提醒' },
  { text: '📰 健康资讯', action: 'navigate_news', description: '查看最新健康资讯' },

  // 系统控制功能
  { text: '🔍 放大显示', action: 'zoom_in', description: '放大页面内容' },
  { text: '🔎 缩小显示', action: 'zoom_out', description: '缩小页面内容' },
  { text: '↩️ 恢复大小', action: 'reset_zoom', description: '恢复正常显示大小' },
  { text: '🔄 刷新数据', action: 'refresh_data', description: '刷新页面获取最新数据' },
  { text: '⬆️ 返回顶部', action: 'scroll_top', description: '快速返回页面顶部' },
  { text: '⬇️ 滚动底部', action: 'scroll_bottom', description: '快速滚动到页面底部' },

  // 对话管理功能
  { text: '🗑️ 清除记录', action: 'clear_history', description: '清除对话历史记录' },
  { text: '🔁 重复回复', action: 'repeat_last', description: '重复上一次AI回复' },
  { text: '🔇 停止语音', action: 'stop_speech', description: '停止当前语音播报' },
  { text: '❓ 使用帮助', action: 'show_help', description: '查看系统使用帮助' }
])

// 初始化语音识别
const initializeSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang = 'zh-CN'
    recognition.maxAlternatives = 1

    recognition.onstart = () => {
      isListening.value = true
      voiceStatus.value = '监听中'
      recognizedText.value = ''
    }

    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscript += transcript
        }
      }

      recognizedText.value = finalTranscript || interimTranscript

      if (finalTranscript) {
        processVoiceCommand(finalTranscript)
      }
    }

    recognition.onerror = (event) => {
      console.error('语音识别错误:', event.error)
      voiceStatus.value = '错误'
      isListening.value = false
      isProcessing.value = false
    }

    recognition.onend = () => {
      isListening.value = false
      if (voiceStatus.value !== '处理中') {
        voiceStatus.value = '就绪'
      }
    }

    isSupported.value = true
    voiceStatus.value = '就绪'
  } else {
    console.warn('浏览器不支持语音识别')
    voiceStatus.value = '不支持'
    isSupported.value = false
  }
}

// 初始化语音合成
const initializeSpeechSynthesis = () => {
  if ('speechSynthesis' in window) {
    speechSynthesis = window.speechSynthesis
  }
}

// 处理语音命令
const processVoiceCommand = async (text) => {
  isProcessing.value = true
  voiceStatus.value = '处理中'

  try {
    // 添加到对话历史
    const conversationItem = { user: text, ai: '' }
    conversationHistory.value.push(conversationItem)

    // 检查是否为导航命令
    const navigationResult = handleNavigationCommands(text)
    if (navigationResult) {
      conversationItem.ai = navigationResult
      speak(navigationResult)
      return
    }

    // 检查是否为系统控制命令
    const systemResult = handleSystemCommands(text)
    if (systemResult) {
      conversationItem.ai = systemResult
      speak(systemResult)
      return
    }

    // 发送到后端AI进行处理
    const response = await sendToAI(text)
    conversationItem.ai = response

    // 语音播报回复
    speak(response)

    emit('voiceResponse', { question: text, answer: response })

  } catch (error) {
    console.error('处理语音命令失败:', error)
    const errorMsg = '抱歉，我现在无法处理您的请求，请稍后再试。'
    conversationHistory.value[conversationHistory.value.length - 1].ai = errorMsg
    speak(errorMsg)
  } finally {
    isProcessing.value = false
    voiceStatus.value = '就绪'
  }
}

// 处理导航命令 - 增强医疗专业功能
const handleNavigationCommands = (text) => {
  const navigationMap = {
    // 基础导航 - 公共页面
    '主页': { path: '/', message: '正在跳转到主页数据大屏', public: true },
    '首页': { path: '/', message: '正在跳转到首页数据大屏', public: true },
    '数据大屏': { path: '/', message: '正在显示医疗数据可视化大屏', public: true },
    '可视化': { path: '/', message: '正在显示医疗数据可视化大屏', public: true },
    '可视化大屏': { path: '/', message: '正在显示医疗数据可视化大屏', public: true },
    '大屏': { path: '/', message: '正在显示医疗数据可视化大屏', public: true },
    '数据': { path: '/', message: '正在显示医疗数据可视化大屏', public: true },
    '回到首页': { path: '/', message: '正在返回首页数据大屏', public: true },
    '返回首页': { path: '/', message: '正在返回首页数据大屏', public: true },

    // 医疗专业导航 - 需要登录
    '医生查询': { path: '/quary-doctor', message: '正在为您打开医生查询页面，寻找专业医生', requireLogin: true },
    '查询医生': { path: '/quary-doctor', message: '正在为您打开医生查询页面，寻找专业医生', requireLogin: true },
    '找医生': { path: '/quary-doctor', message: '正在为您查找合适的医生', requireLogin: true },
    '在线问诊': { path: '/quary-doctor', message: '正在为您打开在线问诊服务', requireLogin: true },
    '线上问诊': { path: '/quary-doctor', message: '正在为您打开在线问诊服务', requireLogin: true },
    '咨询医生': { path: '/quary-doctor', message: '正在为您连接专业医生进行咨询', requireLogin: true },
    '看医生': { path: '/quary-doctor', message: '正在为您打开在线问诊服务', requireLogin: true },
    '预约医生': { path: '/quary-doctor', message: '正在为您打开医生预约服务', requireLogin: true },

    // 康复训练相关 - 修正路由到个人中心
    '康复训练': { path: '/personal', message: '正在为您打开康复训练页面，开始健康之旅', requireLogin: true },
    '康复打卡': { path: '/personal', message: '正在为您打开康复打卡功能', requireLogin: true },
    '运动康复': { path: '/personal', message: '正在为您打开运动康复训练', requireLogin: true },
    '健身训练': { path: '/personal', message: '正在为您打开健身康复训练', requireLogin: true },

    // 智能问诊 - 修正路由
    '智能问诊': { path: '/intelligent-consultation', message: '正在为您打开AI智能问诊服务' },
    'AI问诊': { path: '/intelligent-consultation', message: '正在为您打开AI智能问诊服务' },
    '智能诊断': { path: '/intelligent-consultation', message: '正在为您打开AI智能诊断功能' },
    '智能咨询': { path: '/intelligent-consultation', message: '正在为您打开智能咨询服务' },

    // 医院搜索和健康分析
    '医院搜索': { path: '/health-analytics', message: '正在为您打开医院搜索功能' },
    '附近医院': { path: '/health-analytics', message: '正在为您搜索附近的医院' },
    '医院导航': { path: '/health-analytics', message: '正在为您打开医院导航服务' },
    '数据分析': { path: '/health-analytics', message: '正在跳转到健康数据分析页面' },
    '健康分析': { path: '/health-analytics', message: '正在跳转到健康数据分析页面' },

    // 个人中心
    '个人中心': { path: '/personal', message: '正在跳转到个人中心' },
    '个人信息': { path: '/personal', message: '正在跳转到个人信息页面' },
    '我的': { path: '/personal', message: '正在跳转到个人中心' },
    '个人资料': { path: '/personal', message: '正在跳转到个人资料页面' },

    // 其他功能
    '登录': { path: '/login', message: '正在跳转到登录页面' },
    '注册': { path: '/register', message: '正在跳转到注册页面' },
    '新闻': { path: '/news', message: '正在跳转到健康资讯页面' },
    '资讯': { path: '/news', message: '正在跳转到健康资讯页面' },
    '健康资讯': { path: '/news', message: '正在跳转到健康资讯页面' },

    // 管理后台功能（仅管理员可用）
    '管理后台': { path: '/guanli', message: '正在跳转到管理后台', requireAdmin: true },
    '后台管理': { path: '/guanli', message: '正在跳转到后台管理', requireAdmin: true },
    '系统管理': { path: '/guanli', message: '正在跳转到系统管理', requireAdmin: true },
    '管理员': { path: '/guanli', message: '正在跳转到管理员后台', requireAdmin: true },
    '管理': { path: '/guanli', message: '正在跳转到管理后台', requireAdmin: true }
  }

  // 精确匹配 - 增加权限检查
  for (const [keyword, config] of Object.entries(navigationMap)) {
    if (text.includes(keyword)) {
      // 检查是否需要登录权限
      if (config.requireLogin && !checkLoginStatus()) {
        return '抱歉，该功能需要登录后才能使用。请先登录您的账户。'
      }

      // 检查管理员权限
      if (config.requireAdmin && !checkAdminStatus()) {
        return '抱歉，该功能仅限管理员使用。'
      }

      try {
        router.push(config.path)
        emit('voiceCommand', { type: 'navigation', action: keyword, path: config.path })
        return config.message
      } catch (error) {
        console.error('导航错误:', error)
        return `跳转失败，请稍后重试。错误：${error.message}`
      }
    }
  }

  // 智能模糊匹配 - 增强版

  // 康复训练相关 - 需要登录
  if (text.includes('训练') || text.includes('锻炼') || text.includes('运动') || text.includes('康复') ||
      text.includes('健身') || text.includes('体能') || text.includes('打卡')) {
    if (!checkLoginStatus()) {
      return '抱歉，康复训练功能需要登录后才能使用。请先登录您的账户。'
    }
    try {
      router.push('/personal')
      emit('voiceCommand', { type: 'navigation', action: '康复训练', path: '/personal' })
      return '正在为您打开康复训练页面，开始您的健康康复之旅！'
    } catch (error) {
      return '跳转康复训练页面失败，请稍后重试。'
    }
  }

  // 问诊相关 - 需要登录
  if (text.includes('问诊') || text.includes('咨询') || text.includes('看病') || text.includes('就医') ||
      text.includes('诊断') || text.includes('治疗') || text.includes('症状') || text.includes('病情')) {
    if (!checkLoginStatus()) {
      return '抱歉，在线问诊功能需要登录后才能使用。请先登录您的账户。'
    }
    try {
      router.push('/quary-doctor')
      emit('voiceCommand', { type: 'navigation', action: '在线问诊', path: '/quary-doctor' })
      return '正在为您打开在线问诊页面，连接专业医生为您提供服务！'
    } catch (error) {
      return '跳转在线问诊页面失败，请稍后重试。'
    }
  }

  // AI智能问诊相关 - 需要登录
  if ((text.includes('AI') || text.includes('智能') || text.includes('机器人')) &&
      (text.includes('问诊') || text.includes('咨询') || text.includes('诊断'))) {
    if (!checkLoginStatus()) {
      return '抱歉，AI智能问诊功能需要登录后才能使用。请先登录您的账户。'
    }
    try {
      router.push('/intelligent-consultation')
      emit('voiceCommand', { type: 'navigation', action: 'AI智能问诊', path: '/intelligent-consultation' })
      return '正在为您打开AI智能问诊服务，人工智能医生为您提供专业建议！'
    } catch (error) {
      return '跳转AI智能问诊页面失败，请稍后重试。'
    }
  }

  // 医院搜索相关 - 需要登录
  if (text.includes('医院') && (text.includes('搜索') || text.includes('查找') || text.includes('附近') ||
      text.includes('导航') || text.includes('位置') || text.includes('地图'))) {
    if (!checkLoginStatus()) {
      return '抱歉，医院搜索功能需要登录后才能使用。请先登录您的账户。'
    }
    try {
      router.push('/health-analytics')
      emit('voiceCommand', { type: 'navigation', action: '医院搜索', path: '/health-analytics' })
      return '正在为您打开医院搜索功能，帮您找到最合适的医院！'
    } catch (error) {
      return '跳转医院搜索页面失败，请稍后重试。'
    }
  }

  // 个人中心相关 - 需要登录
  if (text.includes('个人') && (text.includes('中心') || text.includes('信息') || text.includes('资料') ||
      text.includes('设置') || text.includes('账户'))) {
    if (!checkLoginStatus()) {
      return '抱歉，个人中心功能需要登录后才能使用。请先登录您的账户。'
    }
    try {
      router.push('/personal')
      emit('voiceCommand', { type: 'navigation', action: '个人中心', path: '/personal' })
      return '正在为您打开个人中心，管理您的个人信息和设置！'
    } catch (error) {
      return '跳转个人中心页面失败，请稍后重试。'
    }
  }

  // 登录注册相关
  if (text.includes('登录') || text.includes('登陆') || text.includes('sign in')) {
    try {
      router.push('/login')
      emit('voiceCommand', { type: 'navigation', action: '登录', path: '/login' })
      return '正在为您打开登录页面，请输入您的账户信息。'
    } catch (error) {
      return '跳转登录页面失败，请稍后重试。'
    }
  }

  if (text.includes('注册') || text.includes('sign up') || text.includes('创建账户')) {
    try {
      router.push('/register')
      emit('voiceCommand', { type: 'navigation', action: '注册', path: '/register' })
      return '正在为您打开注册页面，创建您的新账户。'
    } catch (error) {
      return '跳转注册页面失败，请稍后重试。'
    }
  }

  return null
}

// 处理系统控制命令 - 增强智能化功能
const handleSystemCommands = (text) => {
  // 显示控制
  if (text.includes('放大') || text.includes('zoom in') || text.includes('放大显示')) {
    emit('voiceCommand', { type: 'system', action: 'zoom_in' })
    document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString()
    return '正在为您放大显示内容，提升阅读体验'
  }

  if (text.includes('缩小') || text.includes('zoom out') || text.includes('缩小显示')) {
    emit('voiceCommand', { type: 'system', action: 'zoom_out' })
    document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString()
    return '正在为您缩小显示内容'
  }

  if (text.includes('恢复') && text.includes('大小')) {
    emit('voiceCommand', { type: 'system', action: 'reset_zoom' })
    document.body.style.zoom = '1'
    return '已恢复正常显示大小'
  }

  // 页面控制
  if (text.includes('刷新') || text.includes('更新') || text.includes('重新加载')) {
    emit('voiceCommand', { type: 'system', action: 'refresh' })
    location.reload()
    return '正在为您刷新页面，获取最新数据'
  }

  if (text.includes('返回顶部') || text.includes('回到顶部') || text.includes('页面顶部')) {
    emit('voiceCommand', { type: 'system', action: 'scroll_top' })
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return '正在为您返回页面顶部'
  }

  if (text.includes('滚动到底部') || text.includes('页面底部')) {
    emit('voiceCommand', { type: 'system', action: 'scroll_bottom' })
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
    return '正在为您滚动到页面底部'
  }

  // 对话记录管理
  if (text.includes('清除') && text.includes('记录')) {
    clearHistory()
    return '已为您清除对话记录'
  }

  if (text.includes('清除') && text.includes('历史')) {
    clearHistory()
    return '已为您清除对话历史'
  }

  // 语音控制
  if (text.includes('停止') && text.includes('语音')) {
    if (speechSynthesis) {
      speechSynthesis.cancel()
    }
    return '已停止语音播报'
  }

  if (text.includes('重复') || text.includes('再说一遍')) {
    const lastAI = conversationHistory.value[conversationHistory.value.length - 1]?.ai
    if (lastAI) {
      speak(lastAI)
      return '正在为您重复上一次回复'
    }
    return '没有可重复的内容'
  }

  // 智能助手状态
  if (text.includes('帮助') || text.includes('使用说明') || text.includes('怎么用')) {
    const helpText = '我是您的智能医疗助手，可以帮您：1.导航到各个功能页面 2.搜索医生和医院 3.提供健康咨询 4.控制页面显示。您可以说"找医生"、"附近医院"、"康复训练"等指令。'
    speak(helpText)
    return helpText
  }

  if (text.includes('你好') || text.includes('您好')) {
    const greeting = '您好！我是医慧之翼智能助手，很高兴为您服务。我可以帮您导航、查找医生、搜索医院，还可以回答健康相关问题。请告诉我您需要什么帮助？'
    return greeting
  }

  // 功能介绍
  if (text.includes('功能') && text.includes('介绍')) {
    const features = '医慧之翼系统包含：数据可视化大屏、在线问诊、医院搜索、康复训练、智能问诊、个人中心等功能。您可以通过语音命令快速访问这些功能。'
    return features
  }

  return null
}

// 发送到AI后端
const sendToAI = async (text) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/chat', {
      message: text,
      name: '',
      location: '',
      problem: ''
    })

    return response.data.response || '抱歉，我没有理解您的问题。'
  } catch (error) {
    console.error('AI请求失败:', error)
    throw new Error('AI服务暂时不可用')
  }
}

// 清理Markdown格式用于语音播报
const cleanTextForSpeech = (text) => {
  if (!text) return ''

  let cleanText = String(text)

  // 移除Markdown标题符号 (# ## ### 等)
  cleanText = cleanText.replace(/^#{1,6}\s+/gm, '')

  // 移除Markdown粗体和斜体 (**text** *text*)
  cleanText = cleanText.replace(/\*\*([^*]+)\*\*/g, '$1')
  cleanText = cleanText.replace(/\*([^*]+)\*/g, '$1')

  // 移除Markdown代码块 (```code```)
  cleanText = cleanText.replace(/```[\s\S]*?```/g, '代码块')
  cleanText = cleanText.replace(/`([^`]+)`/g, '$1')

  // 移除Markdown链接 [text](url)
  cleanText = cleanText.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')

  // 移除Markdown列表符号 (- * +)
  cleanText = cleanText.replace(/^[\s]*[-*+]\s+/gm, '')

  // 移除Markdown数字列表 (1. 2. 3.)
  cleanText = cleanText.replace(/^[\s]*\d+\.\s+/gm, '')

  // 移除Markdown引用符号 (>)
  cleanText = cleanText.replace(/^>\s+/gm, '')

  // 移除Markdown分割线 (--- ***)
  cleanText = cleanText.replace(/^[-*]{3,}$/gm, '')

  // 移除HTML标签
  cleanText = cleanText.replace(/<[^>]*>/g, '')

  // 移除多余的空白字符
  cleanText = cleanText.replace(/\s+/g, ' ').trim()

  // 替换一些特殊符号为更自然的语音
  cleanText = cleanText.replace(/&nbsp;/g, ' ')
  cleanText = cleanText.replace(/&amp;/g, '和')
  cleanText = cleanText.replace(/&lt;/g, '小于')
  cleanText = cleanText.replace(/&gt;/g, '大于')

  return cleanText
}

// 语音播报 - 增强版
const speak = (text) => {
  if (speechSynthesis && text) {
    // 停止当前播报
    speechSynthesis.cancel()

    // 清理Markdown格式
    const cleanText = cleanTextForSpeech(text)

    // 如果清理后的文本为空，则不播报
    if (!cleanText.trim()) {
      console.log('清理后的文本为空，跳过语音播报')
      return
    }

    // 限制播报长度，避免过长的文本
    const maxLength = 300
    const textToSpeak = cleanText.length > maxLength
      ? cleanText.substring(0, maxLength) + '...'
      : cleanText

    const utterance = new SpeechSynthesisUtterance(textToSpeak)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1
    utterance.volume = 0.8

    // 播报错误处理
    utterance.onerror = (event) => {
      console.error('语音播报错误:', event.error)
    }

    console.log('VoiceInteraction 原始文本:', text)
    console.log('VoiceInteraction 清理后文本:', textToSpeak)

    speechSynthesis.speak(utterance)
  }
}

// 控制函数
const toggleListening = () => {
  if (!isSupported.value) return

  if (isListening.value) {
    recognition.stop()
  } else {
    recognition.start()
  }
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
}

const clearHistory = () => {
  conversationHistory.value = []
}

const executeCommand = (action) => {
  const commandMap = {
    // 导航命令
    'navigate_home': () => {
      router.push('/')
      speak('正在跳转到数据可视化大屏')
    },
    'navigate_doctors': () => {
      router.push('/quary-doctor')
      speak('正在为您打开医生查询页面')
    },
    'navigate_personal': () => {
      router.push('/personal')
      speak('正在跳转到个人中心')
    },
    'navigate_dashboard': () => {
      router.push('/')
      speak('正在显示医疗数据大屏')
    },
    'navigate_analytics': () => {
      router.push('/health-analytics')
      speak('正在打开健康数据分析页面')
    },
    'navigate_rehabilitation': () => {
      if (!checkLoginStatus()) {
        speak('抱歉，康复训练功能需要登录后才能使用')
        return
      }
      router.push('/personal')
      speak('正在为您打开康复训练页面')
    },
    'navigate_ai_consultation': () => {
      router.push('/intelligent-consultation')
      speak('正在为您打开AI智能问诊')
    },
    'navigate_news': () => {
      router.push('/news')
      speak('正在跳转到健康资讯页面')
    },
    'navigate_login': () => {
      router.push('/login')
      speak('正在跳转到登录页面')
    },
    'navigate_register': () => {
      router.push('/register')
      speak('正在跳转到注册页面')
    },
    'navigate_admin': () => {
      router.push('/guanli')
      speak('正在跳转到管理后台')
    },

    // 系统控制命令
    'zoom_in': () => {
      document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString()
      emit('voiceCommand', { type: 'system', action: 'zoom_in' })
      speak('正在为您放大显示')
    },
    'zoom_out': () => {
      document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString()
      emit('voiceCommand', { type: 'system', action: 'zoom_out' })
      speak('正在为您缩小显示')
    },
    'reset_zoom': () => {
      document.body.style.zoom = '1'
      emit('voiceCommand', { type: 'system', action: 'reset_zoom' })
      speak('已恢复正常显示大小')
    },
    'refresh_data': () => {
      location.reload()
      speak('正在刷新页面数据')
    },
    'scroll_top': () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
      speak('正在返回页面顶部')
    },
    'scroll_bottom': () => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
      speak('正在滚动到页面底部')
    },

    // 医疗专业功能
    'health_consultation': () => {
      recognizedText.value = '我想进行健康咨询'
      processVoiceCommand('我想进行健康咨询')
    },
    'find_nearby_hospital': () => {
      recognizedText.value = '帮我找附近的医院'
      processVoiceCommand('帮我找附近的医院')
    },
    'emergency_help': () => {
      recognizedText.value = '紧急情况，需要帮助'
      processVoiceCommand('紧急情况，需要帮助')
    },
    'symptom_check': () => {
      recognizedText.value = '我想检查症状'
      processVoiceCommand('我想检查症状')
    },
    'medication_reminder': () => {
      recognizedText.value = '提醒我吃药'
      processVoiceCommand('提醒我吃药')
    },

    // 对话管理
    'clear_history': () => {
      clearHistory()
      speak('已清除对话记录')
    },
    'repeat_last': () => {
      const lastAI = conversationHistory.value[conversationHistory.value.length - 1]?.ai
      if (lastAI) {
        speak(lastAI)
      } else {
        speak('没有可重复的内容')
      }
    },
    'stop_speech': () => {
      if (speechSynthesis) {
        speechSynthesis.cancel()
      }
      speak('已停止语音播报')
    },

    // 帮助功能
    'show_help': () => {
      const helpText = '我是您的智能医疗助手，可以帮您导航、查找医生、搜索医院、提供健康咨询。请告诉我您需要什么帮助？'
      speak(helpText)
    }
  }

  const command = commandMap[action]
  if (command) {
    command()
  }
}

// 生命周期
onMounted(() => {
  initializeSpeechRecognition()
  initializeSpeechSynthesis()
})

onUnmounted(() => {
  if (recognition) {
    recognition.stop()
  }
  if (speechSynthesis) {
    speechSynthesis.cancel()
  }
})
</script>

<style scoped>
.voice-interaction {
  position: relative;
  z-index: 1001;
}

.voice-panel {
  position: fixed;
  top: 20px;
  left: 20px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
  color: white;
  padding: 20px;
  border-radius: 15px;
  min-width: 320px;
  max-width: 400px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.voice-panel h3 {
  margin: 0 0 15px 0;
  color: #00ff88;
  font-size: 18px;
  text-align: center;
}

.voice-panel h4 {
  margin: 15px 0 10px 0;
  color: #88ccff;
  font-size: 14px;
}

.voice-status {
  margin-bottom: 15px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
  font-size: 14px;
}

.status-label {
  color: #aaa;
  min-width: 50px;
}

.status-value {
  flex: 1;
  text-align: right;
}

.status-ready { color: #00ff88; }
.status-listening { color: #ffaa00; }
.status-processing { color: #0088ff; }
.status-error { color: #ff4444; }
.status-default { color: #888; }

.loading-dots {
  display: flex;
  gap: 3px;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: #0088ff;
  border-radius: 50%;
  animation: loading 1.4s infinite ease-in-out;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes loading {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.conversation-history {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 15px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

.user-message,
.ai-message {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 5px 0;
}

.message-icon {
  font-size: 16px;
  min-width: 20px;
}

.message-text {
  font-size: 13px;
  line-height: 1.4;
  word-break: break-word;
}

.user-message .message-text {
  color: #88ccff;
}

.ai-message .message-text {
  color: #ccffcc;
}

.quick-commands {
  margin-top: 15px;
}

.command-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.command-btn {
  padding: 8px 12px;
  background: linear-gradient(45deg, #0066cc, #0088ff);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.command-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(0, 136, 255, 0.3);
}

.voice-controls {
  position: fixed;
  bottom: 60px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1002;
}

.voice-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
  min-width: 160px;
}

.voice-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
}

.voice-btn.listening {
  background: linear-gradient(45deg, #ff4444, #ff6666);
  animation: pulse 1.5s infinite;
}

.voice-btn.processing {
  background: linear-gradient(45deg, #0088ff, #00aaff);
}

.voice-btn.disabled {
  background: #666;
  cursor: not-allowed;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0); }
}

.panel-toggle-btn,
.clear-btn {
  padding: 10px 15px;
  background: linear-gradient(45deg, #666, #888);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.panel-toggle-btn:hover,
.clear-btn:hover {
  transform: translateY(-1px);
  background: linear-gradient(45deg, #777, #999);
}

.voice-wave {
  position: fixed;
  bottom: 180px;
  left: 50px;
  display: flex;
  align-items: end;
  gap: 3px;
  height: 40px;
  z-index: 1002;
}

.wave-bar {
  width: 4px;
  background: linear-gradient(to top, #ff6b6b, #ff8e8e);
  border-radius: 2px;
  animation: wave 1s infinite ease-in-out;
}

.wave-bar:nth-child(1) { animation-delay: 0s; }
.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
.wave-bar:nth-child(4) { animation-delay: 0.3s; }
.wave-bar:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% { height: 10px; }
  50% { height: 40px; }
}
</style>
