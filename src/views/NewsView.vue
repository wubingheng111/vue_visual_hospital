<template>
  <div class="intelligent-consultation">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="consultation-avatar">
          <div class="avatar-circle">
            <span class="avatar-icon">🤖</span>
          </div>
          <div class="avatar-status" :class="{ online: isOnline, offline: !isOnline }"></div>
        </div>
        <div class="header-text">
          <h1 class="page-title">
            <span class="title-icon">🩺</span>
            AI专业医生问诊
          </h1>
          <p class="page-subtitle">专业AI医生24小时在线，提供个性化医疗咨询与健康指导</p>
        </div>
        <div class="consultation-status">
          <div class="status-indicator" :class="{ active: isOnline }">
            <span class="status-dot"></span>
            {{ isOnline ? 'AI医生在线' : 'AI医生离线' }}
          </div>
        </div>
      </div>

      <!-- 功能状态栏 -->
      <div class="status-bar">
        <div class="status-card">
          <div class="status-icon">👨‍⚕️</div>
          <div class="status-info">
            <div class="status-label">AI医生</div>
            <div class="status-value">在线服务</div>
          </div>
        </div>
        <div class="status-card">
          <div class="status-icon">💬</div>
          <div class="status-info">
            <div class="status-label">今日咨询</div>
            <div class="status-value">{{ todayConsultations }}</div>
          </div>
        </div>
        <div class="status-card">
          <div class="status-icon">🎤</div>
          <div class="status-info">
            <div class="status-label">语音对话</div>
            <div class="status-value">{{ isVoiceActive ? '进行中' : '可用' }}</div>
          </div>
        </div>
        <div class="status-card">
          <div class="status-icon">📊</div>
          <div class="status-info">
            <div class="status-label">诊断准确率</div>
            <div class="status-value">{{ diagnosticAccuracy }}%</div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧：用户信息表单 -->
      <div class="left-panel">
        <div class="doctor-profile-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">👨‍⚕️</span>
              您的AI医生
            </h3>
            <div class="doctor-status">
              <span class="status-badge online">
                ✅ 在线服务中
              </span>
            </div>
          </div>

          <div class="card-content">
            <div class="doctor-info">
              <div class="doctor-avatar-large">
                <div class="avatar-circle">
                  <span class="avatar-icon">🤖</span>
                </div>
                <div class="doctor-specialty">AI全科医生</div>
              </div>

              <div class="doctor-details">
                <h4>Dr. AI Assistant</h4>
                <p class="doctor-title">人工智能医疗专家</p>
                <div class="doctor-capabilities">
                  <div class="capability-item">
                    <span class="capability-icon">🧠</span>
                    <span>智能诊断分析</span>
                  </div>
                  <div class="capability-item">
                    <span class="capability-icon">💊</span>
                    <span>用药指导建议</span>
                  </div>
                  <div class="capability-item">
                    <span class="capability-icon">🔬</span>
                    <span>检查项目推荐</span>
                  </div>
                  <div class="capability-item">
                    <span class="capability-icon">🏥</span>
                    <span>就医路径规划</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="consultation-options">
              <h5>咨询方式</h5>
              <div class="option-buttons">
                <button
                  @click="startTextConsultation"
                  class="option-btn"
                  :class="{ active: consultationMode === 'text' }"
                >
                  <span class="btn-icon">💬</span>
                  文字咨询
                </button>
                <button
                  @click="startVoiceConsultation"
                  class="option-btn"
                  :class="{ active: consultationMode === 'voice' }"
                >
                  <span class="btn-icon">🎤</span>
                  语音对话
                </button>
              </div>
            </div>

            <div class="patient-info-section">
              <h5>患者信息 (可选)</h5>
              <div class="info-grid">
                <div class="info-item">
                  <label>称呼</label>
                  <input v-model="patientInfo.name" placeholder="如：张先生" class="info-input" />
                </div>
                <div class="info-item">
                  <label>年龄</label>
                  <input v-model="patientInfo.age" placeholder="如：30岁" class="info-input" />
                </div>
                <div class="info-item">
                  <label>性别</label>
                  <select v-model="patientInfo.gender" class="info-select">
                    <option value="">请选择</option>
                    <option value="male">男</option>
                    <option value="female">女</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 专业医疗工具 -->
        <div class="medical-tools-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">🔬</span>
              专业医疗工具
            </h3>
          </div>
          <div class="card-content">
            <div class="tool-buttons">
              <button @click="openSymptomChecker" class="tool-btn">
                <span class="tool-icon">🩺</span>
                <div class="tool-info">
                  <div class="tool-name">症状自查</div>
                  <div class="tool-desc">智能症状分析</div>
                </div>
              </button>

              <button @click="openHealthAssessment" class="tool-btn">
                <span class="tool-icon">📊</span>
                <div class="tool-info">
                  <div class="tool-name">健康评估</div>
                  <div class="tool-desc">综合健康检查</div>
                </div>
              </button>

              <button @click="openMedicationGuide" class="tool-btn">
                <span class="tool-icon">💊</span>
                <div class="tool-info">
                  <div class="tool-name">用药指导</div>
                  <div class="tool-desc">安全用药建议</div>
                </div>
              </button>

              <button @click="openEmergencyGuide" class="tool-btn emergency">
                <span class="tool-icon">🚨</span>
                <div class="tool-info">
                  <div class="tool-name">急救指导</div>
                  <div class="tool-desc">紧急情况处理</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- 常见症状快速咨询 -->
        <div class="quick-consultation-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">⚡</span>
              常见症状快速咨询
            </h3>
          </div>
          <div class="card-content">
            <div class="symptom-categories">
              <div class="category-section">
                <h6>呼吸系统</h6>
                <div class="symptom-tags">
                  <button @click="quickConsult('咳嗽')" class="symptom-tag">咳嗽</button>
                  <button @click="quickConsult('胸闷')" class="symptom-tag">胸闷</button>
                  <button @click="quickConsult('气喘')" class="symptom-tag">气喘</button>
                </div>
              </div>

              <div class="category-section">
                <h6>消化系统</h6>
                <div class="symptom-tags">
                  <button @click="quickConsult('腹痛')" class="symptom-tag">腹痛</button>
                  <button @click="quickConsult('恶心')" class="symptom-tag">恶心</button>
                  <button @click="quickConsult('腹泻')" class="symptom-tag">腹泻</button>
                </div>
              </div>

              <div class="category-section">
                <h6>神经系统</h6>
                <div class="symptom-tags">
                  <button @click="quickConsult('头痛')" class="symptom-tag">头痛</button>
                  <button @click="quickConsult('头晕')" class="symptom-tag">头晕</button>
                  <button @click="quickConsult('失眠')" class="symptom-tag">失眠</button>
                </div>
              </div>

              <div class="category-section">
                <h6>全身症状</h6>
                <div class="symptom-tags">
                  <button @click="quickConsult('发热')" class="symptom-tag">发热</button>
                  <button @click="quickConsult('乏力')" class="symptom-tag">乏力</button>
                  <button @click="quickConsult('疼痛')" class="symptom-tag">疼痛</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：聊天对话区域 -->
      <div class="right-panel">
        <div class="chat-container">
          <!-- 聊天头部 -->
          <div class="chat-header">
            <div class="doctor-info">
              <div class="doctor-avatar">
                <div class="avatar-circle">
                  <span class="avatar-icon">👨‍⚕️</span>
                </div>
                <div class="avatar-status online"></div>
              </div>
              <div class="doctor-details">
                <h4 class="doctor-name">Dr. AI Assistant</h4>
                <p class="doctor-status">
                  <span class="online-dot"></span>
                  专业AI医生 · 24小时在线 · {{ consultationMode === 'voice' ? '语音对话中' : '文字咨询中' }}
                </p>
              </div>
            </div>
            <div class="chat-actions">
              <button @click="toggleVoiceMode" class="action-btn" :class="{ active: consultationMode === 'voice' }" title="语音模式">
                <span>{{ consultationMode === 'voice' ? '🔴' : '🎤' }}</span>
              </button>
              <button @click="toggleStreamMode" class="action-btn" :title="`流式输出: ${getStreamModeText()}`">
                <span>{{ getStreamModeIcon() }}</span>
              </button>
              <button @click="toggleConversationStyle" class="action-btn" :class="{ active: conversationStyle === 'natural' }" :title="`对话风格: ${getConversationStyleText()}`">
                <span>{{ getConversationStyleIcon() }}</span>
              </button>
              <button @click="saveConsultationRecord" class="action-btn" title="保存病历">
                <span>💾</span>
              </button>
              <button @click="exportConsultation" class="action-btn" title="导出咨询记录">
                <span>📄</span>
              </button>
              <button @click="clearChat" class="action-btn" title="清空对话">
                <span>🗑️</span>
              </button>
            </div>
          </div>

          <!-- 聊天历史 -->
          <div class="chat-history" ref="chatHistoryRef">
            <div v-if="chatHistory.length === 0" class="welcome-message">
              <div class="welcome-content">
                <div class="doctor-welcome-avatar">
                  <div class="avatar-circle">
                    <span class="avatar-icon">👨‍⚕️</span>
                  </div>
                </div>
                <h3>您好，我是您的专属AI医生</h3>
                <p>很高兴为您提供专业的医疗咨询服务。我具备丰富的医学知识，可以为您提供：</p>
                <div class="medical-services">
                  <div class="service-item">
                    <span class="service-icon">🧠</span>
                    <div class="service-info">
                      <strong>智能诊断分析</strong>
                      <span>基于症状进行专业分析</span>
                    </div>
                  </div>
                  <div class="service-item">
                    <span class="service-icon">💊</span>
                    <div class="service-info">
                      <strong>用药指导建议</strong>
                      <span>安全用药与药物相互作用</span>
                    </div>
                  </div>
                  <div class="service-item">
                    <span class="service-icon">🔬</span>
                    <div class="service-info">
                      <strong>检查项目推荐</strong>
                      <span>建议必要的医学检查</span>
                    </div>
                  </div>
                  <div class="service-item">
                    <span class="service-icon">🏥</span>
                    <div class="service-info">
                      <strong>就医路径规划</strong>
                      <span>科室选择与就医时机</span>
                    </div>
                  </div>
                </div>
                <div class="consultation-start">
                  <p class="start-prompt">请详细描述您的症状，我会为您提供专业的医疗建议：</p>
                  <div class="quick-start-buttons">
                    <button @click="quickConsult('头痛')" class="quick-start-btn">头痛咨询</button>
                    <button @click="quickConsult('发热')" class="quick-start-btn">发热咨询</button>
                    <button @click="quickConsult('咳嗽')" class="quick-start-btn">咳嗽咨询</button>
                    <button @click="quickConsult('腹痛')" class="quick-start-btn">腹痛咨询</button>
                  </div>
                </div>
                <div class="medical-disclaimer">
                  <span class="disclaimer-icon">⚕️</span>
                  <span><strong>医疗声明：</strong>本AI医生基于大量医学知识训练，建议仅供参考。如有紧急情况或严重症状，请立即前往医院就诊。</span>
                </div>
              </div>
            </div>

            <div v-for="(msg, index) in chatHistory" :key="index" class="message-wrapper">
              <div
                class="message"
                :class="{ 'user-message': msg.sender === 'You', 'bot-message': msg.sender === 'Bot' }"
                :data-stream-id="msg.streamId"
              >
                <div class="message-avatar">
                  <span v-if="msg.sender === 'You'">👤</span>
                  <span v-else>🤖</span>
                </div>
                <div class="message-content">
                  <div class="message-header">
                    <span class="sender-name">{{ msg.sender === 'You' ? '您' : 'AI医生' }}</span>
                    <span class="message-time">{{ msg.timestamp }}</span>
                  </div>
                  <div class="message-text-container">
                    <div class="message-text" v-html="formatMessage(msg.text)"></div>
                    <!-- 流式输出指示器 -->
                    <span v-if="msg.isStreaming" class="streaming-cursor">|</span>
                  </div>
                  <div v-if="msg.sender === 'Bot' && msg.actions" class="message-actions">
                    <button
                      v-for="action in msg.actions"
                      :key="action.text"
                      @click="handleAction(action)"
                      class="action-button"
                    >
                      {{ action.text }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 正在输入指示器 -->
            <div v-if="isTyping" class="typing-indicator">
              <div class="message bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                  <div class="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span class="typing-text">AI医生正在思考中...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <div class="input-container">
              <div class="input-wrapper">
                <textarea
                  v-model="message"
                  class="message-input"
                  placeholder="请输入您的问题..."
                  rows="1"
                  @keydown.enter.prevent="handleEnterKey"
                  @input="adjustTextareaHeight"
                  ref="messageInput"
                ></textarea>
                <div class="input-actions">
                  <button
                    @click="toggleVoiceInput"
                    class="voice-btn"
                    :class="{
                      active: isVoiceActive,
                      listening: isVoiceActive
                    }"
                    :title="isVoiceActive ? '点击停止语音输入' : '点击开始语音输入'"
                  >
                    <span>{{ isVoiceActive ? '🔴' : '🎤' }}</span>
                    <span class="voice-status" v-if="isVoiceActive">录音中...</span>
                  </button>
                  <button @click="sendMessage" class="send-btn" :disabled="!message.trim() || isSending">
                    <span v-if="isSending">⏳</span>
                    <span v-else>📤</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- 快速回复 -->
            <div class="quick-replies" v-if="quickReplies.length > 0">
              <button
                v-for="reply in quickReplies"
                :key="reply"
                @click="sendQuickReply(reply)"
                class="quick-reply-btn"
              >
                {{ reply }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 智能交互组件 -->
    <GestureControl
      @navigationGesture="handleNavigationGesture"
    />
    <VoiceInteraction
      @voiceCommand="handleVoiceCommand"
      @voiceResponse="handleVoiceResponse"
    />

    <!-- 紧急情况弹窗 -->
    <div v-if="showEmergencyModal" class="emergency-modal">
      <div class="modal-content">
        <div class="emergency-icon">🚨</div>
        <h3>紧急情况提醒</h3>
        <p>根据您的描述，建议立即就医或拨打急救电话！</p>
        <div class="emergency-actions">
          <button @click="call120" class="emergency-btn">📞 拨打120</button>
          <button @click="findNearbyHospital" class="emergency-btn">🏥 附近医院</button>
          <button @click="closeEmergencyModal" class="cancel-btn">我知道了</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import axios from 'axios'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import GestureControl from '@/components/GestureControl.vue'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

// 响应式数据
const message = ref('')
const chatHistory = ref([]) // 确保初始化为空数组
const isTyping = ref(false)
const isSending = ref(false)
const isSubmitting = ref(false)
const isOnline = ref(true)
const isVoiceActive = ref(false)
const showEmergencyModal = ref(false)
const todayConsultations = ref(1247)
const diagnosticAccuracy = ref(94)
const consultationMode = ref('text') // 'text' 或 'voice'
const conversationStyle = ref('natural') // 'natural' 或 'formal'

// 表单数据
const formData = ref({
  name: '',
  location: '',
  problem: '',
  urgency: 'low'
})

// 患者信息
const patientInfo = ref({
  name: '',
  age: '',
  gender: ''
})

// 常见症状
const commonSymptoms = ref([
  '头痛', '发热', '咳嗽', '腹痛', '胸痛', '呼吸困难',
  '恶心呕吐', '腹泻', '失眠', '头晕', '皮疹', '关节痛'
])

// 智能快速回复系统
const quickReplies = ref([])

// 基础快速回复模板
const baseQuickReplies = [
  '症状持续多久了？',
  '有其他伴随症状吗？',
  '之前有类似情况吗？',
  '目前在服用什么药物？',
  '疼痛程度如何？',
  '什么时候症状最严重？'
]

// 智能建议系统
const smartSuggestions = ref({
  enabled: true,
  suggestions: [],
  lastUserMessage: '',
  context: []
})

// 根据对话内容生成智能建议
const generateSmartSuggestions = (userMessage, botResponse) => {
  const suggestions = []
  const lowerMessage = userMessage.toLowerCase()
  const lowerResponse = botResponse.toLowerCase()

  // 基于症状的建议
  if (lowerMessage.includes('头痛') || lowerMessage.includes('头疼')) {
    suggestions.push('头痛的具体位置在哪里？')
    suggestions.push('头痛时有恶心呕吐吗？')
    suggestions.push('最近有熬夜或压力大吗？')
  }

  if (lowerMessage.includes('发热') || lowerMessage.includes('发烧')) {
    suggestions.push('体温具体是多少度？')
    suggestions.push('发热时有寒战吗？')
    suggestions.push('有咳嗽或其他症状吗？')
  }

  if (lowerMessage.includes('咳嗽')) {
    suggestions.push('咳嗽时有痰吗？')
    suggestions.push('痰的颜色是什么样的？')
    suggestions.push('咳嗽在什么时候最严重？')
  }

  if (lowerMessage.includes('腹痛') || lowerMessage.includes('肚子疼')) {
    suggestions.push('腹痛的具体位置在哪里？')
    suggestions.push('疼痛是持续性还是阵发性？')
    suggestions.push('有恶心呕吐或腹泻吗？')
  }

  // 基于AI回复的建议
  if (lowerResponse.includes('建议') || lowerResponse.includes('检查')) {
    suggestions.push('我需要做哪些检查？')
    suggestions.push('检查费用大概多少？')
    suggestions.push('什么时候去检查比较好？')
  }

  if (lowerResponse.includes('药物') || lowerResponse.includes('用药')) {
    suggestions.push('这个药有什么副作用？')
    suggestions.push('需要服用多长时间？')
    suggestions.push('有什么注意事项？')
  }

  if (lowerResponse.includes('医院') || lowerResponse.includes('就诊')) {
    suggestions.push('应该挂什么科室？')
    suggestions.push('需要空腹去医院吗？')
    suggestions.push('附近有推荐的医院吗？')
  }

  // 通用建议
  if (suggestions.length === 0) {
    suggestions.push(...baseQuickReplies.slice(0, 3))
  }

  // 限制建议数量
  return suggestions.slice(0, 4)
}

// 更新快速回复
const updateQuickReplies = (userMessage = '', botResponse = '') => {
  if (smartSuggestions.value.enabled && userMessage && botResponse) {
    const newSuggestions = generateSmartSuggestions(userMessage, botResponse)
    quickReplies.value = newSuggestions
    smartSuggestions.value.suggestions = newSuggestions
    smartSuggestions.value.lastUserMessage = userMessage
  } else {
    // 使用基础快速回复
    quickReplies.value = baseQuickReplies.slice(0, 4)
  }
}

// 引用
const chatHistoryRef = ref(null)
const messageInput = ref(null)

// 配置Markdown解析器
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.warn('代码高亮失败:', err)
      }
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true, // 支持换行
  gfm: true,    // 支持GitHub风格Markdown
  sanitize: false // 允许HTML（注意：生产环境需要谨慎使用）
})

