<template>
    <div class="dashboard" :class="{ 'fullscreen-mode': isFullscreen, 'focus-mode': focusMode }">
      <!-- 智能交互组件 -->
      <GestureControl
        @navigationGesture="handleNavigationGesture"
      />
      <VoiceInteraction
        @voiceCommand="handleVoiceCommand"
        @voiceResponse="handleVoiceResponse"
      />

      <!-- 智能交互状态提示 - 优化位置 -->
      <div class="interaction-status" v-if="showInteractionStatus">
        <div class="status-content">
          <span class="status-icon">{{ interactionStatus.icon }}</span>
          <span class="status-text">{{ interactionStatus.text }}</span>
        </div>
      </div>

      <!-- 控制面板 -->
      <div class="control-panel" v-if="showControlPanel">
        <div class="panel-header">
          <h3>智能控制中心</h3>
          <button @click="toggleControlPanel" class="close-btn">×</button>
        </div>
        <div class="panel-content">
          <div class="control-group">
            <label>显示模式</label>
            <div class="mode-buttons">
              <button @click="setDisplayMode('normal')" :class="{ active: displayMode === 'normal' }">标准</button>
              <button @click="setDisplayMode('focus')" :class="{ active: displayMode === 'focus' }">焦点</button>
              <button @click="toggleFullscreen" :class="{ active: isFullscreen }">全屏</button>
            </div>
          </div>
          <div class="control-group">
            <label>自动刷新</label>
            <div class="refresh-controls">
              <button @click="toggleAutoRefresh" :class="{ active: autoRefresh }">
                {{ autoRefresh ? '已开启' : '已关闭' }}
              </button>
              <select v-model="refreshInterval" @change="updateRefreshInterval">
                <option value="5000">5秒</option>
                <option value="10000">10秒</option>
                <option value="30000">30秒</option>
                <option value="60000">1分钟</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 快速操作按钮 -->
      <div class="quick-actions">
        <button @click="toggleControlPanel" class="action-btn" title="控制面板">
          <span>⚙️</span>
        </button>
        <button @click="refreshAllCharts" class="action-btn" title="刷新数据">
          <span>🔄</span>
        </button>
        <button @click="toggleFullscreen" class="action-btn" title="全屏模式">
          <span>{{ isFullscreen ? '🔲' : '⛶' }}</span>
        </button>
        <button @click="showHelp" class="action-btn" title="帮助">
          <span>❓</span>
        </button>
      </div>

      <!-- 主要内容区域 -->
      <div class="container" :class="{ 'loading': isLoading }">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-spinner"></div>
          <p>数据加载中...</p>
        </div>

        <!-- 新的网格布局 -->
        <div class="charts-grid">
          <!-- 顶部重要图表区域 -->
          <div class="top-section">
            <div class="chart-item large-chart all_box box_head chart-container"
                 @click="focusChart('top', 'mapEchart')"
                 :class="{ 'chart-focused': focusedChart === 'top' && focusedChartId === 'mapEchart' }">
              <Chart
                title="各省(直辖市)三甲医院数量分布"
                chart-id="mapEchart"
                :chart-width="getChartWidth('mapEchart')"
                :chart-height="getChartHeight('mapEchart')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('mapEchart', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('mapEchart', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('mapEchart')" class="export-btn">📥</button>
              </div>
            </div>

            <div class="chart-item medium-chart all_box box_head chart-container"
                 @click="focusChart('top', 'ad4')"
                 :class="{ 'chart-focused': focusedChart === 'top' && focusedChartId === 'ad4' }">
              <Chart
                title="医慧之翼问诊流程"
                chart-id="ad4"
                :chart-width="getChartWidth('ad4')"
                :chart-height="getChartHeight('ad4')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('ad4', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('ad4', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('ad4')" class="export-btn">📥</button>
              </div>
            </div>
          </div>

          <!-- 中间数据分析区域 -->
          <div class="middle-section">
            <div class="chart-item medium-chart all_box box_head chart-container"
                 @click="focusChart('middle', 'ad')"
                 :class="{ 'chart-focused': focusedChart === 'middle' && focusedChartId === 'ad' }">
              <Chart
                title="全国医院经营方式雷达图"
                chart-id="ad"
                :chart-width="getChartWidth('ad')"
                :chart-height="getChartHeight('ad')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('ad', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('ad', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('ad')" class="export-btn">📥</button>
              </div>
            </div>

            <div class="chart-item medium-chart all_box box_head chart-container"
                 @click="focusChart('middle', 'ad1')"
                 :class="{ 'chart-focused': focusedChart === 'middle' && focusedChartId === 'ad1' }">
              <Chart
                title="全国医院数量分级"
                chart-id="ad1"
                :chart-width="getChartWidth('ad1')"
                :chart-height="getChartHeight('ad1')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('ad1', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('ad1', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('ad1')" class="export-btn">📥</button>
              </div>
            </div>
          </div>

          <!-- 底部用户数据区域 -->
          <div class="bottom-section">
            <div class="chart-item medium-chart all_box box_head chart-container"
                 @click="focusChart('bottom', 'ad2')"
                 :class="{ 'chart-focused': focusedChart === 'bottom' && focusedChartId === 'ad2' }">
              <Chart
                title="线上问诊医生评分分布"
                chart-id="ad2"
                :chart-width="getChartWidth('ad2')"
                :chart-height="getChartHeight('ad2')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('ad2', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('ad2', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('ad2')" class="export-btn">📥</button>
              </div>
            </div>

            <div class="chart-item medium-chart all_box box_head chart-container"
                 @click="focusChart('bottom', 'ad3')"
                 :class="{ 'chart-focused': focusedChart === 'bottom' && focusedChartId === 'ad3' }">
              <Chart
                title="患者年龄分布"
                chart-id="ad3"
                :chart-width="getChartWidth('ad3')"
                :chart-height="getChartHeight('ad3')"
                @chartReady="onChartReady"
                @chartError="onChartError"
              />
              <div class="chart-actions">
                <button @click.stop="zoomChart('ad3', 'in')" class="zoom-btn">🔍</button>
                <button @click.stop="zoomChart('ad3', 'out')" class="zoom-btn">🔎</button>
                <button @click.stop="exportChart('ad3')" class="export-btn">📥</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 帮助模态框 -->
      <div v-if="showHelpModal" class="help-modal" @click="closeHelp">
        <div class="help-content" @click.stop>
          <div class="help-header">
            <h3>智能交互帮助</h3>
            <button @click="closeHelp" class="close-btn">×</button>
          </div>
          <div class="help-body">
            <div class="help-section">
              <h4>🤚 手势控制</h4>
              <ul>
                <li><strong>👍 点赞：</strong>放大当前图表</li>
                <li><strong>✊ 握拳：</strong>缩小当前图表</li>
                <li><strong>👈 指向左：</strong>切换到左侧图表</li>
                <li><strong>👉 指向右：</strong>切换到右侧图表</li>
                <li><strong>👌 OK手势：</strong>确认选择</li>
                <li><strong>✋ 张开手掌：</strong>停止操作</li>
              </ul>
            </div>
            <div class="help-section">
              <h4>🎤 语音控制</h4>
              <ul>
                <li><strong>"放大图表"：</strong>放大当前焦点图表</li>
                <li><strong>"缩小图表"：</strong>缩小当前焦点图表</li>
                <li><strong>"切换图表"：</strong>切换图表焦点</li>
                <li><strong>"刷新数据"：</strong>重新加载所有数据</li>
                <li><strong>"全屏模式"：</strong>进入/退出全屏</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script setup>
  import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'
  import Chart from './Chart.vue'
  import GestureControl from '@/components/GestureControl.vue'
  import VoiceInteraction from '@/components/VoiceInteraction.vue'

  // 常量定义
  const CHART_CONFIG = {
    titles: {
      'ad': '全国医院经营方式雷达图',
      'ad1': '全国医院数量分级',
      'ad2': '线上问诊医生评分分布',
      'ad3': '患者年龄分布',
      'ad4': '医慧之翼问诊流程',
      'mapEchart': '各省三甲医院分布'
    },
    defaultWidths: {
      'ad': '100%',
      'ad1': '100%',
      'ad2': '100%',
      'ad3': '100%',
      'ad4': '100%',
      'mapEchart': '100%'
    },
    defaultHeights: {
      'ad': '350px',
      'ad1': '300px',
      'ad2': '280px',
      'ad3': '260px',
      'ad4': '300px',
      'mapEchart': '300px'
    },
    sections: {
      'ad': 'middle',
      'ad1': 'middle',
      'ad4': 'top',
      'mapEchart': 'top',
      'ad2': 'bottom',
      'ad3': 'bottom'
    },
    order: ['ad', 'ad1', 'ad4', 'mapEchart', 'ad2', 'ad3']
  }

  const GESTURE_MESSAGES = {
    'point_up': { icon: '👆', text: '指向上方 - 返回顶部' },
    'point_down': { icon: '👇', text: '指向下方 - 滚动页面' }
  }

  const ACTION_MESSAGES = {
    'previous': { icon: '⬅️', text: '手势导航：返回上一页' },
    'next': { icon: '➡️', text: '手势导航：前往下一页' },
    'up': { icon: '⬆️', text: '手势导航：返回顶部' },
    'down': { icon: '⬇️', text: '手势导航：滚动到底部' },
    'select': { icon: '✅', text: '手势导航：确认选择' },
    'stop': { icon: '⏹️', text: '手势导航：停止操作' },
    'toggle_view': { icon: '🔄', text: '手势导航：切换视图模式' },
    'zoom_in': { icon: '🔍', text: '手势导航：放大显示' },
    'zoom_out': { icon: '🔎', text: '手势导航：缩小显示' }
  }

  const SYSTEM_MESSAGES = {
    'zoom_in': '语音控制：放大显示',
    'zoom_out': '语音控制：缩小显示',
    'refresh': '语音控制：刷新页面'
  }

  // 响应式数据
  const showInteractionStatus = ref(false)
  const interactionStatus = ref({ icon: '', text: '' })
  const showControlPanel = ref(false)
  const showHelpModal = ref(false)
  const isFullscreen = ref(false)
  const isLoading = ref(false)
  const autoRefresh = ref(false)
  const refreshInterval = ref(30000)
  const displayMode = ref('normal')
  const focusedChart = ref(null)
  const focusedChartId = ref(null)
  const chartInstances = ref({})
  const refreshTimer = ref(null)
  const statusTimer = ref(null)
  const errorRetryCount = ref({})
  // 计算属性
  const focusMode = computed(() => displayMode.value === 'focus')

  // 工具函数
  const debounce = (func, wait) => {
    let timeout
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout)
        func(...args)
      }
      clearTimeout(timeout)
      timeout = setTimeout(later, wait)
    }
  }

  const throttle = (func, limit) => {
    let inThrottle
    return function() {
      const args = arguments
      const context = this
      if (!inThrottle) {
        func.apply(context, args)
        inThrottle = true
        setTimeout(() => inThrottle = false, limit)
      }
    }
  }

  // 防抖状态消息显示
  const debouncedStatusMessage = debounce((icon, text, duration = 3000) => {
    // 清除之前的定时器
    if (statusTimer.value) {
      clearTimeout(statusTimer.value)
    }

    interactionStatus.value = { icon, text }
    showInteractionStatus.value = true

    statusTimer.value = setTimeout(() => {
      showInteractionStatus.value = false
      statusTimer.value = null
    }, duration)
  }, 100)

  // 显示交互状态提示
  const showStatusMessage = (icon, text, duration = 3000) => {
    debouncedStatusMessage(icon, text, duration)
  }
  // 控制面板相关
  const toggleControlPanel = () => {
    showControlPanel.value = !showControlPanel.value
  }

  const setDisplayMode = (mode) => {
    displayMode.value = mode
    if (mode === 'focus') {
      showStatusMessage('🎯', '已切换到焦点模式')
    } else {
      showStatusMessage('📊', '已切换到标准模式')
      focusedChart.value = null
      focusedChartId.value = null
    }
  }

  // 全屏控制
  const toggleFullscreen = async () => {
    try {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen()
        isFullscreen.value = true
        showStatusMessage('⛶', '已进入全屏模式')
      } else {
        await document.exitFullscreen()
        isFullscreen.value = false
        showStatusMessage('🔲', '已退出全屏模式')
      }
    } catch (error) {
      console.error('全屏操作失败:', error)
      showStatusMessage('❌', '全屏操作失败')
    }
  }

  // 自动刷新控制
  const toggleAutoRefresh = () => {
    autoRefresh.value = !autoRefresh.value
    if (autoRefresh.value) {
      startAutoRefresh()
      showStatusMessage('🔄', '自动刷新已开启')
    } else {
      stopAutoRefresh()
      showStatusMessage('⏸️', '自动刷新已关闭')
    }
  }

  const updateRefreshInterval = () => {
    if (autoRefresh.value) {
      stopAutoRefresh()
      startAutoRefresh()
    }
  }

  const startAutoRefresh = () => {
    refreshTimer.value = setInterval(() => {
      refreshAllCharts()
    }, refreshInterval.value)
  }

  const stopAutoRefresh = () => {
    if (refreshTimer.value) {
      clearInterval(refreshTimer.value)
      refreshTimer.value = null
    }
  }
  // 图表相关操作
  const focusChart = (section, chartId) => {
    if (displayMode.value === 'focus') {
      focusedChart.value = section
      focusedChartId.value = chartId
      showStatusMessage('🎯', `已聚焦到${getChartTitle(chartId)}`)
    }
  }

  const getChartTitle = (chartId) => {
    return CHART_CONFIG.titles[chartId] || '图表'
  }

  const getChartWidth = (chartId) => {
    if (focusedChartId.value === chartId && displayMode.value === 'focus') {
      return '100%'
    }
    return CHART_CONFIG.defaultWidths[chartId] || '100%'
  }

  const getChartHeight = (chartId) => {
    if (focusedChartId.value === chartId && displayMode.value === 'focus') {
      return '500px'
    }
    return CHART_CONFIG.defaultHeights[chartId] || '300px'
  }
  // 图表操作函数
  const zoomChart = (chartId, direction) => {
    const chart = chartInstances.value[chartId]
    if (chart) {
      try {
        const option = chart.getOption()
        // 实现具体的缩放逻辑
        if (direction === 'in') {
          // 放大逻辑
          chart.dispatchAction({
            type: 'dataZoom',
            start: 10,
            end: 90
          })
        } else {
          // 缩小逻辑
          chart.dispatchAction({
            type: 'dataZoom',
            start: 0,
            end: 100
          })
        }
        showStatusMessage(direction === 'in' ? '🔍' : '🔎',
          `${getChartTitle(chartId)} ${direction === 'in' ? '放大' : '缩小'}`)
      } catch (error) {
        console.error('图表缩放失败:', error)
        showStatusMessage('❌', '图表操作失败')
      }
    }
  }

  const exportChart = (chartId) => {
    const chart = chartInstances.value[chartId]
    if (chart) {
      try {
        const url = chart.getDataURL({
          type: 'png',
          pixelRatio: 2,
          backgroundColor: '#fff'
        })
        const link = document.createElement('a')
        link.download = `${getChartTitle(chartId)}.png`
        link.href = url
        link.click()
        showStatusMessage('📥', `${getChartTitle(chartId)} 导出成功`)
      } catch (error) {
        console.error('图表导出失败:', error)
        showStatusMessage('❌', '图表导出失败')
      }
    }
  }

  const refreshAllCharts = async () => {
    isLoading.value = true
    showStatusMessage('🔄', '正在刷新所有图表数据...')

    try {
      // 模拟异步数据刷新
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 重新调整所有图表大小
      Object.values(chartInstances.value).forEach(chart => {
        if (chart && chart.resize) {
          chart.resize()
        }
      })

      isLoading.value = false
      showStatusMessage('✅', '数据刷新完成')
    } catch (error) {
      console.error('数据刷新失败:', error)
      isLoading.value = false
      showStatusMessage('❌', '数据刷新失败')
    }
  }
  // 图表事件处理
  const onChartReady = (chartId, chartInstance) => {
    chartInstances.value[chartId] = chartInstance
  }

  const onChartError = (chartId, error) => {
    console.error(`图表 ${chartId} 加载失败:`, error)
    showStatusMessage('❌', `${getChartTitle(chartId)} 加载失败`)
  }

  // 帮助相关
  const showHelp = () => {
    showHelpModal.value = true
  }

  const closeHelp = () => {
    showHelpModal.value = false
  }

  // 图表切换辅助函数
  const switchToChart = (direction) => {
    const chartOrder = CHART_CONFIG.order
    const currentIndex = chartOrder.indexOf(focusedChartId.value)

    let newIndex
    if (direction === 'left') {
      newIndex = currentIndex > 0 ? currentIndex - 1 : chartOrder.length - 1
    } else {
      newIndex = currentIndex < chartOrder.length - 1 ? currentIndex + 1 : 0
    }

    const newChartId = chartOrder[newIndex]
    const section = getChartSection(newChartId)
    focusChart(section, newChartId)
  }

  const getChartSection = (chartId) => {
    return CHART_CONFIG.sections[chartId] || 'middle'
  }

  // 处理手势导航事件 - 增强版（合并原手势处理逻辑）
  const handleNavigationGesture = (action) => {
    console.log('数据大屏手势导航:', action)

    // 将标准化的动作映射回原始手势进行处理
    const actionToGestureMap = {
      'zoom_in': 'thumbs_up',
      'zoom_out': 'fist',
      'previous': 'point_left',
      'next': 'point_right',
      'confirm_action': 'ok_sign',
      'stop_action': 'open_palm',
      'toggle_view': 'peace',
      'scroll_top': 'point_up',
      'scroll_bottom': 'point_down'
    }

    const gesture = actionToGestureMap[action]

    if (gesture) {
      // 执行具体的手势操作
      switch (gesture) {
        case 'thumbs_up':
          // 简化逻辑：直接使用页面缩放，更可靠
          document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString()
          showStatusMessage('👍', '🤲 手势控制：页面已放大')
          break
        case 'fist':
          // 简化逻辑：直接使用页面缩放，更可靠
          document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString()
          showStatusMessage('✊', '🤲 手势控制：页面已缩小')
          break
        case 'point_left':
          switchToChart('left')
          showStatusMessage('👈', '🤲 手势控制：切换到上一个图表')
          break
        case 'point_right':
          switchToChart('right')
          showStatusMessage('👉', '🤲 手势控制：切换到下一个图表')
          break
        case 'ok_sign':
          if (focusedChartId.value) {
            exportChart(focusedChartId.value)
            showStatusMessage('👌', '🤲 手势控制：图表导出成功')
          } else {
            showStatusMessage('👌', '🤲 手势控制：请先选择要导出的图表')
          }
          break
        case 'open_palm':
          setDisplayMode('normal')
          showStatusMessage('✋', '🤲 手势控制：切换到标准模式')
          break
        case 'peace':
          setDisplayMode('focus')
          showStatusMessage('✌️', '🤲 手势控制：切换到专注模式')
          break
        case 'point_up':
          window.scrollTo({ top: 0, behavior: 'smooth' })
          showStatusMessage('👆', '🤲 手势控制：已返回页面顶部')
          break
        case 'point_down':
          window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
          showStatusMessage('👇', '🤲 手势控制：已滚动到页面底部')
          break
      }
    } else {
      // 处理其他标准手势
      const message = ACTION_MESSAGES[action]
      if (message) {
        showStatusMessage(message.icon, `🤲 手势控制：${message.text}`)
      }
    }
  }

  // 处理语音命令事件
  const handleVoiceCommand = (command) => {
    console.log('语音命令:', command)

    if (command.type === 'navigation') {
      showStatusMessage('🗣️', `语音导航：${command.action}`)
    } else if (command.type === 'system') {
      const message = SYSTEM_MESSAGES[command.action] || '语音控制：执行系统命令'
      showStatusMessage('🎤', message)
    }
  }

  // 处理语音回复事件
  const handleVoiceResponse = (response) => {
    console.log('语音对话:', response)
    showStatusMessage('🤖', '智能助手已回复您的问题')
  }

  // 键盘快捷键支持
  const handleKeyboardShortcuts = (event) => {
    if (event.ctrlKey || event.metaKey) {
      switch (event.key.toLowerCase()) {
        case 'f':
          event.preventDefault()
          toggleFullscreen()
          break
        case 'r':
          event.preventDefault()
          refreshAllCharts()
          break
        case 'h':
          event.preventDefault()
          showHelp()
          break
        case '`':
          event.preventDefault()
          toggleControlPanel()
          break
      }
    } else {
      switch (event.key) {
        case 'Escape':
          if (showHelpModal.value) {
            closeHelp()
          } else if (showControlPanel.value) {
            toggleControlPanel()
          }
          break
        case 'ArrowLeft':
          event.preventDefault()
          switchToChart('left')
          break
        case 'ArrowRight':
          event.preventDefault()
          switchToChart('right')
          break
      }
    }
  }

  // 监听窗口大小变化
  const handleResize = throttle(() => {
    Object.values(chartInstances.value).forEach(chart => {
      if (chart && chart.resize) {
        chart.resize()
      }
    })
  }, 300)

  // 监听全屏状态变化
  const handleFullscreenChange = () => {
    isFullscreen.value = !!document.fullscreenElement
  }

  // Watch监听器
  watch(refreshInterval, (newVal) => {
    if (autoRefresh.value) {
      stopAutoRefresh()
      startAutoRefresh()
    }
  })

  watch(displayMode, (newMode) => {
    nextTick(() => {
      Object.values(chartInstances.value).forEach(chart => {
        if (chart && chart.resize) {
          chart.resize()
        }
      })
    })
  })

  // 组件挂载时的初始化
  onMounted(() => {
    // 添加事件监听器
    window.addEventListener('resize', handleResize)
    window.addEventListener('keydown', handleKeyboardShortcuts)
    document.addEventListener('fullscreenchange', handleFullscreenChange)

    // 显示欢迎消息
    setTimeout(() => {
      showStatusMessage('🎉', '智能交互系统已启动！支持手势控制和语音交互', 5000)
    }, 1000)
  })

  // 组件卸载时的清理
  onUnmounted(() => {
    // 清理定时器
    if (refreshTimer.value) {
      clearInterval(refreshTimer.value)
    }
    if (statusTimer.value) {
      clearTimeout(statusTimer.value)
    }

    // 移除事件监听器
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('keydown', handleKeyboardShortcuts)
    document.removeEventListener('fullscreenchange', handleFullscreenChange)

    // 清理图表实例
    Object.values(chartInstances.value).forEach(chart => {
      if (chart && chart.dispose) {
        chart.dispose()
      }
    })
  })
  </script>

