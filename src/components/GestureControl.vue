<template>
  <div class="gesture-control">
    <!-- 手势控制面板 -->
    <div class="gesture-panel" v-show="showPanel">
      <h3>🤚 智能图表手势控制</h3>
      <div class="gesture-status">
        <div class="status-item">
          <span class="status-label">状态:</span>
          <span class="status-value" :class="statusClass">{{ gestureStatus }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">当前手势:</span>
          <span class="status-value">{{ currentGesture || '无' }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">置信度:</span>
          <span class="status-value">{{ confidence }}%</span>
        </div>
      </div>

      <!-- 手势说明 -->
      <div class="gesture-guide">
        <h4>📊 图表操作手势</h4>
        <div class="gesture-list">
          <div v-for="action in gestureActions" :key="action.name" class="gesture-item">
            <span class="gesture-icon">{{ action.icon }}</span>
            <span class="gesture-desc">{{ action.description }}</span>
          </div>
        </div>
      </div>

      <!-- 使用提示 -->
      <div class="gesture-tips">
        <h4>💡 使用提示</h4>
        <ul class="tips-list">
          <li>先点击图表选中，再使用手势操作</li>
          <li>保持手势清晰，距离摄像头50-100cm</li>
          <li>确保光线充足，手势持续1-2秒</li>
          <li>可配合语音控制使用</li>
        </ul>
      </div>
    </div>

    <!-- 摄像头视频 -->
    <video
      ref="videoElement"
      class="gesture-video"
      :class="{ 'video-hidden': !showVideo }"
      autoplay
      muted
      playsinline
    ></video>

    <!-- 手势识别画布 -->
    <canvas
      ref="canvasElement"
      class="gesture-canvas"
      :class="{ 'canvas-hidden': !showVideo }"
    ></canvas>

    <!-- 控制按钮 -->
    <div class="gesture-controls">
      <button
        @click="toggleGestureControl"
        class="control-btn primary"
        :disabled="!isSupported"
      >
        <span class="btn-icon">{{ isActive ? '🛑' : '🤚' }}</span>
        <span class="btn-text">{{ isActive ? '关闭手势' : '开启手势' }}</span>
      </button>

      <button
        @click="toggleVideo"
        class="control-btn secondary"
        v-if="isActive"
      >
        <span class="btn-icon">{{ showVideo ? '👁️' : '📹' }}</span>
        <span class="btn-text">{{ showVideo ? '隐藏摄像头' : '显示摄像头' }}</span>
      </button>

      <button
        @click="togglePanel"
        class="control-btn secondary"
        v-if="isActive"
      >
        <span class="btn-icon">{{ showPanel ? '📋' : '📊' }}</span>
        <span class="btn-text">{{ showPanel ? '隐藏面板' : '显示面板' }}</span>
      </button>
    </div>

    <!-- 手势提示动画 -->
    <div class="gesture-hint" v-show="isActive && currentGesture !== 'none'">
      <div class="hint-content">
        <span class="hint-icon">{{ getCurrentGestureIcon() }}</span>
        <span class="hint-text">{{ getCurrentGestureAction() }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['gestureDetected', 'navigationGesture'])

// 响应式数据
const videoElement = ref(null)
const canvasElement = ref(null)
const isSupported = ref(false)
const isActive = ref(false)
const showVideo = ref(false)
const showPanel = ref(true)
const gestureStatus = ref('未初始化')
const currentGesture = ref('none')
const confidence = ref(0)

// MediaPipe 相关变量
let hands = null
let camera = null
let canvasCtx = null
let lastGestureTime = 0

// 计算属性
const statusClass = computed(() => {
  switch (gestureStatus.value) {
    case '就绪': return 'status-ready'
    case '运行中': return 'status-active'
    case '启动中': return 'status-loading'
    case '已停止': return 'status-stopped'
    case '初始化失败':
    case '启动失败': return 'status-error'
    default: return 'status-default'
  }
})

// 手势动作配置 - 增强医疗专业功能
const gestureActions = ref([
  { name: 'thumbs_up', icon: '👍', description: '点赞 - 放大显示内容' },
  { name: 'fist', icon: '✊', description: '握拳 - 缩小显示内容' },
  { name: 'point_left', icon: '👈', description: '向左 - 返回上一页/切换图表' },
  { name: 'point_right', icon: '👉', description: '向右 - 前进下一页/切换图表' },
  { name: 'ok_sign', icon: '👌', description: 'OK手势 - 确认操作/导出数据' },
  { name: 'open_palm', icon: '✋', description: '张开手掌 - 停止操作/标准模式' },
  { name: 'peace', icon: '✌️', description: '胜利手势 - 切换视图模式' },
  { name: 'point_up', icon: '👆', description: '向上 - 返回页面顶部' },
  { name: 'point_down', icon: '👇', description: '向下 - 滚动到页面底部' },
  { name: 'call_me', icon: '🤙', description: '打电话手势 - 紧急呼叫' },
  { name: 'rock', icon: '🤘', description: '摇滚手势 - 切换到康复训练' },
  { name: 'love_you', icon: '🤟', description: '爱你手势 - 健康祝福' }
])

// 获取当前手势图标
const getCurrentGestureIcon = () => {
  const action = gestureActions.value.find(a => a.name === currentGesture.value)
  return action ? action.icon : '🤚'
}

// 获取当前手势动作描述
const getCurrentGestureAction = () => {
  const action = gestureActions.value.find(a => a.name === currentGesture.value)
  return action ? action.description : ''
}

// 手势识别核心逻辑 - 优化版
const detectGesture = (landmarks) => {
  if (!landmarks || landmarks.length === 0) {
    return { gesture: 'none', confidence: 0 }
  }

  const hand = landmarks[0]

  // 获取关键点坐标
  const thumb_tip = hand[4]
  const thumb_ip = hand[3]
  const thumb_mcp = hand[2]
  const index_tip = hand[8]
  const index_pip = hand[6]
  const index_mcp = hand[5]
  const middle_tip = hand[12]
  const middle_pip = hand[10]
  const middle_mcp = hand[9]
  const ring_tip = hand[16]
  const ring_pip = hand[14]
  const ring_mcp = hand[13]
  const pinky_tip = hand[20]
  const pinky_pip = hand[18]
  const pinky_mcp = hand[17]
  const wrist = hand[0]

  // 改进的手指状态判断 - 考虑更多关键点
  const isThumbUp = thumb_tip.y < thumb_ip.y && thumb_tip.y < thumb_mcp.y
  const isIndexUp = index_tip.y < index_pip.y && index_tip.y < index_mcp.y
  const isMiddleUp = middle_tip.y < middle_pip.y && middle_tip.y < middle_mcp.y
  const isRingUp = ring_tip.y < ring_pip.y && ring_tip.y < ring_mcp.y
  const isPinkyUp = pinky_tip.y < pinky_pip.y && pinky_tip.y < pinky_mcp.y

  // 计算手指弯曲程度
  const thumbBend = Math.abs(thumb_tip.y - thumb_ip.y)
  const indexBend = Math.abs(index_tip.y - index_pip.y)
  const middleBend = Math.abs(middle_tip.y - middle_pip.y)
  const ringBend = Math.abs(ring_tip.y - ring_pip.y)
  const pinkyBend = Math.abs(pinky_tip.y - pinky_pip.y)

  let gesture = 'none'
  let conf = 0

  // 优化的手势识别逻辑
  if (isThumbUp && !isIndexUp && !isMiddleUp && !isRingUp && !isPinkyUp) {
    // 竖起大拇指 - 点赞手势
    gesture = 'thumbs_up'
    conf = Math.min(95, 70 + thumbBend * 500)
  }
  else if (!isThumbUp && isIndexUp && !isMiddleUp && !isRingUp && !isPinkyUp) {
    // 竖起食指 - 判断指向方向
    const deltaX = index_tip.x - wrist.x
    const deltaY = index_tip.y - wrist.y
    const absX = Math.abs(deltaX)
    const absY = Math.abs(deltaY)

    if (absX > absY * 1.2) {
      // 水平指向
      gesture = deltaX > 0 ? 'point_right' : 'point_left'
      conf = Math.min(90, 70 + absX * 100)
    } else if (absY > absX * 1.2) {
      // 垂直指向
      gesture = deltaY < 0 ? 'point_up' : 'point_down'
      conf = Math.min(90, 70 + absY * 100)
    } else {
      // 模糊指向，默认向上
      gesture = 'point_up'
      conf = 75
    }
  }
  else if (isThumbUp && isIndexUp && !isMiddleUp && !isRingUp && !isPinkyUp) {
    // OK手势 - 放宽距离阈值
    const distance = Math.sqrt(
      Math.pow(thumb_tip.x - index_tip.x, 2) +
      Math.pow(thumb_tip.y - index_tip.y, 2)
    )
    if (distance < 0.08) { // 放宽阈值从0.05到0.08
      gesture = 'ok_sign'
      conf = Math.min(95, 90 - distance * 500)
    }
  }
  else if (!isThumbUp && isIndexUp && isMiddleUp && !isRingUp && !isPinkyUp) {
    // 胜利手势 - V字手势
    const fingerDistance = Math.abs(index_tip.x - middle_tip.x)
    if (fingerDistance > 0.03) { // 确保两指分开
      gesture = 'peace'
      conf = Math.min(90, 75 + fingerDistance * 300)
    }
  }
  else if (isThumbUp && isIndexUp && isMiddleUp && isRingUp && isPinkyUp) {
    // 张开手掌 - 所有手指都伸直
    const spreadScore = (thumbBend + indexBend + middleBend + ringBend + pinkyBend) * 100
    gesture = 'open_palm'
    conf = Math.min(95, 85 + spreadScore)
  }
  else if (!isThumbUp && !isIndexUp && !isMiddleUp && !isRingUp && !isPinkyUp) {
    // 握拳 - 所有手指都弯曲
    const fistScore = Math.min(thumbBend, indexBend, middleBend, ringBend, pinkyBend) * 200
    gesture = 'fist'
    conf = Math.min(90, 70 + fistScore)
  }
  else if (isThumbUp && !isIndexUp && !isMiddleUp && !isRingUp && isPinkyUp) {
    // 打电话手势 - 拇指和小指伸出
    gesture = 'call_me'
    conf = 85
  }
  else if (!isThumbUp && isIndexUp && !isMiddleUp && !isRingUp && isPinkyUp) {
    // 摇滚手势 - 食指和小指伸出
    gesture = 'rock'
    conf = 85
  }
  else if (isThumbUp && isIndexUp && !isMiddleUp && !isRingUp && isPinkyUp) {
    // 爱你手势 - 拇指、食指和小指伸出
    gesture = 'love_you'
    conf = 85
  }

  // 确保置信度在合理范围内
  conf = Math.max(0, Math.min(100, conf))

  return { gesture, confidence: conf }
}

// 处理MediaPipe结果
const onResults = (results) => {
  if (!canvasCtx) return

  // 清空画布并绘制视频帧
  canvasCtx.save()
  canvasCtx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height)
  canvasCtx.drawImage(results.image, 0, 0, canvasElement.value.width, canvasElement.value.height)

  if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
    // 绘制手部关键点和连接线
    for (const landmarks of results.multiHandLandmarks) {
      drawLandmarks(canvasCtx, landmarks)
      drawConnectors(canvasCtx, landmarks)
    }

    // 检测手势
    const gestureResult = detectGesture(results.multiHandLandmarks)
    currentGesture.value = gestureResult.gesture
    confidence.value = Math.round(gestureResult.confidence)

    // 触发手势事件 - 针对不同手势使用不同的置信度阈值
    let confidenceThreshold = 65 // 默认阈值

    // 缩放手势使用更低的阈值，提高识别敏感度
    if (gestureResult.gesture === 'thumbs_up' || gestureResult.gesture === 'fist') {
      confidenceThreshold = 60 // 缩放手势降低阈值到60
    }
    // 精确操作手势使用更高阈值，避免误操作
    else if (gestureResult.gesture === 'ok_sign') {
      confidenceThreshold = 70 // OK手势提高阈值到70
    }

    if (gestureResult.confidence > confidenceThreshold) {
      // 只发送原始手势检测事件用于调试和显示
      emit('gestureDetected', gestureResult)
      // 处理手势并发送标准化的导航事件
      handleGestureAction(gestureResult.gesture)
    }
  } else {
    currentGesture.value = 'none'
    confidence.value = 0
  }

  canvasCtx.restore()
}