// 计算属性
const isFormValid = computed(() => {
  return formData.value.name.trim() &&
         formData.value.location.trim() &&
         formData.value.problem.trim()
})

// 格式化时间
const formatTime = () => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 更新表单状态
const updateFormStatus = () => {
  // 检查是否包含紧急关键词
  const emergencyKeywords = ['急症', '晕倒', '休克', '大出血', '呼吸困难', '胸痛', '剧烈疼痛']
  const hasEmergency = emergencyKeywords.some(keyword =>
    formData.value.problem.includes(keyword)
  )

  if (hasEmergency) {
    formData.value.urgency = 'high'
    showEmergencyModal.value = true
  }
}

// 选择症状
const selectSymptom = (symptom) => {
  if (formData.value.problem) {
    formData.value.problem += '、' + symptom
  } else {
    formData.value.problem = symptom
  }
  updateFormStatus()
}

// 提交表单
const submitForm = async () => {
  if (!isFormValid.value) {
    ElMessage.warning('请填写完整的基本信息')
    return
  }

  isSubmitting.value = true

  try {
    console.log('提交表单数据:', formData.value)

    // 提交表单数据
    const response = await axios.post('http://127.0.0.1:8000/submit', formData.value)

    console.log('提交响应:', response.data)

    // 检查响应状态
    if (response.data.code === 200) {
      // 自动发送初始咨询消息
      const initialMessage = `医生您好，我是${formData.value.name}，来自${formData.value.location}。我的主要症状是：${formData.value.problem}。请问这种情况需要注意什么？`

      await sendMessage(initialMessage)

      ElMessage.success('信息提交成功，AI医生正在为您分析')
    } else {
      ElMessage.error(response.data.message || '提交失败')
    }

  } catch (error) {
    console.error('表单提交失败:', error)

    // 处理不同类型的错误
    if (error.response) {
      // 服务器返回了错误状态码
      const errorData = error.response.data
      if (errorData.code === 400) {
        ElMessage.warning(errorData.message || '请检查填写的信息')
      } else if (errorData.code === 500) {
        ElMessage.error('服务器错误，请稍后重试')
      } else {
        ElMessage.error(errorData.message || '提交失败')
      }
    } else if (error.request) {
      // 网络错误
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      ElMessage.error('提交失败，请稍后重试')
    }
  } finally {
    isSubmitting.value = false
  }
}