<style scoped>
  .dashboard {
    min-height: 100vh;
    background: linear-gradient(135deg,
      #0a0a2e 0%,
      #16213e 25%,
      #0f3460 50%,
      #16213e 75%,
      #0a0a2e 100%);
    color: #ffffff;
    font-family: "微软雅黑", "PingFang SC", sans-serif;
    position: relative;
    overflow-x: hidden;
    padding-top: 80px;
    transition: all 0.3s ease;
  }

  .dashboard::before {
    content: '';
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

  .dashboard.fullscreen-mode {
    padding-top: 0;
  }

  .dashboard.focus-mode .container {
    filter: brightness(0.7);
  }

  .dashboard.focus-mode .chart-container.chart-focused {
    filter: brightness(1.2);
    transform: scale(1.05);
    z-index: 100;
  }

  /* 控制面板样式 */
  .control-panel {
    position: fixed;
    top: 80px;
    right: 20px;
    width: 320px;
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(30, 30, 60, 0.95));
    border: 2px solid rgba(0, 255, 136, 0.4);
    border-radius: 15px;
    backdrop-filter: blur(20px);
    z-index: 1000;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
    animation: slideInRight 0.3s ease-out;
    transition: all 0.3s ease;
  }

  .control-panel:hover {
    border-color: rgba(0, 255, 136, 0.6);
    box-shadow: 0 20px 45px rgba(0, 255, 136, 0.2);
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid rgba(0, 255, 136, 0.3);
  }

  .panel-header h3 {
    color: #00ff88;
    margin: 0;
    font-size: 16px;
    font-weight: bold;
  }

  .close-btn {
    background: none;
    border: none;
    color: #00ff88;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: rgba(0, 255, 136, 0.2);
    transform: scale(1.1);
  }

  .panel-content {
    padding: 20px;
  }

  .control-group {
    margin-bottom: 20px;
  }

  .control-group label {
    display: block;
    color: #00ff88;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .mode-buttons {
    display: flex;
    gap: 8px;
  }

  .mode-buttons button {
    flex: 1;
    padding: 8px 12px;
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.3);
    color: #00ff88;
    border-radius: 8px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s ease;
  }

  .mode-buttons button:hover {
    background: rgba(0, 255, 136, 0.2);
    transform: translateY(-1px);
  }

  .mode-buttons button.active {
    background: #00ff88;
    color: #000;
    font-weight: bold;
  }

  .refresh-controls {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .refresh-controls button {
    padding: 8px 16px;
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.3);
    color: #00ff88;
    border-radius: 8px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s ease;
  }

  .refresh-controls button:hover {
    background: rgba(0, 255, 136, 0.2);
  }

  .refresh-controls button.active {
    background: #00ff88;
    color: #000;
    font-weight: bold;
  }

  .refresh-controls select {
    padding: 6px 10px;
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid rgba(0, 255, 136, 0.3);
    color: #00ff88;
    border-radius: 6px;
    font-size: 12px;
  }

  /* 快速操作按钮样式 */
  .quick-actions {
    position: fixed;
    top: 80px;
    left: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 1000;
  }

  .action-btn {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
    border: 2px solid #00ff88;
    border-radius: 50%;
    color: #00ff88;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
  }

  .action-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(30, 60, 30, 0.9));
  }

  /* 智能交互状态提示样式 */
  .interaction-status {
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    pointer-events: none;
  }

  .status-content {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
    color: white;
    padding: 16px 24px;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    border: 2px solid #00ff88;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    animation: statusFadeIn 0.3s ease-out;
    min-width: 280px;
    justify-content: center;
  }

  .status-icon {
    font-size: 24px;
    animation: iconBounce 0.6s ease-out;
  }

  .status-text {
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    color: #00ff88;
  }

  @keyframes statusFadeIn {
    from {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.8);
    }
    to {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
  }

  @keyframes iconBounce {
    0%, 20%, 60%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-10px);
    }
    80% {
      transform: translateY(-5px);
    }
  }

  .visualization {
    width: 80%; /* 设置可视化大屏内容宽度 */
    height: 80%; /* 设置可视化大屏内容高度 */
    border: 1px solid #ccc; /* 添加边框 */
    border-radius: 10px; /* 添加圆角 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  }

  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'PingFangSC-Regular', 'helvetica neue', tahoma, 'PingFang SC', 'microsoft yahei', arial, 'hiragino sans gb', sans-serif;
      overflow: hidden;
  }

  #page-3 {
      background: linear-gradient(135deg,
        #0a0a2e 0%,
        #16213e 25%,
        #0f3460 50%,
        #16213e 75%,
        #0a0a2e 100%);
      background-attachment: fixed;
      color: #fff;
      font-family: "微软雅黑", "PingFang SC", sans-serif;
      height: 100vh;
      font-size: 1rem;
      position: relative;
      overflow: hidden;
  }

  #page-3::before {
      content: '';
      position: absolute;
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

  .head {
      height: 8vh;
      width: 100%;
      background: url(./images/head_bg.png) no-repeat center center;
      background-size: 100% 100%;
  }

  h1 {
      text-align: center;
      color: rgba(255, 255, 255);
      font-weight: bold;
      line-height: 8vh;
  }

  #time {
      position: absolute;
      right: 0.33%;
      top: 0%;
      line-height: 8vh;
  }

  #showTime {
      position: relative;
      color: rgba(255, 255, 255, .7);
      padding-right: 15px;
  }

  .main_box {
      list-style: none;
      display: flex;
      justify-content: center;
      margin-top: 0.33rem;
      padding: 0.05rem;
  }

  .main_box>li {
      display: inline;
  }

  /* 新的网格布局系统 */
  .container {
    width: 100%;
    height: calc(100vh - 80px);
    padding: 20px;
    box-sizing: border-box;
    position: relative;
    z-index: 2;
    transition: all 0.3s ease;
  }

  .container.loading {
    pointer-events: none;
  }

  .charts-grid {
    height: 100%;
    display: grid;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 20px;
  }

  /* 顶部区域 - 重要图表 */
  .top-section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
    height: 100%;
  }

  /* 中间区域 - 数据分析 */
  .middle-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    height: 100%;
  }

  /* 底部区域 - 用户数据 */
  .bottom-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    height: 100%;
  }

  /* 图表项目样式 */
  .chart-item {
    display: flex;
    flex-direction: column;
    min-height: 0;
    position: relative;
  }

  .large-chart {
    /* 大图表样式 - 地图等重要图表 */
  }

  .medium-chart {
    /* 中等图表样式 - 普通数据图表 */
  }

  /* 图表内容区域 */
  .chart-item > div:first-child {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  /* 图表容器增强样式 */
  .chart-container {
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    overflow: hidden;
  }

  .chart-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
  }

  .chart-container.chart-focused {
    border: 2px solid #00ff88;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
  }

  /* 图表操作按钮 */
  .chart-actions {
    position: absolute;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 5px;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .chart-container:hover .chart-actions {
    opacity: 1;
  }

  .zoom-btn, .export-btn {
    width: 30px;
    height: 30px;
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid #00ff88;
    border-radius: 50%;
    color: #00ff88;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    transition: all 0.2s ease;
  }

  .zoom-btn:hover, .export-btn:hover {
    background: #00ff88;
    color: #000;
    transform: scale(1.1);
  }

  /* 加载状态样式 */
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    color: #00ff88;
  }

  .loading-spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(0, 255, 136, 0.3);
    border-top: 3px solid #00ff88;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .loading-overlay p {
    font-size: 16px;
    font-weight: bold;
  }

  /* 焦点模式样式 */
  .left_box.focused, .middle_box.focused, .right_box.focused {
    filter: brightness(1.2);
    transform: scale(1.02);
    z-index: 50;
  }

  .all_box {
      border: 2px solid rgba(0, 255, 136, 0.3);
      padding: 20px;
      background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
      backdrop-filter: blur(15px);
      border-radius: 15px;
      position: relative;
      z-index: 10;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
      transition: all 0.3s ease;
      overflow: hidden;
  }

  .all_box::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(45deg,
        transparent 30%,
        rgba(0, 255, 136, 0.05) 50%,
        transparent 70%);
      pointer-events: none;
      z-index: 1;
  }

  .all_box:hover {
      border-color: rgba(0, 255, 136, 0.6);
      box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
      transform: translateY(-2px);
  }

  .left_box_top {
      height: 35%;
      width: 100%;
      margin: auto;
  }

  .title {
      height: auto;
      font-size: 16px;
      font-weight: bold;
      color: #00ff88;
      text-align: center;
      padding: 15px 0;
      margin-bottom: 10px;
      position: relative;
      z-index: 2;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
      background: linear-gradient(90deg,
        transparent 0%,
        rgba(0, 255, 136, 0.1) 50%,
        transparent 100%);
      border-radius: 8px;
  }

  .title::before {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 60px;
      height: 2px;
      background: linear-gradient(90deg,
        transparent 0%,
        #00ff88 50%,
        transparent 100%);
  }

  .m_v_ul {
      list-style: none;
      display: flex;
      justify-content: center;
      justify-content: space-between;
      flex-wrap: nowrap;
      text-align: center;
  }

  .m_v_ul>li {
      font-size: 0.9rem;
      padding: 0.9rem;
  }

  h2 {
      margin: 0;
      padding: 0;
      color: #c5ccff;
  }

  .m_v_ul>li>span {
      font-size: 0.5rem;
      color: #fff;
      opacity: 0.5;
  }

  .first_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 70%;
      top: 30%;
  }

  .second_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 30%;
      top: 30%;
  }

  ._first_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 70%;
      top: 68%;
  }

  ._second_li::after {
      position: absolute;
      content: "";
      height: 1.3rem;
      width: 0.05rem;
      background: rgba(136, 172, 211, 0.37);
      right: 30%;
      top: 68%;
  }

  .box_head::before {
      position: absolute;
      width: 20px;
      height: 20px;
      content: "";
      border-top: 3px solid #00ff88;
      border-left: 3px solid #00ff88;
      top: 10px;
      left: 10px;
      border-radius: 4px 0 0 0;
      z-index: 3;
  }

  .box_head::after {
      position: absolute;
      width: 20px;
      height: 20px;
      content: "";
      border-top: 3px solid #00ff88;
      border-right: 3px solid #00ff88;
      top: 10px;
      right: 10px;
      border-radius: 0 4px 0 0;
      z-index: 3;
  }

  .box_foot::before {
      position: absolute;
      width: 20px;
      height: 20px;
      content: "";
      border-bottom: 3px solid #00ff88;
      border-left: 3px solid #00ff88;
      bottom: 10px;
      left: 10px;
      border-radius: 0 0 0 4px;
      z-index: 3;
  }

  .box_foot::after {
      position: absolute;
      width: 20px;
      height: 20px;
      content: "";
      border-bottom: 3px solid #00ff88;
      border-right: 3px solid #00ff88;
      bottom: 10px;
      right: 10px;
      border-radius: 0 0 4px 0;
      z-index: 3;
  }

  .left_box_middle {
      height: 35%;
      width: 100%;
      margin: auto;
      margin-top: 1.25rem;
  }

  #left_middle_echarts {
      height: 100%;
      width: 100%;
  }

  .left_box_down {
      height: 50%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }

  #left_down_echarts {
      height: 100%;
      width: 100%;
      margin-top: -.9rem;
      margin-left: -.6rem;
  }

  .middle_up {
      width: 100%;
      height: 100%;
      margin: auto;
  }

  .middle_box_up {
      display: flex;
      justify-content: center;
      height: 15%;
      width: 100%;
      margin: auto;
      text-align: center;
      z-index: 100;
  }

  .money_show {
      position: absolute;
      text-align: center;
      width: 39vw;
      margin: auto;
      background: rgba(101, 132, 226, .1);
      padding: 0.8rem;
  }

  .middle_up_up_box {
      height: 4.5rem;
      width: 100%;
      margin: auto;
      border: .0655rem solid rgba(25, 186, 139, .17);
      position: relative;
  }

  .now_money {
      display: flex;
      height: 4.5rem;
      margin: auto;
      line-height: 4.5rem;
      text-align: center;
      justify-content: space-around;
      overflow: hidden;
      margin-top: -0.3rem;
  }

  @font-face {
      font-family: electronicFont;
      src: url('./libs/font/Open-24-Display-St-1.ttf');
  }

  .in_money,
  .out_money {
      font-family: electronicFont;
      font-size: 3rem;
      letter-spacing: .1875rem;
      color: #ffeb7b;
      overflow: hidden;
      display: inline-block;
      width: 12.5rem;
  }

  .in_money::after {
      position: absolute;
      content: "";
      height: 1.875rem;
      width: .0625rem;
      background-color: #3e4f8d;
      right: 50%;
      top: 30%;
  }

  .middle_middle_box {
      height: 60%;
      width: 100%;
      margin: auto;
  }

  ._middle_middle_box {
      height: 100%;
      width: 100%;
      margin-top: -3rem;
      overflow: visible;
  }

  #middle_down_echarts {
      height: 100%;
      width: 39vw;
  }

  .middle_down_box {
      height: 5%;
      width: 100%;
      position: relative;
      margin-top: 10%;
      overflow: hidden;
      text-align: center;
      /* display: flex;
      justify-content: center; */
  }

  #tips {
      position: relative;
      width: 40.625rem;
      /* line-height: 3.125rem; */
      height: 3.125rem;
      margin: auto;
      overflow: hidden;
      color: #6faac8;
      text-align: center;
  }

  #tips span {
      position: absolute;
      left: 0;
      margin: 0.5rem .625rem;
      font-size: 1rem;
      white-space: nowrap;
  }

  @keyframes around1 {
      from {
          left: 0;
      }
      to {
          left: -100%;
      }
  }

  @keyframes around2 {
      from {
          left: 100%;
      }
      to {
          left: 0%;
      }
  }

  #tips .span1 {
      animation: around1 9s linear infinite;
  }

  #tips .span2 {
      animation: around2 9s linear infinite;
  }

  .middle_up_down_box {
      display: flex;
      margin: auto;
      margin-top: .25rem;
      font-size: 1rem;
      color: rgba(255, 255, 255, .7);
      justify-content: space-around;
  }

  .middle_up_up_box::before {
      position: absolute;
      width: 1rem;
      height: .5rem;
      content: "";
      border-top: .125rem solid #02a6b5;
      border-left: .125rem solid #02a6b5;
      top: 0;
      left: 0;
  }

  .now_money_foot::after {
      position: absolute;
      width: 1rem;
      height: .5rem;
      content: "";
      border-bottom: .125rem solid #02a6b5;
      border-right: .125rem solid #02a6b5;
      bottom: 0;
      right: 0;
  }

  .right_box {
      overflow: hidden;
  }

  .right_box_top {
      height: 35%;
      width: 96%;
      margin: auto;
  }

  #right_up_echarts {
      height: 100%;
      width: 100%;
      overflow: hidden;
  }

  .right_box_middle {
      height: 35%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }

  #right_middle_echarts {
      height: 100%;
      width: 100%;
      overflow: hidden;
  }

  .right_box_down {
      height: 50%;
      width: 96%;
      margin: auto;
      margin-top: 1.25rem;
  }

  #right_down_echarts {
      height: 100%;
      width: 100%;
  }

  /* 帮助模态框样式 */
  .help-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    animation: fadeIn 0.3s ease-out;
  }

  .help-content {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(30, 30, 60, 0.95));
    border: 2px solid #00ff88;
    border-radius: 15px;
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
    animation: slideInUp 0.3s ease-out;
  }

  .help-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    border-bottom: 1px solid rgba(0, 255, 136, 0.3);
  }

  .help-header h3 {
    color: #00ff88;
    margin: 0;
    font-size: 20px;
    font-weight: bold;
  }

  .help-body {
    padding: 25px;
  }

  .help-section {
    margin-bottom: 25px;
  }

  .help-section h4 {
    color: #00ff88;
    font-size: 16px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .help-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .help-section li {
    color: #fff;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 14px;
    line-height: 1.5;
  }

  .help-section li:last-child {
    border-bottom: none;
  }

  .help-section strong {
    color: #00ff88;
  }

  /* 动画效果 */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(30px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  /* 响应式设计 */
  @media (max-width: 1400px) {
    .container {
      padding: 15px;
    }

    .charts-grid {
      gap: 15px;
    }

    .top-section, .middle-section, .bottom-section {
      gap: 15px;
    }

    .all_box {
      padding: 15px;
    }

    .title {
      font-size: 14px;
      padding: 12px 0;
    }
  }

  @media (max-width: 1200px) {
    .container {
      padding: 12px;
    }

    .charts-grid {
      gap: 12px;
    }

    .top-section {
      grid-template-columns: 1.5fr 1fr;
    }

    .all_box {
      padding: 12px;
      border-radius: 12px;
    }

    .control-panel {
      width: 280px;
    }

    .title {
      font-size: 13px;
      padding: 10px 0;
    }
  }

  @media (max-width: 768px) {
    .dashboard {
      padding-top: 60px;
    }

    .container {
      padding: 8px;
    }

    .charts-grid {
      grid-template-rows: auto auto auto;
      gap: 10px;
    }

    .top-section, .middle-section, .bottom-section {
      grid-template-columns: 1fr;
      gap: 10px;
    }

    .control-panel {
      width: 250px;
      top: 70px;
      right: 10px;
    }

    .quick-actions {
      top: 70px;
      left: 10px;
    }

    .action-btn {
      width: 40px;
      height: 40px;
      font-size: 16px;
    }

    .all_box {
      padding: 10px;
      border-radius: 10px;
    }

    .title {
      font-size: 12px;
      padding: 8px 0;
    }

    .help-content {
      width: 95%;
      margin: 10px;
    }
  }

  /* 滚动条样式 */
  .help-content::-webkit-scrollbar {
    width: 8px;
  }

  .help-content::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  .help-content::-webkit-scrollbar-thumb {
    background: #00ff88;
    border-radius: 4px;
  }

  .help-content::-webkit-scrollbar-thumb:hover {
    background: #00cc6a;
  }

  </style>