// 绘制手部关键点
const drawLandmarks = (ctx, landmarks) => {
  ctx.fillStyle = '#00FF88'
  for (const landmark of landmarks) {
    ctx.beginPath()
    ctx.arc(
      landmark.x * ctx.canvas.width,
      landmark.y * ctx.canvas.height,
      3, 0, 2 * Math.PI
    )
    ctx.fill()
  }
}

// 绘制手部连接线
const drawConnectors = (ctx, landmarks) => {
  ctx.strokeStyle = '#FF0088'
  ctx.lineWidth = 2

  // 手部连接关系
  const connections = [
    [0, 1], [1, 2], [2, 3], [3, 4], // 拇指
    [0, 5], [5, 6], [6, 7], [7, 8], // 食指
    [0, 9], [9, 10], [10, 11], [11, 12], // 中指
    [0, 13], [13, 14], [14, 15], [15, 16], // 无名指
    [0, 17], [17, 18], [18, 19], [19, 20] // 小指
  ]

  for (const [start, end] of connections) {
    ctx.beginPath()
    ctx.moveTo(
      landmarks[start].x * ctx.canvas.width,
      landmarks[start].y * ctx.canvas.height
    )
    ctx.lineTo(
      landmarks[end].x * ctx.canvas.width,
      landmarks[end].y * ctx.canvas.height
    )
    ctx.stroke()
  }
}