// 清理HTML标签的函数
const stripHtmlTags = (text) => {
  if (typeof text !== 'string') return String(text || '')

  // 移除HTML标签
  const cleanText = text.replace(/<[^>]*>/g, '')

  // 解码HTML实体
  const textarea = document.createElement('textarea')
  textarea.innerHTML = cleanText
  return textarea.value
}

// 发送消息
const sendMessage = async (customMessage = null) => {
  let messageText = customMessage || message.value.trim()
  if (!messageText) return

  // 清理可能的HTML内容
  messageText = stripHtmlTags(messageText)

  // 再次检查是否为空
  if (!messageText.trim()) {
    ElMessage.warning('请输入有效的消息内容')
    return
  }

  console.log('发送消息:', messageText)
  console.log('chatHistory 当前状态:', chatHistory.value)
  console.log('chatHistory 是否为数组:', Array.isArray(chatHistory.value))

  isSending.value = true

  // 确保 chatHistory 是数组
  if (!Array.isArray(chatHistory.value)) {
    console.warn('chatHistory 不是数组，重新初始化')
    chatHistory.value = []
  }

  // 添加用户消息
  const userMessage = {
    sender: 'You',
    text: String(messageText || ''),
    timestamp: formatTime()
  }

  try {
    chatHistory.value.push(userMessage)
    console.log('成功添加用户消息:', userMessage)
  } catch (error) {
    console.error('添加用户消息失败:', error)
    console.log('chatHistory.value 类型:', typeof chatHistory.value)
    console.log('chatHistory.value 内容:', chatHistory.value)
    return
  }

  // 清空输入框
  if (!customMessage) {
    message.value = ''
  }

  // 显示正在输入
  isTyping.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  try {
    const response = await axios.post('http://127.0.0.1:8000/chat', {
      message: messageText,
      name: formData.value.name,
      location: formData.value.location,
      problem: formData.value.problem,
      conversationStyle: conversationStyle.value // 传递对话风格
    })

    // 隐藏正在输入
    isTyping.value = false

    // 模拟打字效果
    await simulateStreamOutput(response.data.response)

    // 更新智能快速回复
    updateQuickReplies(messageText, response.data.response)

    // 自动语音播报AI回复（如果启用了语音模式）
    if (consultationMode.value === 'voice' || isVoiceActive.value) {
      setTimeout(() => {
        speakText(response.data.response)
      }, 500)
    }

  } catch (error) {
    console.error('发送消息失败:', error)
    isTyping.value = false

    const errorMessage = {
      sender: 'Bot',
      text: String('抱歉，服务暂时不可用，请稍后重试。'),
      timestamp: formatTime()
    }
    chatHistory.value.push(errorMessage)

    ElMessage.error('发送失败，请检查网络连接')
  } finally {
    isSending.value = false
  }
}