// 处理手势动作 - 优化版（避免重复指令）
const handleGestureAction = (gesture) => {
  const now = Date.now()

  // 针对不同手势使用不同的防抖时间
  let debounceTime = 1000 // 默认防抖时间

  // 缩放手势使用更短的防抖时间，提高响应性
  if (gesture === 'thumbs_up' || gesture === 'fist') {
    debounceTime = 800 // 缩放手势800ms防抖
  }
  // 导航手势使用标准防抖时间
  else if (gesture === 'point_left' || gesture === 'point_right' || gesture === 'point_up' || gesture === 'point_down') {
    debounceTime = 1000 // 导航手势1000ms防抖
  }
  // 确认类手势使用更长防抖时间，避免误操作
  else if (gesture === 'ok_sign' || gesture === 'open_palm') {
    debounceTime = 1200 // 确认手势1200ms防抖
  }

  if (now - lastGestureTime < debounceTime) return
  lastGestureTime = now

  const actionMap = {
    'point_left': 'previous',
    'point_right': 'next',
    'point_up': 'scroll_top',
    'point_down': 'scroll_bottom',
    'ok_sign': 'confirm_action',
    'open_palm': 'stop_action',
    'peace': 'toggle_view',
    'thumbs_up': 'zoom_in',
    'fist': 'zoom_out',
    'call_me': 'emergency_call',
    'rock': 'rehabilitation_mode',
    'love_you': 'health_blessing'
  }

  const action = actionMap[gesture]
  if (action) {
    // 只发送事件给父组件，不在这里执行具体操作
    emit('navigationGesture', action)

    // 只显示手势识别反馈，具体操作由父组件处理
    const gestureMessages = {
      'previous': { icon: '👈', text: '手势识别：返回上一页' },
      'next': { icon: '👉', text: '手势识别：前进下一页' },
      'scroll_top': { icon: '👆', text: '手势识别：返回页面顶部' },
      'scroll_bottom': { icon: '👇', text: '手势识别：滚动到页面底部' },
      'zoom_in': { icon: '👍', text: '手势识别：放大显示内容' },
      'zoom_out': { icon: '✊', text: '手势识别：缩小显示内容' },
      'confirm_action': { icon: '👌', text: '手势识别：确认当前操作' },
      'stop_action': { icon: '✋', text: '手势识别：停止当前操作' },
      'toggle_view': { icon: '✌️', text: '手势识别：切换视图模式' },
      'emergency_call': { icon: '🤙', text: '手势识别：紧急呼叫功能' },
      'rehabilitation_mode': { icon: '🤘', text: '手势识别：切换到康复训练' },
      'health_blessing': { icon: '🤟', text: '手势识别：健康祝福' }
    }

    const message = gestureMessages[action]
    if (message) {
      showGestureMessage(message.icon, message.text)
    }

    // 只有特殊功能在组件内处理
    switch (action) {
      case 'emergency_call':
        handleEmergencyCall()
        break
      case 'rehabilitation_mode':
        navigateToRehabilitation()
        break
      case 'health_blessing':
        showHealthBlessing()
        break
    }
  }
}