// 优化的流式输出 - 解决卡顿问题
const simulateStreamOutput = async (text) => {
  const startTime = performance.now() // 性能监控

  const botMessage = {
    sender: 'Bot',
    text: '',
    timestamp: formatTime(),
    actions: generateActions(text),
    isStreaming: true,
    streamId: Date.now()
  }
  chatHistory.value.push(botMessage)

  const textString = String(text || '抱歉，无法获取回复')

  // 检查是否使用简化模式
  if (streamSettings.value.speed !== 'normal') {
    const handled = await simpleStreamOutput(textString, botMessage)
    if (handled) {
      const endTime = performance.now()
      console.log(`流式输出完成，耗时: ${(endTime - startTime).toFixed(2)}ms`)
      return
    }
  }

  await nextTick()

  // 优化的流式输出策略
  const messageElement = document.querySelector(`[data-stream-id="${botMessage.streamId}"]`)
  if (!messageElement) {
    console.warn('未找到消息元素，使用响应式更新')
    botMessage.text = textString
    botMessage.isStreaming = false
    return
  }

  const textContainer = messageElement.querySelector('.message-text')
  if (!textContainer) {
    console.warn('未找到文本容器')
    botMessage.text = textString
    botMessage.isStreaming = false
    return
  }

  // 短文本直接显示
  if (textString.length < 100) {
    textContainer.innerHTML = formatMessage(textString)
    botMessage.text = textString
    botMessage.isStreaming = false
    scrollToBottom()
    const endTime = performance.now()
    console.log(`短文本渲染完成，耗时: ${(endTime - startTime).toFixed(2)}ms`)
    return
  }

  // 优化的分块策略
  const totalLength = textString.length
  const chunkSize = Math.max(30, Math.floor(totalLength / 15)) // 更大的块，减少更新次数
  const updateInterval = 80 // 稍慢的更新间隔，减少CPU占用
  let currentIndex = 0
  let updateCount = 0

  const performUpdate = () => {
    updateCount++

    if (currentIndex >= totalLength) {
      // 完成时渲染最终格式
      textContainer.innerHTML = formatMessage(textString)
      botMessage.text = textString
      botMessage.isStreaming = false
      scrollToBottom()

      const endTime = performance.now()
      console.log(`流式输出完成，总耗时: ${(endTime - startTime).toFixed(2)}ms，更新次数: ${updateCount}`)
      return
    }

    // 计算下一个更新位置
    const nextIndex = Math.min(currentIndex + chunkSize, totalLength)
    const currentText = textString.slice(0, nextIndex)

    // 简化的渲染策略：只在句子结束时渲染Markdown
    if (isGoodBreakPoint(textString, nextIndex) || nextIndex === totalLength) {
      textContainer.innerHTML = formatMessage(currentText)
    } else {
      // 使用纯文本，避免破坏的HTML
      textContainer.textContent = currentText
    }

    currentIndex = nextIndex

    // 减少滚动频率
    if (currentIndex % (chunkSize * 2) === 0) {
      scrollToBottom()
    }

    // 使用更高效的调度
    setTimeout(performUpdate, updateInterval)
  }

  // 简化的断点判断
  const isGoodBreakPoint = (text, index) => {
    if (index >= text.length) return true

    const char = text[index - 1]
    const nextChar = text[index]

    // 在句号、问号、感叹号、换行符后是好的断点
    return char === '。' || char === '？' || char === '！' || char === '\n' ||
           (char === '，' && nextChar === ' ') ||
           (char === ' ' && /[A-Z]/.test(nextChar))
  }

  // 开始更新
  performUpdate()
}

// 生成操作按钮
const generateActions = (text) => {
  const actions = []

  if (text.includes('医院')) {
    actions.push({ text: '查看医院详情', action: 'hospital_detail' })
  }

  if (text.includes('药物') || text.includes('用药')) {
    actions.push({ text: '用药指导', action: 'medication_guide' })
  }

  if (text.includes('检查') || text.includes('化验')) {
    actions.push({ text: '检查须知', action: 'examination_guide' })
  }

  actions.push({ text: '继续咨询', action: 'continue_chat' })

  return actions.length > 0 ? actions : null
}

// 处理操作按钮点击
const handleAction = (action) => {
  switch (action.action) {
    case 'hospital_detail':
      ElMessage.info('正在为您查询医院详细信息...')
      break
    case 'medication_guide':
      ElMessage.info('正在为您提供用药指导...')
      break
    case 'examination_guide':
      ElMessage.info('正在为您提供检查须知...')
      break
    case 'continue_chat':
      messageInput.value?.focus()
      break
  }
}

// 快速回复
const sendQuickReply = (reply) => {
  message.value = reply
  sendMessage()
}

// 处理回车键
const handleEnterKey = (event) => {
  if (event.shiftKey) {
    // Shift + Enter 换行
    return
  } else {
    // Enter 发送
    sendMessage()
  }
}

// 调整文本框高度
const adjustTextareaHeight = () => {
  const textarea = messageInput.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }
}

// 切换语音输入 - 增强功能
const toggleVoiceInput = () => {
  isVoiceActive.value = !isVoiceActive.value
  if (isVoiceActive.value) {
    startVoiceRecognition()
    ElMessage.info('🎤 语音输入已开启，请开始说话')
  } else {
    stopVoiceRecognition()
    ElMessage.info('🔇 语音输入已关闭')
  }
}

// 语音识别相关变量
let voiceRecognition = null

// 语音识别状态管理
const voiceRecognitionState = ref({
  isSupported: false,
  isListening: false,
  retryCount: 0,
  maxRetries: 3,
  lastError: null
})

// 启动语音识别 - 增强版
const startVoiceRecognition = () => {
  // 检查浏览器支持
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    ElMessage.error('您的浏览器不支持语音识别功能')
    isVoiceActive.value = false
    voiceRecognitionState.value.isSupported = false
    return
  }

  voiceRecognitionState.value.isSupported = true

  try {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    voiceRecognition = new SpeechRecognition()

    // 优化配置
    voiceRecognition.continuous = false
    voiceRecognition.interimResults = true
    voiceRecognition.lang = 'zh-CN'
    voiceRecognition.maxAlternatives = 1

    voiceRecognition.onstart = () => {
      console.log('语音识别开始')
      voiceRecognitionState.value.isListening = true
      voiceRecognitionState.value.retryCount = 0
      ElMessage.info('🎤 正在监听，请开始说话...')
    }

    voiceRecognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript.trim()
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscript += transcript
        }
      }

      // 实时显示识别结果
      if (finalTranscript) {
        message.value = finalTranscript
        ElMessage.success(`🎤 识别成功：${finalTranscript}`)

        // 智能发送：检查内容有效性
        if (finalTranscript.length > 2) {
          setTimeout(() => {
            sendMessage()
            isVoiceActive.value = false
            voiceRecognitionState.value.isListening = false
          }, 800)
        } else {
          ElMessage.warning('识别内容过短，请重新说话')
          // 重新开始识别
          setTimeout(() => {
            if (isVoiceActive.value) {
              restartVoiceRecognition()
            }
          }, 1000)
        }
      } else if (interimTranscript) {
        // 显示临时识别结果
        message.value = interimTranscript
      }
    }

    voiceRecognition.onerror = (event) => {
      console.error('语音识别错误:', event.error)
      voiceRecognitionState.value.lastError = event.error
      voiceRecognitionState.value.isListening = false

      // 智能错误处理
      switch (event.error) {
        case 'no-speech':
          ElMessage.warning('未检测到语音，请重新尝试')
          if (voiceRecognitionState.value.retryCount < voiceRecognitionState.value.maxRetries) {
            setTimeout(() => restartVoiceRecognition(), 1000)
          } else {
            isVoiceActive.value = false
          }
          break
        case 'audio-capture':
          ElMessage.error('无法访问麦克风，请检查权限设置')
          isVoiceActive.value = false
          break
        case 'not-allowed':
          ElMessage.error('麦克风权限被拒绝，请允许访问麦克风')
          isVoiceActive.value = false
          break
        case 'network':
          ElMessage.error('网络错误，请检查网络连接')
          isVoiceActive.value = false
          break
        default:
          ElMessage.error(`语音识别错误：${event.error}`)
          isVoiceActive.value = false
      }
    }

    voiceRecognition.onend = () => {
      console.log('语音识别结束')
      voiceRecognitionState.value.isListening = false

      // 智能重启逻辑
      if (isVoiceActive.value && !message.value.trim()) {
        if (voiceRecognitionState.value.retryCount < voiceRecognitionState.value.maxRetries) {
          setTimeout(() => {
            if (isVoiceActive.value) {
              restartVoiceRecognition()
            }
          }, 500)
        } else {
          ElMessage.warning('多次尝试未成功，已停止语音识别')
          isVoiceActive.value = false
        }
      }
    }

    voiceRecognition.start()
  } catch (error) {
    console.error('语音识别初始化失败:', error)
    ElMessage.error('语音识别初始化失败')
    isVoiceActive.value = false
  }
}

// 重启语音识别
const restartVoiceRecognition = () => {
  if (voiceRecognitionState.value.retryCount >= voiceRecognitionState.value.maxRetries) {
    ElMessage.warning('重试次数过多，已停止语音识别')
    isVoiceActive.value = false
    return
  }

  voiceRecognitionState.value.retryCount++
  console.log(`重启语音识别，第${voiceRecognitionState.value.retryCount}次重试`)

  if (voiceRecognition) {
    voiceRecognition.stop()
  }

  setTimeout(() => {
    if (isVoiceActive.value) {
      startVoiceRecognition()
    }
  }, 300)
}

// 停止语音识别
const stopVoiceRecognition = () => {
  if (voiceRecognition) {
    voiceRecognition.stop()
    voiceRecognition = null
  }
}

// 清空对话
const clearChat = () => {
  chatHistory.value = []
  ElMessage.success('对话已清空')
}

// 专业医疗工具方法
const openSymptomChecker = () => {
  ElMessage.info('正在启动症状自查工具...')
  // 这里可以打开症状自查模块
}

const openHealthAssessment = () => {
  ElMessage.info('正在启动健康评估工具...')
  // 这里可以打开健康评估模块
}

const openMedicationGuide = () => {
  ElMessage.info('正在启动用药指导工具...')
  // 这里可以打开用药指导模块
}

const openEmergencyGuide = () => {
  ElMessage.warning('正在启动急救指导工具...')
  // 这里可以打开急救指导模块
}

// 流式输出设置
const streamSettings = ref({
  enabled: true,
  speed: 'normal' // 'fast', 'normal', 'slow', 'instant'
})

// 切换流式输出模式
const toggleStreamMode = () => {
  const modes = ['instant', 'fast', 'normal', 'slow']
  const currentIndex = modes.indexOf(streamSettings.value.speed)
  const nextIndex = (currentIndex + 1) % modes.length
  streamSettings.value.speed = modes[nextIndex]

  const modeNames = {
    instant: '瞬时显示',
    fast: '快速显示',
    normal: '正常速度',
    slow: '慢速显示'
  }

  ElMessage.success(`已切换到${modeNames[streamSettings.value.speed]}模式`)
}

// 获取流式输出模式文本
const getStreamModeText = () => {
  const modeNames = {
    instant: '瞬时显示',
    fast: '快速显示',
    normal: '正常速度',
    slow: '慢速显示'
  }
  return modeNames[streamSettings.value.speed] || '正常速度'
}

// 获取流式输出模式图标
const getStreamModeIcon = () => {
  const modeIcons = {
    instant: '⚡',
    fast: '🚀',
    normal: '📝',
    slow: '🐌'
  }
  return modeIcons[streamSettings.value.speed] || '📝'
}

// 切换对话风格
const toggleConversationStyle = () => {
  conversationStyle.value = conversationStyle.value === 'natural' ? 'formal' : 'natural'
  const styleNames = {
    natural: '自然对话',
    formal: '正式回复'
  }
  ElMessage.success(`已切换到${styleNames[conversationStyle.value]}模式`)
}

// 获取对话风格文本
const getConversationStyleText = () => {
  const styleNames = {
    natural: '自然对话',
    formal: '正式回复'
  }
  return styleNames[conversationStyle.value] || '自然对话'
}

// 获取对话风格图标
const getConversationStyleIcon = () => {
  const styleIcons = {
    natural: '💬',
    formal: '📋'
  }
  return styleIcons[conversationStyle.value] || '💬'
}

// 优化的简化版流式输出
const simpleStreamOutput = async (text, botMessage) => {
  const textString = String(text || '抱歉，无法获取回复')

  switch (streamSettings.value.speed) {
    case 'instant':
      // 瞬时显示，无动画
      botMessage.text = textString
      botMessage.isStreaming = false
      await nextTick()
      scrollToBottom()
      break

    case 'fast':
      // 快速显示，优化的分块策略
      const chunkCount = 8
      const chunkSize = Math.ceil(textString.length / chunkCount)

      for (let i = 0; i < chunkCount; i++) {
        const end = Math.min((i + 1) * chunkSize, textString.length)
        botMessage.text = textString.slice(0, end)

        // 只在最后一次更新时滚动
        if (i === chunkCount - 1) {
          botMessage.isStreaming = false
          await nextTick()
          scrollToBottom()
        } else {
          await new Promise(resolve => setTimeout(resolve, 100))
        }
      }
      break

    case 'slow':
      // 慢速显示，按句子分割
      const sentences = textString.split(/([。！？\n])/)
      let currentText = ''

      for (let i = 0; i < sentences.length; i += 2) {
        const sentence = sentences[i] || ''
        const punctuation = sentences[i + 1] || ''
        currentText += sentence + punctuation

        botMessage.text = currentText

        if (i < sentences.length - 2) {
          await new Promise(resolve => setTimeout(resolve, 800))
        }
      }

      botMessage.text = textString
      botMessage.isStreaming = false
      scrollToBottom()
      break

    default: // normal
      // 正常速度，使用优化的DOM操作
      return false
  }

  return true
}

// 咨询方式切换
const startTextConsultation = () => {
  consultationMode.value = 'text'
  isVoiceActive.value = false
  ElMessage.success('已切换到文字咨询模式')
}

const startVoiceConsultation = () => {
  consultationMode.value = 'voice'
  isVoiceActive.value = true
  ElMessage.success('已切换到语音对话模式')
  // 这里可以启动语音识别
}

const toggleVoiceMode = () => {
  if (consultationMode.value === 'voice') {
    startTextConsultation()
  } else {
    startVoiceConsultation()
  }
}

// 快速咨询
const quickConsult = (symptom) => {
  const consultMessage = `医生您好，我想咨询关于${symptom}的问题。请问这种症状可能是什么原因引起的？需要注意什么？`
  message.value = consultMessage
  sendMessage()
}

// 保存咨询记录
const saveConsultationRecord = () => {
  if (chatHistory.value.length === 0) {
    ElMessage.warning('暂无咨询记录可保存')
    return
  }

  const record = {
    patientInfo: patientInfo.value,
    consultationDate: new Date().toISOString(),
    chatHistory: chatHistory.value,
    consultationMode: consultationMode.value
  }

  // 这里可以保存到数据库
  localStorage.setItem('lastConsultationRecord', JSON.stringify(record))
  ElMessage.success('咨询记录已保存')
}