// 显示手势消息
const showGestureMessage = (icon, message) => {
  // 创建临时消息提示
  const messageDiv = document.createElement('div')
  messageDiv.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 20px 30px;
    border-radius: 15px;
    font-size: 18px;
    z-index: 10000;
    border: 2px solid #00ff88;
    backdrop-filter: blur(10px);
  `
  messageDiv.innerHTML = `<span style="font-size: 24px; margin-right: 10px;">${icon}</span>${message}`

  document.body.appendChild(messageDiv)

  setTimeout(() => {
    document.body.removeChild(messageDiv)
  }, 2000)
}

// 处理紧急呼叫
const handleEmergencyCall = () => {
  const emergencyModal = document.createElement('div')
  emergencyModal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 0, 0, 0.9);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10001;
    font-size: 24px;
    text-align: center;
  `
  emergencyModal.innerHTML = `
    <div style="font-size: 48px; margin-bottom: 20px;">🚨</div>
    <div style="font-size: 32px; margin-bottom: 20px;">紧急呼叫</div>
    <div style="margin-bottom: 30px;">如有紧急情况，请立即拨打120</div>
    <button onclick="this.parentElement.remove()" style="
      padding: 15px 30px;
      font-size: 18px;
      background: white;
      color: red;
      border: none;
      border-radius: 10px;
      cursor: pointer;
    ">关闭</button>
  `

  document.body.appendChild(emergencyModal)

  // 5秒后自动关闭
  setTimeout(() => {
    if (document.body.contains(emergencyModal)) {
      document.body.removeChild(emergencyModal)
    }
  }, 5000)
}