// 导出咨询记录
const exportConsultation = () => {
  if (chatHistory.value.length === 0) {
    ElMessage.warning('暂无咨询记录可导出')
    return
  }

  const patientName = patientInfo.value.name || '患者'
  const consultationDate = new Date().toLocaleDateString()

  let content = `医慧之翼 - AI专业医生咨询记录\n`
  content += `==========================================\n`
  content += `患者姓名：${patientName}\n`
  content += `咨询日期：${consultationDate}\n`
  content += `咨询方式：${consultationMode.value === 'voice' ? '语音对话' : '文字咨询'}\n`
  content += `==========================================\n\n`

  chatHistory.value.forEach(msg => {
    const sender = msg.sender === 'You' ? '患者' : 'AI医生'
    content += `[${msg.timestamp}] ${sender}：\n${msg.text}\n\n`
  })

  content += `==========================================\n`
  content += `本记录由医慧之翼AI医生系统生成\n`
  content += `仅供参考，不能替代专业医生诊断\n`

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `AI医生咨询记录_${patientName}_${consultationDate}.txt`
  link.click()
  URL.revokeObjectURL(url)

  ElMessage.success('咨询记录已导出')
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    const chatContainer = chatHistoryRef.value
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight
    }
  })
}

// 优化的消息格式化 - 减少性能开销
const formatMessage = (text) => {
  if (typeof text !== 'string') {
    console.warn('formatMessage 接收到非字符串类型:', typeof text, text)
    return String(text || '')
  }

  try {
    let cleanText = text

    // 检查是否已经包含HTML标签
    const hasHtmlTags = /<[^>]+>/.test(text)
    if (hasHtmlTags) {
      // 移除HTML标签但保留内容
      cleanText = text.replace(/<[^>]+>/g, '')
      // 解码HTML实体
      const textarea = document.createElement('textarea')
      textarea.innerHTML = cleanText
      cleanText = textarea.value
    }

    // 检查是否包含Markdown语法
    const hasMarkdown = /[*_`#\[\]()>-]|^\d+\.|^[-*+]\s/m.test(cleanText)

    if (!hasMarkdown) {
      // 如果没有Markdown语法，只处理换行
      return cleanText.replace(/\n/g, '<br>')
    }

    // 使用marked解析Markdown（仅在需要时）
    const htmlContent = marked.parse(cleanText)
    return htmlContent
  } catch (error) {
    console.warn('Markdown解析失败，使用纯文本:', error)
    // 回退到简单的换行处理
    const cleanText = text.replace(/<[^>]+>/g, '')
    return cleanText.replace(/\n/g, '<br>')
  }
}

// 紧急情况处理
const call120 = () => {
  ElNotification({
    title: '紧急呼叫',
    message: '正在为您拨打120急救电话...',
    type: 'warning',
    duration: 3000
  })
  // 在实际应用中，这里可以集成电话拨打功能
}

const findNearbyHospital = () => {
  ElMessage.info('正在为您查找附近的医院...')
  // 这里可以集成地图API查找附近医院
}

const closeEmergencyModal = () => {
  showEmergencyModal.value = false
}

// 智能交互处理
const handleNavigationGesture = (action) => {
  console.log('智能问诊手势导航:', action)

  switch (action) {
    case 'zoom_in':
      // 页面放大
      document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString()
      ElMessage.success('🤲 手势控制：页面已放大')
      break
    case 'zoom_out':
      // 页面缩小
      document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString()
      ElMessage.success('🤲 手势控制：页面已缩小')
      break
    case 'scroll_top':
      // 返回页面顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
      ElMessage.success('🤲 手势控制：已返回页面顶部')
      break
    case 'scroll_bottom':
      // 滚动到页面底部
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
      ElMessage.success('🤲 手势控制：已滚动到页面底部')
      break
    case 'confirm_action':
      // 发送消息
      if (message.value.trim()) {
        sendMessage()
        ElMessage.success('🤲 手势控制：已发送消息')
      } else {
        ElMessage.warning('🤲 手势控制：请先输入消息内容')
      }
      break
    case 'stop_action':
      // 停止语音输入
      if (isVoiceActive.value) {
        toggleVoiceInput()
        ElMessage.success('🤲 手势控制：已停止语音输入')
      }
      break
    default:
      console.log('未处理的手势动作:', action)
  }
}

const handleVoiceCommand = (command) => {
  console.log('语音命令:', command)
  if (command.type === 'navigation') {
    // 处理导航命令
  }
}

const handleVoiceResponse = (response) => {
  console.log('语音回复:', response)

  // 处理语音识别的结果
  if (response.question) {
    // 将语音识别的问题填入输入框
    message.value = response.question
    ElMessage.success(`🎤 语音识别：${response.question}`)

    // 自动发送消息（可选）
    setTimeout(() => {
      if (message.value.trim()) {
        sendMessage()
      }
    }, 1000)
  }

  // 处理AI回复的语音播报
  if (response.answer) {
    speakText(response.answer)
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

// 语音播报功能 - 增强版
const speakText = (text) => {
  if ('speechSynthesis' in window && text) {
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
    const maxLength = 500
    const textToSpeak = cleanText.length > maxLength
      ? cleanText.substring(0, maxLength) + '...'
      : cleanText

    const utterance = new SpeechSynthesisUtterance(textToSpeak)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1
    utterance.volume = 0.8

    // 播报开始时的提示
    utterance.onstart = () => {
      ElMessage.info('🔊 AI正在为您播报回复')
    }

    // 播报结束时的提示
    utterance.onend = () => {
      console.log('语音播报结束')
    }

    // 播报错误处理
    utterance.onerror = (event) => {
      console.error('语音播报错误:', event.error)
      ElMessage.warning('语音播报失败')
    }

    console.log('原始文本:', text)
    console.log('清理后文本:', textToSpeak)

    speechSynthesis.speak(utterance)
  }
}

// 工具函数已集成到其他地方

// 生命周期
onMounted(() => {
  console.log('组件已挂载')
  console.log('chatHistory 初始状态:', chatHistory.value)
  console.log('chatHistory 是否为数组:', Array.isArray(chatHistory.value))

  // 确保 chatHistory 正确初始化
  if (!Array.isArray(chatHistory.value)) {
    console.warn('重新初始化 chatHistory')
    chatHistory.value = []
  }

  // 初始化快速回复
  updateQuickReplies()

  // 初始化欢迎消息
  setTimeout(() => {
    ElNotification({
      title: '欢迎使用智能问诊',
      message: '请先填写基本信息，然后开始咨询。您可以使用语音输入功能！',
      type: 'info',
      duration: 5000
    })
  }, 1000)

  // 模拟在线状态检查
  setInterval(() => {
    // 这里可以添加实际的在线状态检查逻辑
  }, 30000)
})

// 组件卸载时清理资源
onUnmounted(() => {
  // 停止语音识别
  if (voiceRecognition) {
    voiceRecognition.stop()
    voiceRecognition = null
  }

  // 停止语音播报
  if (speechSynthesis) {
    speechSynthesis.cancel()
  }

  console.log('AI问诊组件已卸载，语音功能已清理')
})
</script>

<style scoped>
.intelligent-consultation {
  min-height: 100vh;
  background: linear-gradient(135deg,
    #0a0a2e 0%,
    #16213e 25%,
    #0f3460 50%,
    #16213e 75%,
    #0a0a2e 100%);
  font-family: "微软雅黑", "PingFang SC", sans-serif;
  color: #ffffff;
  position: relative;
  overflow-x: hidden;
  padding-top: 80px; /* 为固定header留出空间 */
}

.page-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(0, 255, 136, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(0, 136, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(255, 0, 136, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 1;
}

/* 页面头部 */
.page-header {
  position: relative;
  z-index: 10;
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 25px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(30, 30, 60, 0.4));
  border: 2px solid rgba(0, 255, 136, 0.4);
  border-radius: 15px;
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  max-width: 1400px;
  margin: 0 auto 20px auto;
}

.header-content:hover {
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
}

.consultation-avatar {
  position: relative;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.avatar-status {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid #fff;
}

.avatar-status.online {
  background: #00ff88;
  animation: pulse 2s infinite;
}

.avatar-status.offline {
  background: #f44336;
}

.header-text {
  flex: 1;
}

.consultation-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 14px;
}

.status-indicator.active {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
}

.status-indicator.active .status-dot {
  background: #00ff88;
  animation: pulse 2s infinite;
}

/* 强制页面头部所有文字为白色 */
.page-header,
.page-header *,
.header-content,
.header-content *,
.page-title,
.page-title *,
.page-subtitle,
.page-subtitle * {
  color: #ffffff !important;
}

/* 强制欢迎消息所有文字为白色 */
.welcome-message,
.welcome-message *,
.welcome-content,
.welcome-content *,
.welcome-content h3,
.welcome-content p,
.welcome-tips,
.welcome-tips *,
.tip-item,
.tip-item * {
  color: #ffffff !important;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #00ff88;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  font-size: 32px;
}

.page-subtitle {
  font-size: 16px;
  color: #ccc;
  margin: 0;
}

/* 状态栏 */
.status-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 25px;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.status-card:hover {
  border-color: rgba(0, 255, 136, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
}

.status-card .status-icon {
  font-size: 24px;
  width: 40px;
  text-align: center;
}

.status-info {
  flex: 1;
}

.status-label {
  display: block;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 5px;
}

.status-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #00ff88;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #ff5722;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-item.active .status-dot {
  background: #4caf50;
}

.status-icon {
  font-size: 16px;
}

/* 主要内容区域 */
.main-content {
  display: flex;
  gap: 30px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 180px);
  position: relative;
  z-index: 2;
}

/* 左侧面板 */
.left-panel {
  flex: 0 0 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card,
.quick-symptoms-card,
.doctor-profile-card,
.medical-tools-card,
.quick-consultation-card {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.info-card:hover,
.quick-symptoms-card:hover,
.doctor-profile-card:hover,
.medical-tools-card:hover,
.quick-consultation-card:hover {
  border-color: rgba(0, 255, 136, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
}

.card-header h3 {
  margin: 0;
  color: #00ff88;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.valid {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-badge.invalid {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.card-content {
  padding: 20px;
}

.card-icon {
  font-size: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 0;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
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
  color: #00ff88;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
  font-family: inherit;
  background: rgba(0, 0, 0, 0.2);
  color: #ffffff;
  backdrop-filter: blur(5px);
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.2);
  background: rgba(0, 0, 0, 0.3);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #ccc;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-loading {
  position: relative;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.btn-icon {
  font-size: 18px;
}

/* 快速症状选择 */
.symptom-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
}

.symptom-tag {
  padding: 10px 15px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  text-align: center;
  backdrop-filter: blur(5px);
}

.symptom-tag:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 255, 136, 0.2);
}

/* 右侧面板 */
.right-panel {
  flex: 1;
  min-width: 0;
}

.chat-container {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.chat-container:hover {
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
}

/* 聊天头部 */
.chat-header {
  padding: 20px;
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.doctor-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.doctor-avatar {
  position: relative;
}

.doctor-avatar .avatar-circle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #000;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.doctor-avatar .avatar-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid #fff;
}

.doctor-avatar .avatar-status.online {
  background: #00ff88;
  animation: pulse 2s infinite;
}

.doctor-name {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
}

.doctor-status {
  font-size: 14px;
  color: #ccc;
  margin: 4px 0 0 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.online-dot {
  width: 8px;
  height: 8px;
  background: #00ff88;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.chat-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(0, 255, 136, 0.3);
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #00ff88;
  backdrop-filter: blur(5px);
}

.action-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: scale(1.1);
}

.action-btn.active {
  background: #00ff88;
  color: #000;
  border-color: #00ff88;
}

/* 聊天历史 */
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.welcome-message {
  text-align: center;
  padding: 40px 20px;
}

.welcome-content {
  max-width: 400px;
  margin: 0 auto;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.welcome-content h3 {
  font-size: 24px;
  color: #ffffff !important;
  margin: 0 0 12px 0;
}

.welcome-content p {
  font-size: 16px;
  color: #ffffff !important;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.welcome-tips {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tip-item {
  font-size: 14px;
  color: #ffffff !important;
  text-align: left;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 消息样式 */
.message-wrapper {
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bot-message {
  align-self: flex-start;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bot-message .message-avatar {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.sender-name {
  font-size: 12px;
  font-weight: 600;
  color: #666;
}

.message-time {
  font-size: 11px;
  color: #999;
}

.message-text {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
  color: #ffffff;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 统一所有消息为白色字体 - 深色主题 */
.message-text,
.message-text h1,
.message-text h2,
.message-text h3,
.message-text h4,
.message-text h5,
.message-text h6,
.message-text p,
.message-text li,
.message-text span,
.message-text div,
.message-text strong,
.message-text em,
.message-text ul,
.message-text ol,
.message-text blockquote,
.message-text code,
.message-text pre,
.bot-message .message-text,
.bot-message .message-text *,
.user-message .message-text,
.user-message .message-text * {
  color: #ffffff !important;
}

/* 特别强调AI医生回复的可读性 */
.bot-message .message-text {
  background: rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(0, 255, 136, 0.3) !important;
  color: #ffffff !important;
}

/* 确保所有Markdown元素都是白色 */
.bot-message .message-text h1,
.bot-message .message-text h2,
.bot-message .message-text h3,
.bot-message .message-text h4,
.bot-message .message-text h5,
.bot-message .message-text h6 {
  color: #00ff88 !important;
  font-weight: bold !important;
}

.bot-message .message-text p,
.bot-message .message-text li,
.bot-message .message-text span,
.bot-message .message-text div,
.bot-message .message-text strong,
.bot-message .message-text em {
  color: #ffffff !important;
}

.bot-message .message-text ul,
.bot-message .message-text ol {
  color: #ffffff !important;
  padding-left: 20px !important;
}

.bot-message .message-text li {
  color: #ffffff !important;
  margin: 4px 0 !important;
}

.bot-message .message-text strong {
  color: #00ff88 !important;
  font-weight: bold !important;
}

.bot-message .message-text code {
  background: rgba(0, 255, 136, 0.2) !important;
  color: #ffffff !important;
  padding: 2px 4px !important;
  border-radius: 4px !important;
}

/* Markdown样式 - 深色主题优化 */
.message-text h1 { font-size: 18px; margin: 10px 0 5px 0; font-weight: bold; }
.message-text h2 { font-size: 16px; margin: 10px 0 5px 0; font-weight: bold; }
.message-text h3 { font-size: 15px; margin: 10px 0 5px 0; font-weight: bold; }
.message-text h4 { font-size: 14px; margin: 10px 0 5px 0; font-weight: bold; }

.message-text p {
  margin: 8px 0;
}

.message-text ul,
.message-text ol {
  margin: 8px 0;
  padding-left: 20px;
}

.message-text li {
  margin: 4px 0;
}

.message-text blockquote {
  border-left: 4px solid #00d4ff;
  margin: 10px 0;
  padding: 8px 12px;
  background: rgba(0, 212, 255, 0.1);
  border-radius: 4px;
}

.message-text code {
  background: rgba(0, 212, 255, 0.2);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #00d4ff !important;
}

.message-text pre {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 12px;
  margin: 10px 0;
  overflow-x: auto;
}

.message-text pre code {
  background: none;
  padding: 0;
  border-radius: 0;
}

.message-text table {
  border-collapse: collapse;
  width: 100%;
  margin: 10px 0;
}

.message-text th,
.message-text td {
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 8px;
  text-align: left;
}

.message-text th {
  background-color: rgba(255, 255, 255, 0.1);
  font-weight: bold;
}

.message-text strong {
  font-weight: bold;
}

.message-text em {
  font-style: italic;
}

.message-text a {
  color: #00d4ff !important;
  text-decoration: none;
}

.message-text a:hover {
  text-decoration: underline;
}

/* 流式输出相关样式 */
.message-text-container {
  position: relative;
}

.streaming-cursor {
  display: inline-block;
  margin-left: 2px;
  font-weight: bold;
  animation: blink 1s infinite;
  color: #667eea;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.user-message .message-text {
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
  color: white !important;
  border: 1px solid rgba(0, 212, 255, 0.3);
}

/* 确保用户消息中的所有元素都是白色 */
.user-message .message-text * {
  color: white !important;
}

/* 确保AI回复的文字颜色正确 - 深色主题 */
.bot-message .message-text {
  background: rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(0, 255, 136, 0.3) !important;
  color: #ffffff !important;
}

.bot-message .message-text * {
  color: #ffffff !important;
}

.bot-message .message-text h1,
.bot-message .message-text h2,
.bot-message .message-text h3,
.bot-message .message-text h4,
.bot-message .message-text h5,
.bot-message .message-text h6 {
  color: #00ff88 !important;
  font-weight: bold !important;
}

.bot-message .message-text p {
  color: #ffffff !important;
}

.bot-message .message-text li {
  color: #ffffff !important;
}

.bot-message .message-text strong {
  color: #00ff88 !important;
  font-weight: bold !important;
}

.bot-message .message-text code {
  color: #ffffff !important;
  background: rgba(0, 255, 136, 0.2) !important;
}

.bot-message .message-text a {
  color: #00d4ff !important;
}

.message-actions {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.action-button {
  padding: 6px 12px;
  background: #e3f2fd;
  border: 1px solid #2196f3;
  border-radius: 15px;
  font-size: 12px;
  color: #2196f3;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: #2196f3;
  color: white;
}

/* 正在输入指示器 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
}

.typing-animation {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 18px;
}

.typing-animation span {
  width: 8px;
  height: 8px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-animation span:nth-child(1) { animation-delay: -0.32s; }
.typing-animation span:nth-child(2) { animation-delay: -0.16s; }

.typing-text {
  font-size: 12px;
  color: #666;
  margin-left: 8px;
}

/* 输入区域 */
.chat-input-area {
  padding: 20px;
  border-top: 1px solid #e9ecef;
}

.input-container {
  margin-bottom: 12px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 25px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  font-size: 14px;
  line-height: 1.5;
  font-family: inherit;
  max-height: 120px;
}

.input-actions {
  display: flex;
  gap: 8px;
}

.voice-btn,
.send-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.3s ease;
}

.voice-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
  flex-direction: column;
  gap: 2px;
  width: auto;
  min-width: 36px;
  padding: 8px 12px;
  border-radius: 18px;
}

.voice-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.voice-btn.active,
.voice-btn.listening {
  background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
  animation: pulse 1.5s infinite;
  box-shadow: 0 0 20px rgba(255, 71, 87, 0.6);
}

.voice-btn.listening::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

.voice-status {
  font-size: 8px;
  opacity: 0.9;
  animation: blink 1s infinite;
  white-space: nowrap;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
}

/* 快速回复 */
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-reply-btn {
  padding: 8px 12px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 15px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-reply-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* 紧急情况弹窗 */
.emergency-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  padding: 30px;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.emergency-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.modal-content h3 {
  font-size: 24px;
  color: #f44336;
  margin: 0 0 12px 0;
}

.modal-content p {
  font-size: 16px;
  color: #666;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.emergency-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.emergency-btn {
  padding: 12px 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.emergency-btn:hover {
  background: #d32f2f;
  transform: translateY(-2px);
}

.cancel-btn {
  padding: 12px 20px;
  background: #e9ecef;
  color: #666;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #dee2e6;
}

/* 动画 */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
  100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
    padding: 10px;
  }

  .left-panel {
    flex: none;
  }

  .status-bar {
    gap: 20px;
  }

  .page-title {
    font-size: 24px;
  }

  .chat-container {
    height: 60vh;
  }
}

/* 滚动条样式 */
.chat-history::-webkit-scrollbar {
  width: 6px;
}

.chat-history::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 医生资料卡片样式 */
.doctor-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-bottom: 25px;
}

.doctor-avatar-large {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.doctor-avatar-large .avatar-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.doctor-specialty {
  color: #00ff88;
  font-size: 12px;
  font-weight: bold;
  text-align: center;
}

.doctor-details h4 {
  margin: 0 0 5px 0;
  color: #ffffff;
  font-size: 18px;
  text-align: center;
}

.doctor-title {
  color: #ccc;
  font-size: 14px;
  margin: 0 0 15px 0;
  text-align: center;
}

.doctor-capabilities {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.capability-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e0e0e0;
  font-size: 13px;
}

.capability-icon {
  font-size: 16px;
  color: #00ff88;
}

.consultation-options {
  margin-bottom: 20px;
}

.consultation-options h5 {
  margin: 0 0 10px 0;
  color: #00ff88;
  font-size: 14px;
  font-weight: bold;
}

.option-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.option-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.option-btn.active {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
  border-color: #00ff88;
}

.patient-info-section {
  margin-top: 20px;
}

.patient-info-section h5 {
  margin: 0 0 10px 0;
  color: #00ff88;
  font-size: 14px;
  font-weight: bold;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item label {
  color: #ccc;
  font-size: 12px;
}

.info-input,
.info-select {
  padding: 8px 12px;
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.2);
  color: #ffffff;
  font-size: 12px;
  transition: all 0.3s ease;
}

.info-input:focus,
.info-select:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
}

/* 医疗工具样式 */
.tool-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.tool-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
}

.tool-btn.emergency {
  border-color: rgba(255, 69, 58, 0.5);
}

.tool-btn.emergency:hover {
  border-color: #ff453a;
  background: rgba(255, 69, 58, 0.1);
}

.tool-icon {
  font-size: 24px;
  color: #00ff88;
}

.tool-btn.emergency .tool-icon {
  color: #ff453a;
}

.tool-info {
  flex: 1;
}

.tool-name {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #ffffff;
}

.tool-desc {
  font-size: 12px;
  color: #ccc;
}

/* 症状分类样式 */
.symptom-categories {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-section h6 {
  margin: 0 0 8px 0;
  color: #00ff88;
  font-size: 13px;
  font-weight: bold;
}

.symptom-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.symptom-tag {
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  backdrop-filter: blur(5px);
}

.symptom-tag:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 255, 136, 0.2);
}

/* 欢迎消息新样式 */
.doctor-welcome-avatar {
  margin-bottom: 20px;
}

.doctor-welcome-avatar .avatar-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
  margin: 0 auto;
}

.medical-services {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 20px 0;
}

.service-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(0, 255, 136, 0.1);
  border-radius: 10px;
  border-left: 4px solid #00ff88;
}

.service-icon {
  font-size: 20px;
  color: #00ff88;
}

.service-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.service-info strong {
  color: #ffffff;
  font-size: 14px;
}

.service-info span {
  color: #ccc;
  font-size: 12px;
}

.consultation-start {
  margin: 20px 0;
}

.start-prompt {
  color: #ffffff;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: center;
}

.quick-start-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.quick-start-btn {
  padding: 10px 15px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-start-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.medical-disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 193, 7, 0.1);
  border-radius: 8px;
  border-left: 4px solid #ffc107;
  margin-top: 20px;
}

.disclaimer-icon {
  font-size: 16px;
  color: #ffc107;
  margin-top: 2px;
}

.medical-disclaimer span {
  color: #ffffff;
  font-size: 12px;
  line-height: 1.4;
}

/* 医生状态样式 */
.doctor-status {
  display: flex;
  align-items: center;
}

.status-badge.online {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}
</style>