// 导航到康复训练
const navigateToRehabilitation = () => {
  if (router) {
    router.push('/personal')
  } else {
    window.location.href = '/personal'
  }
}

// 显示健康祝福
const showHealthBlessing = () => {
  const blessings = [
    '祝您身体健康！',
    '愿您早日康复！',
    '健康是最大的财富！',
    '保持积极的心态！',
    '祝您生活愉快！'
  ]

  const randomBlessing = blessings[Math.floor(Math.random() * blessings.length)]

  const blessingDiv = document.createElement('div')
  blessingDiv.style.cssText = `
    position: fixed;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    padding: 30px 40px;
    border-radius: 20px;
    font-size: 24px;
    z-index: 10000;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: heartbeat 1s ease-in-out infinite;
  `

  // 添加心跳动画
  const style = document.createElement('style')
  style.textContent = `
    @keyframes heartbeat {
      0% { transform: translate(-50%, -50%) scale(1); }
      50% { transform: translate(-50%, -50%) scale(1.05); }
      100% { transform: translate(-50%, -50%) scale(1); }
    }
  `
  document.head.appendChild(style)

  blessingDiv.innerHTML = `
    <div style="font-size: 36px; margin-bottom: 15px;">💖</div>
    <div>${randomBlessing}</div>
  `

  document.body.appendChild(blessingDiv)

  setTimeout(() => {
    document.body.removeChild(blessingDiv)
    document.head.removeChild(style)
  }, 3000)
}

// 初始化MediaPipe
const initializeMediaPipe = async () => {
  try {
    gestureStatus.value = '启动中'

    // 检查浏览器支持
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('浏览器不支持摄像头访问')
    }

    // 动态导入MediaPipe（使用CDN）
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js'
    document.head.appendChild(script)

    await new Promise((resolve, reject) => {
      script.onload = resolve
      script.onerror = reject
    })

    // 初始化Hands
    hands = new window.Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
      }
    })

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.6, // 降低检测阈值，提高敏感度
      minTrackingConfidence: 0.4   // 降低跟踪阈值，提高稳定性
    })

    hands.onResults(onResults)

    // 初始化摄像头
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    })

    if (videoElement.value) {
      videoElement.value.srcObject = stream
      await videoElement.value.play()
    }

    gestureStatus.value = '就绪'
    isSupported.value = true

  } catch (error) {
    console.error('MediaPipe初始化失败:', error)
    gestureStatus.value = '初始化失败'
    isSupported.value = false
  }
}

// 启动手势识别
const startGestureControl = async () => {
  try {
    gestureStatus.value = '启动中'

    await nextTick()

    if (!hands) {
      await initializeMediaPipe()
    }

    if (canvasElement.value) {
      canvasCtx = canvasElement.value.getContext('2d')
      canvasElement.value.width = 640
      canvasElement.value.height = 480
    }

    // 开始处理视频帧
    const processFrame = async () => {
      if (isActive.value && videoElement.value && hands) {
        await hands.send({ image: videoElement.value })
        requestAnimationFrame(processFrame)
      }
    }

    isActive.value = true
    gestureStatus.value = '运行中'
    processFrame()

  } catch (error) {
    console.error('启动手势控制失败:', error)
    gestureStatus.value = '启动失败'
  }
}

// 停止手势识别
const stopGestureControl = () => {
  isActive.value = false
  showVideo.value = false
  gestureStatus.value = '已停止'
  currentGesture.value = 'none'
  confidence.value = 0

  // 停止摄像头
  if (videoElement.value && videoElement.value.srcObject) {
    const tracks = videoElement.value.srcObject.getTracks()
    tracks.forEach(track => track.stop())
    videoElement.value.srcObject = null
  }
}

// 控制函数
const toggleGestureControl = async () => {
  if (!isActive.value) {
    await startGestureControl()
  } else {
    stopGestureControl()
  }
}

const toggleVideo = () => {
  showVideo.value = !showVideo.value
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
}

// 生命周期
onMounted(() => {
  // 组件挂载时检查支持性
  isSupported.value = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
  if (!isSupported.value) {
    gestureStatus.value = '浏览器不支持'
  }
})

onUnmounted(() => {
  stopGestureControl()
})
</script>

<style scoped>
.gesture-control {
  position: relative;
  z-index: 1000;
}

.gesture-panel {
  position: fixed;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
  color: white;
  padding: 20px;
  border-radius: 15px;
  min-width: 280px;
  max-width: 350px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(0, 255, 136, 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.gesture-panel h3 {
  margin: 0 0 15px 0;
  color: #00ff88;
  font-size: 18px;
  text-align: center;
}

.gesture-panel h4 {
  margin: 15px 0 10px 0;
  color: #88ccff;
  font-size: 14px;
}

.gesture-status {
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
  min-width: 70px;
}

.status-value {
  flex: 1;
  text-align: right;
  font-weight: bold;
}

.status-ready { color: #00ff88; }
.status-active { color: #ffaa00; }
.status-loading { color: #0088ff; }
.status-stopped { color: #888; }
.status-error { color: #ff4444; }
.status-default { color: #ccc; }

.gesture-guide {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 15px;
}

.gesture-list {
  max-height: 200px;
  overflow-y: auto;
}

.gesture-item {
  display: flex;
  align-items: center;
  margin: 8px 0;
  padding: 5px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.gesture-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.gesture-icon {
  font-size: 18px;
  margin-right: 10px;
  min-width: 25px;
}

.gesture-desc {
  font-size: 12px;
  color: #ccc;
}

.gesture-tips {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 15px;
  margin-top: 15px;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  font-size: 11px;
  color: #aaa;
  margin: 6px 0;
  padding: 4px 0;
  line-height: 1.4;
  position: relative;
  padding-left: 15px;
}

.tips-list li:before {
  content: "•";
  color: #00ff88;
  position: absolute;
  left: 0;
  top: 4px;
}

.gesture-video {
  position: fixed;
  bottom: 60px;
  right: 20px;
  width: 200px;
  height: 150px;
  border-radius: 10px;
  border: 2px solid #00ff88;
  background: black;
  object-fit: cover;
  z-index: 1002;
}

.gesture-canvas {
  position: fixed;
  bottom: 60px;
  right: 20px;
  width: 200px;
  height: 150px;
  border-radius: 10px;
  border: 2px solid #ff0088;
  pointer-events: none;
  z-index: 1002;
}

.video-hidden,
.canvas-hidden {
  display: none;
}

.gesture-controls {
  position: fixed;
  bottom: 60px;
  left: 200px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1002;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
  min-width: 140px;
}

.control-btn.primary {
  background: linear-gradient(45deg, #00ff88, #0088ff);
  color: white;
}

.control-btn.secondary {
  background: linear-gradient(45deg, #666, #888);
  color: white;
}

.control-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
}

.control-btn:disabled {
  background: #444;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-icon {
  font-size: 16px;
}

.gesture-hint {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 15px 25px;
  border-radius: 25px;
  backdrop-filter: blur(10px);
  border: 2px solid #00ff88;
  animation: pulse 1.5s infinite;
}

.hint-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hint-icon {
  font-size: 24px;
}

.hint-text {
  font-size: 16px;
  font-weight: bold;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
    transform: translate(-50%, -50%) scale(1);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 255, 136, 0);
    transform: translate(-50%, -50%) scale(1.05);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0);
    transform: translate(-50%, -50%) scale(1);
  }
}

/* 滚动条样式 */
.gesture-list::-webkit-scrollbar {
  width: 4px;
}

.gesture-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.gesture-list::-webkit-scrollbar-thumb {
  background: #00ff88;
  border-radius: 2px;
}
</style>
