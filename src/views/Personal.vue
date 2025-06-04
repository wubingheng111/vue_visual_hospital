<template>
  <div class="rehabilitation-page">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <!-- 主要内容 -->
    <div class="main-content">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-content">
          <div class="rehab-avatar">
            <div class="avatar-circle">
              <span class="avatar-icon">🏃‍♂️</span>
            </div>
            <div class="avatar-status" :class="{ online: isTraining, training: isTraining }"></div>
          </div>
          <div class="header-text">
            <h1 class="page-title">
              <span class="title-icon">💪</span>
              智能康复训练中心
            </h1>
            <p class="page-subtitle">AI驱动的个性化康复训练监督系统</p>
          </div>
          <div class="training-status">
            <div class="status-indicator" :class="{ active: isTraining }">
              <span class="status-dot"></span>
              {{ isTraining ? '训练中' : '待机中' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 调试信息面板 -->
      <div class="debug-panel" v-if="showDebugInfo">
        <div class="debug-content">
          <h4>🔧 调试信息</h4>
          <div class="debug-item">
            <span>摄像头状态:</span>
            <span :class="{ 'status-on': showCamera, 'status-off': !showCamera }">
              {{ showCamera ? '✅ 已开启' : '❌ 未开启' }}
            </span>
          </div>
          <div class="debug-item">
            <span>训练状态:</span>
            <span :class="{ 'status-on': isTraining, 'status-off': !isTraining }">
              {{ isTraining ? '🏃‍♂️ 训练中' : '⏸️ 待机' }}
            </span>
          </div>
          <div class="debug-item">
            <span>当前训练:</span>
            <span>{{ currentExercise.name || '未选择' }}</span>
          </div>
          <div class="debug-item">
            <span>浏览器支持:</span>
            <span :class="{ 'status-on': browserSupport, 'status-off': !browserSupport }">
              {{ browserSupport ? '✅ 支持' : '❌ 不支持' }}
            </span>
          </div>
        </div>
        <button @click="showDebugInfo = false" class="debug-close">×</button>
      </div>

      <!-- 摄像头预览区域 -->
      <div class="camera-section">
        <div class="camera-container" v-if="showCamera">
          <video ref="videoElement" autoplay muted class="camera-feed"></video>
          <canvas ref="canvasElement" class="pose-overlay"></canvas>

          <!-- 训练指导界面 -->
          <div class="training-overlay" v-if="isTraining">
            <div class="training-info">
              <div class="current-exercise">
                <h3>{{ currentExercise.name }}</h3>
                <p>{{ currentExercise.description }}</p>
              </div>

              <div class="training-metrics">
                <div class="metric-item">
                  <span class="metric-label">完成次数</span>
                  <span class="metric-value">{{ completedReps }}/{{ targetReps }}</span>
                </div>
                <div class="metric-item">
                  <span class="metric-label">动作质量</span>
                  <span class="metric-value" :class="getQualityClass(currentQuality)">
                    {{ currentQuality }}%
                  </span>
                </div>
                <div class="metric-item">
                  <span class="metric-label">训练时长</span>
                  <span class="metric-value">{{ formatTime(trainingTime) }}</span>
                </div>
              </div>
            </div>

            <!-- 实时反馈 -->
            <div class="feedback-panel">
              <div class="feedback-message" :class="feedbackType">
                <span class="feedback-icon">{{ feedbackIcon }}</span>
                <span class="feedback-text">{{ feedbackMessage }}</span>
              </div>
            </div>
          </div>

          <!-- 摄像头控制按钮 -->
          <div class="camera-controls">
            <button @click="toggleCamera" class="control-btn">
              <span>{{ showCamera ? '📷' : '📹' }}</span>
              {{ showCamera ? '关闭摄像头' : '开启摄像头' }}
            </button>
            <button @click="toggleTraining" class="control-btn" :class="{ active: isTraining }">
              <span>{{ isTraining ? '⏹️' : '▶️' }}</span>
              {{ isTraining ? '停止训练' : '开始训练' }}
            </button>
            <button @click="showDebugInfo = true" class="control-btn debug-btn">
              <span>🔧</span>
              调试信息
            </button>
          </div>
        </div>

        <!-- 摄像头未开启时的提示 -->
        <div class="camera-placeholder" v-else>
          <div class="placeholder-content">
            <div class="placeholder-icon">📹</div>
            <h3>摄像头未开启</h3>
            <p>请点击下方按钮开启摄像头以开始康复训练</p>
            <div class="placeholder-actions">
              <button @click="toggleCamera" class="placeholder-btn primary">
                <span>📹</span>
                开启摄像头
              </button>
              <button @click="showDebugInfo = true" class="placeholder-btn secondary">
                <span>🔧</span>
                查看调试信息
              </button>
            </div>

            <!-- 摄像头权限说明 -->
            <div class="permission-tips">
              <h4>💡 摄像头权限说明</h4>
              <ul>
                <li>首次使用需要允许浏览器访问摄像头</li>
                <li>如果权限被拒绝，请在浏览器地址栏点击摄像头图标重新授权</li>
                <li>确保没有其他应用正在使用摄像头</li>
                <li>建议使用Chrome、Firefox等现代浏览器</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 康复训练功能区域 -->
      <div class="training-section">
        <!-- 训练计划卡片 -->
        <div class="training-plan-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">📋</span>
              今日训练计划
            </h3>
            <div class="card-actions">
              <button @click="showExerciseSelector" class="select-btn">
                <span class="btn-icon">🎯</span>
                选择训练
              </button>
            </div>
          </div>

          <div class="card-content">
            <div class="exercise-grid">
              <div
                v-for="exercise in exerciseList"
                :key="exercise.id"
                class="exercise-item"
                :class="{ active: currentExercise.id === exercise.id, completed: exercise.completed }"
                @click="selectExercise(exercise)"
              >
                <div class="exercise-icon">{{ exercise.icon }}</div>
                <div class="exercise-info">
                  <h4>{{ exercise.name }}</h4>
                  <p>{{ exercise.description }}</p>
                  <div class="exercise-meta">
                    <span class="duration">{{ exercise.duration }}分钟</span>
                    <span class="difficulty" :class="exercise.difficulty">
                      {{ getDifficultyText(exercise.difficulty) }}
                    </span>
                  </div>
                </div>
                <div class="exercise-status">
                  <span v-if="exercise.completed" class="status-icon completed">✅</span>
                  <span v-else-if="currentExercise.id === exercise.id" class="status-icon active">🔄</span>
                  <span v-else class="status-icon pending">⏳</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 训练统计卡片 -->
        <div class="stats-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">📊</span>
              训练统计
            </h3>
            <div class="card-actions">
              <button @click="showDetailedStats" class="stats-btn">
                <span class="btn-icon">📈</span>
                详细报告
              </button>
            </div>
          </div>

          <div class="card-content">
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon">🔥</div>
                <div class="stat-info">
                  <div class="stat-label">连续打卡</div>
                  <div class="stat-value">{{ trainingStats.streak }}天</div>
                </div>
              </div>

              <div class="stat-item">
                <div class="stat-icon">⏱️</div>
                <div class="stat-info">
                  <div class="stat-label">总训练时长</div>
                  <div class="stat-value">{{ trainingStats.totalTime }}小时</div>
                </div>
              </div>

              <div class="stat-item">
                <div class="stat-icon">🎯</div>
                <div class="stat-info">
                  <div class="stat-label">完成率</div>
                  <div class="stat-value">{{ trainingStats.completionRate }}%</div>
                </div>
              </div>

              <div class="stat-item">
                <div class="stat-icon">⭐</div>
                <div class="stat-info">
                  <div class="stat-label">平均质量</div>
                  <div class="stat-value">{{ trainingStats.averageQuality }}%</div>
                </div>
              </div>
            </div>

            <!-- 进度条 -->
            <div class="progress-section">
              <div class="progress-item">
                <div class="progress-label">
                  <span>本周目标进度</span>
                  <span>{{ trainingStats.weeklyProgress }}/7</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (trainingStats.weeklyProgress / 7 * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 康复记录卡片 -->
        <div class="history-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">📅</span>
              训练记录
            </h3>
            <div class="card-actions">
              <button @click="showFullHistory" class="history-btn">
                <span class="btn-icon">📋</span>
                查看全部
              </button>
            </div>
          </div>

          <div class="card-content">
            <div class="history-list">
              <div
                v-for="record in recentTrainingHistory"
                :key="record.id"
                class="history-item"
              >
                <div class="history-date">
                  <span class="date-day">{{ formatDay(record.date) }}</span>
                  <span class="date-month">{{ formatMonth(record.date) }}</span>
                </div>
                <div class="history-info">
                  <h4>{{ record.exerciseName }}</h4>
                  <div class="history-meta">
                    <span class="duration">{{ record.duration }}分钟</span>
                    <span class="quality" :class="getQualityClass(record.quality)">
                      质量: {{ record.quality }}%
                    </span>
                    <span class="reps">{{ record.completedReps }}次</span>
                  </div>
                </div>
                <div class="history-status">
                  <span class="status-badge" :class="record.status">
                    {{ getStatusText(record.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快速操作区域 -->
      <div class="action-section">
        <button @click="startQuickTraining" class="action-btn primary" :disabled="isTraining">
          <span class="btn-icon">🚀</span>
          {{ isTraining ? '训练进行中...' : '快速开始训练' }}
        </button>
        <button @click="showTrainingPlan" class="action-btn secondary">
          <span class="btn-icon">📋</span>
          制定训练计划
        </button>
        <button @click="exportTrainingData" class="action-btn info">
          <span class="btn-icon">📊</span>
          导出训练数据
        </button>
        <button @click="Exit" class="action-btn danger">
          <span class="btn-icon">🚪</span>
          退出登录
        </button>
      </div>
    </div>

    <!-- 编辑信息模态框 -->
    <div v-if="editDialogVisible" class="modal-overlay" @click="closeEditDialog">
      <div class="edit-modal" @click.stop>
        <div class="modal-header">
          <h3>
            <span class="modal-icon">✏️</span>
            编辑个人信息
          </h3>
          <button @click="closeEditDialog" class="close-btn">×</button>
        </div>

        <div class="modal-content">
          <form @submit.prevent="saveEdit" class="edit-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="edit-name">
                  <span class="label-icon">👤</span>
                  姓名
                </label>
                <input
                  id="edit-name"
                  v-model="editForm.name"
                  type="text"
                  placeholder="请输入姓名"
                  required
                />
              </div>

              <div class="form-group">
                <label for="edit-username">
                  <span class="label-icon">🏷️</span>
                  用户名
                </label>
                <input
                  id="edit-username"
                  v-model="editForm.username"
                  type="text"
                  placeholder="请输入用户名"
                  required
                />
              </div>

              <div class="form-group">
                <label for="edit-gender">
                  <span class="label-icon">⚧️</span>
                  性别
                </label>
                <select id="edit-gender" v-model="editForm.gender">
                  <option value="">请选择性别</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                </select>
              </div>

              <div class="form-group">
                <label for="edit-phone">
                  <span class="label-icon">📱</span>
                  联系电话
                </label>
                <input
                  id="edit-phone"
                  v-model="editForm.phone"
                  type="tel"
                  placeholder="请输入手机号码"
                />
              </div>

              <div class="form-group full-width">
                <label for="edit-email">
                  <span class="label-icon">📧</span>
                  邮箱地址
                </label>
                <input
                  id="edit-email"
                  v-model="editForm.email"
                  type="email"
                  placeholder="请输入邮箱地址"
                />
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeEditDialog" class="btn-cancel">
                <span class="btn-icon">❌</span>
                取消
              </button>
              <button type="submit" class="btn-save" :disabled="isSaving">
                <span class="btn-icon">💾</span>
                {{ isSaving ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 修改密码模态框 -->
    <div v-if="passwordDialogVisible" class="modal-overlay" @click="closePasswordDialog">
      <div class="password-modal" @click.stop>
        <div class="modal-header">
          <h3>
            <span class="modal-icon">🔑</span>
            修改密码
          </h3>
          <button @click="closePasswordDialog" class="close-btn">×</button>
        </div>

        <div class="modal-content">
          <form @submit.prevent="savePassword" class="password-form">
            <div class="form-group">
              <label for="current-password">
                <span class="label-icon">🔒</span>
                当前密码
              </label>
              <input
                id="current-password"
                v-model="passwordForm.currentPassword"
                type="password"
                placeholder="请输入当前密码"
                required
              />
            </div>

            <div class="form-group">
              <label for="new-password">
                <span class="label-icon">🔑</span>
                新密码
              </label>
              <input
                id="new-password"
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                required
              />
            </div>

            <div class="form-group">
              <label for="confirm-password">
                <span class="label-icon">🔐</span>
                确认密码
              </label>
              <input
                id="confirm-password"
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                required
              />
            </div>

            <div class="form-actions">
              <button type="button" @click="closePasswordDialog" class="btn-cancel">
                <span class="btn-icon">❌</span>
                取消
              </button>
              <button type="submit" class="btn-save" :disabled="isChangingPassword">
                <span class="btn-icon">🔑</span>
                {{ isChangingPassword ? '修改中...' : '修改密码' }}
              </button>
            </div>
          </form>
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
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { useLoginStore } from '@/stores/login';
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { ElMessage } from 'element-plus'
import GestureControl from '@/components/GestureControl.vue'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

const router = useRouter();
const loginStore = useLoginStore();

// MediaPipe 相关引用
const videoElement = ref(null);
const canvasElement = ref(null);

// 康复训练状态
const isTraining = ref(false);
const showCamera = ref(false);
const currentExercise = ref({});
const completedReps = ref(0);
const targetReps = ref(10);
const currentQuality = ref(0);
const trainingTime = ref(0);
const feedbackMessage = ref('准备开始训练');
const feedbackType = ref('info');
const feedbackIcon = ref('💪');

// 动作状态跟踪 - 解决动作完成判断过于敏感的问题
const motionState = ref({
  isInMotion: false,           // 是否正在做动作
  motionStartTime: 0,          // 动作开始时间
  motionHoldTime: 0,           // 动作保持时间
  requiredHoldTime: 1000,      // 需要保持的时间（毫秒）
  lastMotionTime: 0,           // 上次动作时间
  motionCooldown: 2000,        // 动作间隔冷却时间（毫秒）
  consecutiveFrames: 0,        // 连续符合条件的帧数
  requiredFrames: 10,          // 需要连续的帧数
  currentPhase: 'ready'        // 动作阶段：ready, starting, holding, completing, cooldown
});

// 专业康复训练数据库 - 医学级训练项目
const exerciseCategories = ref([
  {
    id: 'upper_limb',
    name: '上肢康复',
    icon: '💪',
    description: '肩关节、肘关节、腕关节康复训练',
    exercises: [
      {
        id: 1,
        name: '肩关节前屈训练',
        description: '改善肩关节前向活动度，适用于肩周炎康复',
        icon: '🤸‍♂️',
        duration: 10,
        difficulty: 'easy',
        completed: false,
        targetReps: 15,
        targetAngle: { min: 90, max: 120 },
        medicalBasis: '基于Codman摆动理论',
        contraindications: ['急性肩关节损伤', '严重肩关节脱位'],
        benefits: ['增加肩关节活动度', '减少肩部疼痛', '改善日常生活功能'],
        instructions: [
          '站立或坐位，保持身体直立',
          '缓慢将患侧手臂向前抬起',
          '抬至最大无痛范围',
          '保持2-3秒后缓慢放下'
        ]
      },
      {
        id: 2,
        name: '肩关节外展训练',
        description: '增强肩关节外展功能，预防肩关节粘连',
        icon: '🏋️‍♂️',
        duration: 12,
        difficulty: 'medium',
        completed: false,
        targetReps: 12,
        targetAngle: { min: 80, max: 100 },
        medicalBasis: '基于关节活动度训练原理',
        contraindications: ['急性肩袖损伤'],
        benefits: ['改善肩关节外展功能', '增强三角肌力量'],
        instructions: [
          '双脚分开与肩同宽站立',
          '将手臂向身体两侧抬起',
          '抬至肩膀高度形成T字形',
          '保持姿势后缓慢放下'
        ]
      },
      {
        id: 3,
        name: '肘关节屈伸训练',
        description: '恢复肘关节正常活动度，适用于肘关节僵硬',
        icon: '💪',
        duration: 8,
        difficulty: 'easy',
        completed: false,
        targetReps: 20,
        targetAngle: { min: 30, max: 150 },
        medicalBasis: '基于关节松动技术',
        contraindications: ['肘关节急性炎症'],
        benefits: ['恢复肘关节活动度', '增强前臂肌力'],
        instructions: [
          '坐位，上臂贴近身体',
          '缓慢弯曲肘关节',
          '尽量让手接触肩膀',
          '然后缓慢伸直手臂'
        ]
      }
    ]
  },
  {
    id: 'lower_limb',
    name: '下肢康复',
    icon: '🦵',
    description: '髋关节、膝关节、踝关节康复训练',
    exercises: [
      {
        id: 4,
        name: '膝关节屈伸训练',
        description: '增强膝关节稳定性，适用于膝关节术后康复',
        icon: '🦵',
        duration: 10,
        difficulty: 'medium',
        completed: true,
        targetReps: 15,
        targetAngle: { min: 90, max: 110 },
        medicalBasis: '基于闭链运动康复理论',
        contraindications: ['急性膝关节损伤', '膝关节感染'],
        benefits: ['增强股四头肌力量', '改善膝关节稳定性'],
        instructions: [
          '坐位，双脚平放地面',
          '缓慢抬起一侧小腿',
          '伸直膝关节至最大角度',
          '保持2秒后缓慢放下'
        ]
      },
      {
        id: 5,
        name: '髋关节外展训练',
        description: '增强髋关节外展肌群，改善步态',
        icon: '🤸‍♀️',
        duration: 12,
        difficulty: 'medium',
        completed: false,
        targetReps: 12,
        targetAngle: { min: 30, max: 45 },
        medicalBasis: '基于神经肌肉再教育理论',
        contraindications: ['髋关节急性损伤'],
        benefits: ['增强臀中肌力量', '改善步态稳定性'],
        instructions: [
          '侧卧位，下侧腿弯曲支撑',
          '上侧腿保持伸直',
          '向上抬起上侧腿',
          '保持2秒后缓慢放下'
        ]
      },
      {
        id: 6,
        name: '踝关节背屈训练',
        description: '改善踝关节背屈功能，预防足下垂',
        icon: '🦶',
        duration: 8,
        difficulty: 'easy',
        completed: false,
        targetReps: 20,
        targetAngle: { min: 15, max: 20 },
        medicalBasis: '基于神经促进技术',
        contraindications: ['踝关节急性扭伤'],
        benefits: ['改善踝关节活动度', '增强胫前肌力量'],
        instructions: [
          '坐位，双腿伸直',
          '将脚尖向上勾起',
          '感受小腿前侧肌肉收缩',
          '保持2秒后放松'
        ]
      }
    ]
  },
  {
    id: 'core_stability',
    name: '核心稳定',
    icon: '🎯',
    description: '腰背部、腹部核心肌群训练',
    exercises: [
      {
        id: 7,
        name: '腰部旋转运动',
        description: '缓解腰部僵硬，增强腰椎灵活性',
        icon: '🌀',
        duration: 12,
        difficulty: 'easy',
        completed: false,
        targetReps: 10,
        targetAngle: { min: 20, max: 45 },
        medicalBasis: '基于脊柱运动学原理',
        contraindications: ['急性腰椎间盘突出', '腰椎不稳'],
        benefits: ['增加腰椎活动度', '缓解腰部肌肉紧张'],
        instructions: [
          '站立，双脚分开与肩同宽',
          '双手叉腰或交叉胸前',
          '缓慢向左右旋转腰部',
          '保持骨盆稳定不动'
        ]
      },
      {
        id: 8,
        name: '核心稳定训练',
        description: '增强核心肌群力量，改善脊柱稳定性',
        icon: '💎',
        duration: 15,
        difficulty: 'hard',
        completed: false,
        targetReps: 8,
        targetAngle: { min: 0, max: 10 },
        medicalBasis: '基于核心稳定理论',
        contraindications: ['严重腰椎疾病'],
        benefits: ['增强核心力量', '改善姿势控制'],
        instructions: [
          '俯卧位，前臂和脚尖支撑',
          '保持身体呈一条直线',
          '收紧腹部和臀部肌肉',
          '保持稳定姿势'
        ]
      }
    ]
  },
  {
    id: 'balance_coordination',
    name: '平衡协调',
    icon: '⚖️',
    description: '平衡能力、协调性、本体感觉训练',
    exercises: [
      {
        id: 9,
        name: '单腿站立平衡',
        description: '提高本体感觉，预防跌倒',
        icon: '⚖️',
        duration: 15,
        difficulty: 'hard',
        completed: false,
        targetReps: 8,
        targetAngle: { min: 0, max: 5 },
        medicalBasis: '基于感觉整合理论',
        contraindications: ['严重平衡障碍', '眩晕症'],
        benefits: ['提高平衡能力', '增强本体感觉'],
        instructions: [
          '单脚站立，另一脚抬起',
          '保持身体平衡',
          '可闭眼增加难度',
          '逐渐延长保持时间'
        ]
      },
      {
        id: 10,
        name: '动态平衡训练',
        description: '在运动中保持平衡，提高协调性',
        icon: '🤹‍♂️',
        duration: 18,
        difficulty: 'hard',
        completed: false,
        targetReps: 6,
        targetAngle: { min: 0, max: 15 },
        medicalBasis: '基于动态平衡理论',
        contraindications: ['急性前庭疾病'],
        benefits: ['提高动态平衡', '增强协调能力'],
        instructions: [
          '在一条直线上行走',
          '每步脚跟接触脚尖',
          '保持身体直立',
          '可加入转头动作'
        ]
      }
    ]
  }
]);

// 当前选中的训练类别和项目
const selectedCategory = ref('upper_limb');
const exerciseList = ref([]);

// 根据选中类别更新训练列表
const updateExerciseList = () => {
  const category = exerciseCategories.value.find(cat => cat.id === selectedCategory.value);
  if (category) {
    exerciseList.value = category.exercises;
    // 如果当前训练项目不在新列表中，选择第一个
    if (!exerciseList.value.find(ex => ex.id === currentExercise.value.id)) {
      currentExercise.value = exerciseList.value[0] || {};
    }
  }
};

// 训练统计数据
const trainingStats = ref({
  streak: 7,
  totalTime: 24.5,
  completionRate: 85,
  averageQuality: 92,
  weeklyProgress: 5
});

// 训练历史记录
const recentTrainingHistory = ref([
  {
    id: 1,
    date: new Date('2024-01-15'),
    exerciseName: '肩部外展训练',
    duration: 10,
    quality: 95,
    completedReps: 15,
    status: 'completed'
  },
  {
    id: 2,
    date: new Date('2024-01-14'),
    exerciseName: '膝关节屈伸',
    duration: 8,
    quality: 88,
    completedReps: 12,
    status: 'completed'
  },
  {
    id: 3,
    date: new Date('2024-01-13'),
    exerciseName: '腰部旋转运动',
    duration: 6,
    quality: 76,
    completedReps: 8,
    status: 'partial'
  }
]);

// 模态框状态
const editDialogVisible = ref(false);
const exerciseSelectorVisible = ref(false);
const detailedStatsVisible = ref(false);
const showDebugInfo = ref(false);

// 浏览器支持检测
const browserSupport = ref(false);

// 调试信息
const debugInfo = ref({
  currentAngle: 0,
  targetRange: '',
  detectionCount: 0
});

// 定时器
let trainingTimer = null;
let poseDetection = null;

// 工具函数
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const formatDay = (date) => {
  return date.getDate().toString().padStart(2, '0');
};

const formatMonth = (date) => {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  return months[date.getMonth()];
};

const getDifficultyText = (difficulty) => {
  const difficultyMap = {
    'easy': '简单',
    'medium': '中等',
    'hard': '困难'
  };
  return difficultyMap[difficulty] || '未知';
};

const getQualityClass = (quality) => {
  if (quality >= 90) return 'excellent';
  if (quality >= 80) return 'good';
  if (quality >= 70) return 'fair';
  return 'poor';
};

const getStatusText = (status) => {
  const statusMap = {
    'completed': '已完成',
    'partial': '部分完成',
    'failed': '未完成'
  };
  return statusMap[status] || '未知';
};

// 摄像头和训练控制
const toggleCamera = async () => {
  console.log('toggleCamera 被调用，当前状态:', showCamera.value);

  if (!showCamera.value) {
    try {
      // 检查浏览器是否支持摄像头
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        ElMessage.error('您的浏览器不支持摄像头功能');
        return;
      }

      ElMessage.info('正在请求摄像头权限...');

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user' // 前置摄像头
        }
      });

      console.log('摄像头流获取成功:', stream);

      // 先设置状态为true，让video元素渲染
      showCamera.value = true;

      // 等待DOM元素准备好
      await nextTick();

      if (videoElement.value) {
        console.log('找到videoElement，设置视频流');
        videoElement.value.srcObject = stream;

        // 等待视频加载
        videoElement.value.onloadedmetadata = () => {
          console.log('视频元数据加载完成');
          ElMessage.success('摄像头已开启');

          // 初始化MediaPipe姿态检测
          initPoseDetection();
        };

        videoElement.value.onerror = (error) => {
          console.error('视频加载错误:', error);
          ElMessage.error('视频加载失败');
          // 如果视频加载失败，重置状态
          showCamera.value = false;
          // 停止视频流
          stream.getTracks().forEach(track => track.stop());
        };

      } else {
        console.error('videoElement 仍未找到，DOM可能还未准备好');
        ElMessage.error('视频元素未找到，请稍后重试');
        // 重置状态
        showCamera.value = false;
        // 停止视频流
        stream.getTracks().forEach(track => track.stop());
      }
    } catch (error) {
      console.error('摄像头开启失败:', error);

      let errorMessage = '摄像头开启失败';
      if (error.name === 'NotAllowedError') {
        errorMessage = '摄像头权限被拒绝，请在浏览器设置中允许摄像头访问';
      } else if (error.name === 'NotFoundError') {
        errorMessage = '未找到摄像头设备';
      } else if (error.name === 'NotReadableError') {
        errorMessage = '摄像头被其他应用占用';
      }

      ElMessage.error(errorMessage);
    }
  } else {
    // 关闭摄像头
    console.log('关闭摄像头');

    if (videoElement.value && videoElement.value.srcObject) {
      const tracks = videoElement.value.srcObject.getTracks();
      tracks.forEach(track => {
        console.log('停止摄像头轨道:', track);
        track.stop();
      });
      videoElement.value.srcObject = null;
    }

    showCamera.value = false;
    stopTraining();
    ElMessage.info('摄像头已关闭');
  }
};

const toggleTraining = () => {
  if (!isTraining.value) {
    startTraining();
  } else {
    stopTraining();
  }
};

const startTraining = () => {
  console.log('startTraining 被调用，摄像头状态:', showCamera.value);

  if (!showCamera.value) {
    ElMessage.warning('请先开启摄像头');
    // 自动尝试开启摄像头
    toggleCamera();
    return;
  }

  if (!currentExercise.value.id) {
    // 默认选择第一个未完成的训练
    const nextExercise = exerciseList.value.find(ex => !ex.completed);
    if (nextExercise) {
      selectExercise(nextExercise);
    } else {
      // 如果所有训练都完成了，选择第一个训练
      if (exerciseList.value.length > 0) {
        selectExercise(exerciseList.value[0]);
      } else {
        ElMessage.warning('没有可用的训练项目');
        return;
      }
    }
  }

  isTraining.value = true;
  completedReps.value = 0;
  trainingTime.value = 0;
  targetReps.value = currentExercise.value.targetReps;

  // 开始训练计时
  trainingTimer = setInterval(() => {
    trainingTime.value++;
  }, 1000);

  // 开始姿态检测
  startPoseDetection();

  ElMessage.success(`开始${currentExercise.value.name}训练`);
  updateFeedback('开始训练，请按照指导完成动作', 'info', '💪');
};

const stopTraining = () => {
  isTraining.value = false;

  // 清除计时器
  if (trainingTimer) {
    clearInterval(trainingTimer);
    trainingTimer = null;
  }

  // 停止姿态检测
  stopPoseDetection();

  // 保存训练记录
  if (completedReps.value > 0) {
    saveTrainingRecord();
  }

  ElMessage.info('训练已停止');
  updateFeedback('训练结束，感谢您的坚持！', 'success', '🎉');
};

const selectExercise = (exercise) => {
  currentExercise.value = exercise;
  targetReps.value = exercise.targetReps;
  ElMessage.info(`已选择：${exercise.name}`);
};

const updateFeedback = (message, type, icon) => {
  feedbackMessage.value = message;
  feedbackType.value = type;
  feedbackIcon.value = icon;
};

// MediaPipe 姿态检测相关 - 真实AI实现
let pose = null;
let canvasCtx = null;

const initPoseDetection = async () => {
  try {
    console.log('初始化MediaPipe姿态检测...');

    // 动态加载MediaPipe库
    await loadMediaPipeLibrary();

    // 初始化Pose模型
    pose = new window.Pose({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
      }
    });

    // 配置Pose参数 - 启用GPU加速
    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: false,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
      // GPU加速配置
      selfieMode: false,
      upperBodyOnly: false,
      // 尝试启用GPU加速（如果支持）
      runningMode: 'VIDEO'
    });

    // 设置结果处理回调
    pose.onResults(onPoseResults);

    // 初始化画布
    if (canvasElement.value) {
      canvasCtx = canvasElement.value.getContext('2d');
      canvasElement.value.width = 640;
      canvasElement.value.height = 480;
    }

    // 检测GPU支持情况
    const gpuInfo = await detectGPUSupport();

    ElMessage.success(`AI姿态检测系统已就绪 ${gpuInfo.message}`);
    console.log('MediaPipe Pose初始化成功');
    console.log('GPU支持情况:', gpuInfo);
  } catch (error) {
    console.error('姿态检测初始化失败:', error);
    ElMessage.error('AI姿态检测初始化失败，将使用基础模式');
    // 降级到基础检测模式
    initBasicDetection();
  }
};

// 动态加载MediaPipe库
const loadMediaPipeLibrary = async () => {
  return new Promise((resolve, reject) => {
    // 检查是否已经加载
    if (window.Pose) {
      resolve();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js';
    script.onload = () => {
      console.log('MediaPipe库加载成功');
      resolve();
    };
    script.onerror = () => {
      console.error('MediaPipe库加载失败');
      reject(new Error('MediaPipe库加载失败'));
    };
    document.head.appendChild(script);
  });
};

// 检测GPU支持情况
const detectGPUSupport = async () => {
  try {
    // 检测WebGL支持
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');

    if (!gl) {
      return {
        supported: false,
        message: '(CPU模式)',
        details: 'WebGL不支持，使用CPU计算'
      };
    }

    // 获取GPU信息
    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    let gpuInfo = '未知GPU';

    if (debugInfo) {
      const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
      const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
      gpuInfo = `${vendor} ${renderer}`;
    }

    // 简单的GPU性能测试
    const startTime = performance.now();
    const testTexture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, testTexture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 256, 256, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    const endTime = performance.now();

    const isHighPerformance = (endTime - startTime) < 5; // 5ms以内认为是高性能GPU

    return {
      supported: true,
      message: isHighPerformance ? '(GPU加速)' : '(GPU基础)',
      details: {
        gpu: gpuInfo,
        webglVersion: gl.getParameter(gl.VERSION),
        performance: isHighPerformance ? 'high' : 'basic',
        testTime: `${(endTime - startTime).toFixed(2)}ms`
      }
    };
  } catch (error) {
    console.error('GPU检测失败:', error);
    return {
      supported: false,
      message: '(CPU模式)',
      details: 'GPU检测失败，使用CPU计算'
    };
  }
};

// 处理MediaPipe姿态检测结果
const onPoseResults = (results) => {
  if (!canvasCtx || !canvasElement.value) return;

  // 清空画布
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.value.width, canvasElement.value.height);

  // 绘制视频帧
  if (results.image) {
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.value.width, canvasElement.value.height);
  }

  // 如果检测到姿态关键点
  if (results.poseLandmarks) {
    // 绘制姿态关键点和连接线
    drawPoseLandmarks(canvasCtx, results.poseLandmarks);

    // 分析动作质量
    const analysis = analyzePoseQuality(results.poseLandmarks, currentExercise.value.id);
    currentQuality.value = analysis.quality;

    // 使用改进的动作完成判断逻辑
    const motionResult = processMotionDetection(analysis);

    if (motionResult.completed) {
      completedReps.value++;

      // 根据质量给出反馈
      if (analysis.quality >= 85) {
        updateFeedback(`动作${completedReps.value}完成！质量优秀！`, 'success', '🎉');
      } else if (analysis.quality >= 70) {
        updateFeedback(`动作${completedReps.value}完成！继续保持！`, 'info', '💪');
      } else {
        updateFeedback(`动作${completedReps.value}完成，注意动作标准性`, 'warning', '⚠️');
      }

      // 检查是否完成目标
      if (completedReps.value >= targetReps.value) {
        completeExercise();
      }
    } else if (motionResult.feedback) {
      // 显示动作进度反馈
      updateFeedback(motionResult.feedback, motionResult.type, motionResult.icon);
    }
  }

  canvasCtx.restore();
};

// 绘制姿态关键点
const drawPoseLandmarks = (ctx, landmarks) => {
  // 绘制关键点
  ctx.fillStyle = '#00ff88';
  landmarks.forEach((landmark) => {
    ctx.beginPath();
    ctx.arc(
      landmark.x * canvasElement.value.width,
      landmark.y * canvasElement.value.height,
      5,
      0,
      2 * Math.PI
    );
    ctx.fill();
  });

  // 绘制骨架连接线
  ctx.strokeStyle = '#00ff88';
  ctx.lineWidth = 2;

  // 定义连接关系（简化版）
  const connections = [
    [11, 12], // 肩膀
    [11, 13], [13, 15], // 左臂
    [12, 14], [14, 16], // 右臂
    [11, 23], [12, 24], // 躯干
    [23, 24], // 腰部
    [23, 25], [25, 27], // 左腿
    [24, 26], [26, 28], // 右腿
  ];

  connections.forEach(([start, end]) => {
    if (landmarks[start] && landmarks[end]) {
      ctx.beginPath();
      ctx.moveTo(
        landmarks[start].x * canvasElement.value.width,
        landmarks[start].y * canvasElement.value.height
      );
      ctx.lineTo(
        landmarks[end].x * canvasElement.value.width,
        landmarks[end].y * canvasElement.value.height
      );
      ctx.stroke();
    }
  });
};

// 分析姿态质量 - 扩展支持所有训练项目
const analyzePoseQuality = (landmarks, exerciseId) => {
  switch (exerciseId) {
    // 上肢康复训练
    case 1: // 肩关节前屈训练
      return analyzeShoulderFlexion(landmarks);
    case 2: // 肩关节外展训练
      return analyzeShoulderAbduction(landmarks);
    case 3: // 肘关节屈伸训练
      return analyzeElbowFlexion(landmarks);

    // 下肢康复训练
    case 4: // 膝关节屈伸训练
      return analyzeKneeFlexion(landmarks);
    case 5: // 髋关节外展训练
      return analyzeHipAbduction(landmarks);
    case 6: // 踝关节背屈训练
      return analyzeAnkleDorsiflexion(landmarks);

    // 核心稳定训练
    case 7: // 腰部旋转运动
      return analyzeWaistRotation(landmarks);
    case 8: // 核心稳定训练
      return analyzeCoreStability(landmarks);

    // 平衡协调训练
    case 9: // 单腿站立平衡
      return analyzeSingleLegBalance(landmarks);
    case 10: // 动态平衡训练
      return analyzeDynamicBalance(landmarks);

    default:
      return { quality: 75, isTargetPosition: false, feedback: '未知训练类型' };
  }
};

// 肩部外展分析 - 修复版本
const analyzeShoulderAbduction = (landmarks) => {
  try {
    const leftShoulder = landmarks[11];
    const rightShoulder = landmarks[12];
    const leftElbow = landmarks[13];

    if (!leftShoulder || !rightShoulder || !leftElbow) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保上半身在摄像头范围内' };
    }

    // 计算肩膀水平线
    const shoulderLineY = (leftShoulder.y + rightShoulder.y) / 2;

    // 计算左手肘相对于肩膀水平线的高度差
    const elbowLift = shoulderLineY - leftElbow.y;

    // 计算肩膀宽度作为参考
    const shoulderWidth = Math.abs(rightShoulder.x - leftShoulder.x);

    // 外展比例：肘部抬起高度相对于肩膀宽度的比例
    const abductionRatio = elbowLift / shoulderWidth;

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    // 外展训练：肘部应该抬起到肩膀水平线附近
    if (abductionRatio >= 0.3) { // 肘部抬起高度至少是肩膀宽度的30%
      isTargetPosition = true;

      if (abductionRatio >= 0.8 && abductionRatio <= 1.2) {
        quality = 95;
        feedback = '肩关节外展角度标准！';
      } else if (abductionRatio >= 0.6 && abductionRatio <= 1.4) {
        quality = 80;
        feedback = '动作良好，继续保持';
      } else {
        quality = 65;
        feedback = '请调整手臂外展角度';
      }
    } else {
      feedback = '请将手臂向两侧抬起到肩膀高度';
    }

    // 更新调试信息
    debugInfo.value.currentAngle = abductionRatio;
    debugInfo.value.targetRange = '0.8-1.2';
    debugInfo.value.detectionCount++;

    return { quality, isTargetPosition, feedback, ratio: abductionRatio };
  } catch (error) {
    console.error('肩部外展分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 计算三点角度 - 修复版本
const calculateAngle = (point1, point2, point3) => {
  // point2 是顶点（关节点）
  // 计算两个向量
  const vector1 = {
    x: point1.x - point2.x,
    y: point1.y - point2.y
  };
  const vector2 = {
    x: point3.x - point2.x,
    y: point3.y - point2.y
  };

  // 计算向量的模长
  const magnitude1 = Math.sqrt(vector1.x * vector1.x + vector1.y * vector1.y);
  const magnitude2 = Math.sqrt(vector2.x * vector2.x + vector2.y * vector2.y);

  // 避免除零错误
  if (magnitude1 === 0 || magnitude2 === 0) {
    return 0;
  }

  // 计算点积
  const dotProduct = vector1.x * vector2.x + vector1.y * vector2.y;

  // 计算夹角（弧度）
  const cosAngle = dotProduct / (magnitude1 * magnitude2);

  // 确保cosAngle在[-1, 1]范围内，避免数值误差
  const clampedCosAngle = Math.max(-1, Math.min(1, cosAngle));

  // 转换为角度
  const angle = Math.acos(clampedCosAngle) * 180.0 / Math.PI;

  return angle;
};

// 计算垂直角度（相对于垂直方向的角度）
const calculateVerticalAngle = (point1, point2) => {
  const deltaX = point2.x - point1.x;
  const deltaY = point2.y - point1.y;

  // 计算相对于垂直方向的角度
  const angle = Math.atan2(Math.abs(deltaX), Math.abs(deltaY)) * 180.0 / Math.PI;

  return angle;
};

// 计算水平角度（相对于水平方向的角度）
const calculateHorizontalAngle = (point1, point2) => {
  const deltaX = point2.x - point1.x;
  const deltaY = point2.y - point1.y;

  // 计算相对于水平方向的角度
  const angle = Math.atan2(Math.abs(deltaY), Math.abs(deltaX)) * 180.0 / Math.PI;

  return angle;
};

// 膝关节屈伸分析
const analyzeKneeFlexion = (landmarks) => {
  try {
    const leftHip = landmarks[23];
    const leftKnee = landmarks[25];
    const leftAnkle = landmarks[27];

    if (!leftHip || !leftKnee || !leftAnkle) {
      return { quality: 0, isComplete: false, feedback: '请确保下半身在摄像头范围内' };
    }

    // 计算膝关节角度
    const kneeAngle = calculateAngle(leftHip, leftKnee, leftAnkle);

    let quality = 0;
    let feedback = '';
    let isComplete = false;

    // 判断是否完成一次屈伸动作
    if (kneeAngle <= 120) { // 膝关节弯曲
      isComplete = true;

      if (kneeAngle >= 90 && kneeAngle <= 110) {
        quality = 90;
        feedback = '膝关节弯曲角度标准！';
      } else if (kneeAngle >= 80 && kneeAngle <= 130) {
        quality = 75;
        feedback = '动作良好，注意控制角度';
      } else {
        quality = 60;
        feedback = '请控制膝关节弯曲角度在90-110度';
      }
    }

    return { quality, isComplete, feedback, angle: kneeAngle };
  } catch (error) {
    console.error('膝关节分析错误:', error);
    return { quality: 0, isComplete: false, feedback: '分析出错，请重试' };
  }
};

// 腰部旋转分析
const analyzeWaistRotation = (landmarks) => {
  try {
    const leftShoulder = landmarks[11];
    const rightShoulder = landmarks[12];
    const leftHip = landmarks[23];
    const rightHip = landmarks[24];

    if (!leftShoulder || !rightShoulder || !leftHip || !rightHip) {
      return { quality: 0, isComplete: false, feedback: '请确保身体在摄像头范围内' };
    }

    // 计算肩部和髋部的角度差（旋转程度）
    const shoulderAngle = Math.atan2(rightShoulder.y - leftShoulder.y, rightShoulder.x - leftShoulder.x);
    const hipAngle = Math.atan2(rightHip.y - leftHip.y, rightHip.x - leftHip.x);
    const rotationAngle = Math.abs(shoulderAngle - hipAngle) * 180 / Math.PI;

    let quality = 0;
    let feedback = '';
    let isComplete = false;

    // 判断是否完成旋转动作
    if (rotationAngle >= 15) {
      isComplete = true;

      if (rotationAngle >= 20 && rotationAngle <= 45) {
        quality = 85;
        feedback = '腰部旋转幅度适中！';
      } else if (rotationAngle >= 10 && rotationAngle <= 60) {
        quality = 70;
        feedback = '继续保持旋转动作';
      } else {
        quality = 55;
        feedback = '注意控制旋转幅度，避免过度扭转';
      }
    }

    return { quality, isComplete, feedback, rotation: rotationAngle };
  } catch (error) {
    console.error('腰部旋转分析错误:', error);
    return { quality: 0, isComplete: false, feedback: '分析出错，请重试' };
  }
};

// 平衡训练分析
const analyzeBalance = (landmarks) => {
  try {
    const leftAnkle = landmarks[27];
    const rightAnkle = landmarks[28];
    const nose = landmarks[0];

    if (!leftAnkle || !rightAnkle || !nose) {
      return { quality: 0, isComplete: false, feedback: '请确保全身在摄像头范围内' };
    }

    // 计算身体重心稳定性
    const centerX = (leftAnkle.x + rightAnkle.x) / 2;
    const bodyStability = Math.abs(nose.x - centerX);

    // 计算双脚距离（平衡宽度）
    const feetDistance = Math.abs(leftAnkle.x - rightAnkle.x);

    let quality = 0;
    let feedback = '';
    let isComplete = true; // 平衡训练持续进行

    if (bodyStability < 0.05 && feetDistance > 0.1) {
      quality = 95;
      feedback = '平衡控制优秀！';
    } else if (bodyStability < 0.1 && feetDistance > 0.05) {
      quality = 80;
      feedback = '平衡良好，继续保持';
    } else {
      quality = 60;
      feedback = '注意保持身体平衡，双脚适当分开';
    }

    return { quality, isComplete, feedback, stability: bodyStability };
  } catch (error) {
    console.error('平衡分析错误:', error);
    return { quality: 0, isComplete: false, feedback: '分析出错，请重试' };
  }
};

// 改进的动作完成判断逻辑
const processMotionDetection = (analysis) => {
  const now = Date.now();
  const state = motionState.value;

  // 检查是否在冷却期
  if (state.currentPhase === 'cooldown' && now - state.lastMotionTime < state.motionCooldown) {
    const remainingTime = Math.ceil((state.motionCooldown - (now - state.lastMotionTime)) / 1000);
    return {
      completed: false,
      feedback: `请休息 ${remainingTime} 秒后继续下一个动作`,
      type: 'info',
      icon: '⏱️'
    };
  }

  // 如果动作质量符合要求
  if (analysis.isTargetPosition) {
    state.consecutiveFrames++;

    // 刚开始检测到动作
    if (state.currentPhase === 'ready' || state.currentPhase === 'cooldown') {
      state.currentPhase = 'starting';
      state.motionStartTime = now;
      state.consecutiveFrames = 1;

      return {
        completed: false,
        feedback: '检测到动作开始，请保持姿势...',
        type: 'info',
        icon: '🎯'
      };
    }

    // 动作进行中
    if (state.currentPhase === 'starting' && state.consecutiveFrames >= state.requiredFrames) {
      state.currentPhase = 'holding';
      state.motionHoldTime = now;

      return {
        completed: false,
        feedback: '动作姿势正确，请继续保持...',
        type: 'success',
        icon: '✅'
      };
    }

    // 检查是否保持足够时间
    if (state.currentPhase === 'holding') {
      const holdDuration = now - state.motionHoldTime;
      const progress = Math.min(100, (holdDuration / state.requiredHoldTime) * 100);

      if (holdDuration >= state.requiredHoldTime) {
        // 动作完成
        state.currentPhase = 'cooldown';
        state.lastMotionTime = now;
        state.consecutiveFrames = 0;

        return {
          completed: true,
          feedback: '动作完成！',
          type: 'success',
          icon: '🎉'
        };
      } else {
        return {
          completed: false,
          feedback: `保持动作中... ${Math.round(progress)}%`,
          type: 'info',
          icon: '⏳'
        };
      }
    }
  } else {
    // 动作不符合要求，重置状态
    if (state.currentPhase !== 'ready' && state.currentPhase !== 'cooldown') {
      state.currentPhase = 'ready';
      state.consecutiveFrames = 0;

      return {
        completed: false,
        feedback: analysis.feedback || '请调整动作姿势',
        type: 'warning',
        icon: '⚠️'
      };
    }
  }

  return {
    completed: false,
    feedback: null,
    type: 'info',
    icon: '💪'
  };
};

// 肩关节前屈分析 - 修复版本
const analyzeShoulderFlexion = (landmarks) => {
  try {
    const leftShoulder = landmarks[11];
    const leftElbow = landmarks[13];
    const leftWrist = landmarks[15];

    if (!leftShoulder || !leftElbow || !leftWrist) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保上半身在摄像头范围内' };
    }

    // 计算手臂相对于身体的前屈角度
    // 使用肩膀到肘部的向量相对于垂直方向的角度
    const armAngle = calculateVerticalAngle(leftShoulder, leftElbow);

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    // 前屈训练：手臂向前抬起，角度应该在30-60度之间（相对于垂直方向）
    if (armAngle >= 30 && armAngle <= 60) {
      isTargetPosition = true;

      if (armAngle >= 40 && armAngle <= 50) {
        quality = 95;
        feedback = '肩关节前屈角度标准！';
      } else if (armAngle >= 35 && armAngle <= 55) {
        quality = 80;
        feedback = '动作良好，继续保持';
      } else {
        quality = 65;
        feedback = '请调整手臂前屈角度';
      }
    } else if (armAngle < 30) {
      feedback = '请将手臂更多地向前抬起';
    } else {
      feedback = '手臂抬起过高，请适当降低';
    }

    return { quality, isTargetPosition, feedback, angle: armAngle };
  } catch (error) {
    console.error('肩关节前屈分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 肘关节屈伸分析
const analyzeElbowFlexion = (landmarks) => {
  try {
    const leftShoulder = landmarks[11];
    const leftElbow = landmarks[13];
    const leftWrist = landmarks[15];

    if (!leftShoulder || !leftElbow || !leftWrist) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保手臂在摄像头范围内' };
    }

    // 计算肘关节角度
    const elbowAngle = calculateAngle(leftShoulder, leftElbow, leftWrist);

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    // 判断是否完成屈伸动作（角度小于90度为屈曲）
    if (elbowAngle <= 90) {
      isTargetPosition = true;

      if (elbowAngle >= 30 && elbowAngle <= 60) {
        quality = 90;
        feedback = '肘关节屈曲角度标准！';
      } else if (elbowAngle >= 20 && elbowAngle <= 90) {
        quality = 75;
        feedback = '动作良好，注意控制角度';
      } else {
        quality = 60;
        feedback = '请控制肘关节屈曲角度';
      }
    } else {
      feedback = '请弯曲肘关节，让手接近肩膀';
    }

    return { quality, isTargetPosition, feedback, angle: elbowAngle };
  } catch (error) {
    console.error('肘关节屈伸分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 髋关节外展分析
const analyzeHipAbduction = (landmarks) => {
  try {
    const leftHip = landmarks[23];
    const leftKnee = landmarks[25];
    const rightHip = landmarks[24];

    if (!leftHip || !leftKnee || !rightHip) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保下半身在摄像头范围内' };
    }

    // 计算髋关节外展角度
    const hipDistance = Math.abs(leftKnee.x - leftHip.x);
    const normalDistance = Math.abs(rightHip.x - leftHip.x);
    const abductionRatio = hipDistance / normalDistance;

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    if (abductionRatio >= 1.2) {
      isTargetPosition = true;

      if (abductionRatio >= 1.3 && abductionRatio <= 1.8) {
        quality = 90;
        feedback = '髋关节外展幅度标准！';
      } else if (abductionRatio >= 1.2 && abductionRatio <= 2.0) {
        quality = 75;
        feedback = '动作良好，继续保持';
      } else {
        quality = 60;
        feedback = '注意控制外展幅度';
      }
    } else {
      feedback = '请将腿向外侧抬起';
    }

    return { quality, isTargetPosition, feedback, ratio: abductionRatio };
  } catch (error) {
    console.error('髋关节外展分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 踝关节背屈分析
const analyzeAnkleDorsiflexion = (landmarks) => {
  try {
    const leftKnee = landmarks[25];
    const leftAnkle = landmarks[27];
    const leftFootIndex = landmarks[31];

    if (!leftKnee || !leftAnkle || !leftFootIndex) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保腿部在摄像头范围内' };
    }

    // 计算踝关节背屈角度
    const ankleAngle = calculateAngle(leftKnee, leftAnkle, leftFootIndex);

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    if (ankleAngle >= 100) {
      isTargetPosition = true;

      if (ankleAngle >= 105 && ankleAngle <= 120) {
        quality = 90;
        feedback = '踝关节背屈角度标准！';
      } else if (ankleAngle >= 100 && ankleAngle <= 130) {
        quality = 75;
        feedback = '动作良好，继续保持';
      } else {
        quality = 60;
        feedback = '注意控制背屈角度';
      }
    } else {
      feedback = '请将脚尖向上勾起';
    }

    return { quality, isTargetPosition, feedback, angle: ankleAngle };
  } catch (error) {
    console.error('踝关节背屈分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 核心稳定训练分析
const analyzeCoreStability = (landmarks) => {
  try {
    const leftShoulder = landmarks[11];
    const rightShoulder = landmarks[12];
    const leftHip = landmarks[23];
    const rightHip = landmarks[24];

    if (!leftShoulder || !rightShoulder || !leftHip || !rightHip) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保身体在摄像头范围内' };
    }

    // 计算身体稳定性（肩部和髋部的水平度）
    const shoulderLevel = Math.abs(leftShoulder.y - rightShoulder.y);
    const hipLevel = Math.abs(leftHip.y - rightHip.y);
    const bodyStability = (shoulderLevel + hipLevel) / 2;

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    if (bodyStability < 0.05) {
      isTargetPosition = true;

      if (bodyStability < 0.02) {
        quality = 95;
        feedback = '核心稳定性优秀！';
      } else if (bodyStability < 0.03) {
        quality = 85;
        feedback = '稳定性良好，继续保持';
      } else {
        quality = 70;
        feedback = '注意保持身体稳定';
      }
    } else {
      feedback = '请收紧核心肌群，保持身体稳定';
    }

    return { quality, isTargetPosition, feedback, stability: bodyStability };
  } catch (error) {
    console.error('核心稳定分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 单腿站立平衡分析
const analyzeSingleLegBalance = (landmarks) => {
  try {
    const leftAnkle = landmarks[27];
    const rightAnkle = landmarks[28];
    const nose = landmarks[0];

    if (!leftAnkle || !rightAnkle || !nose) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保全身在摄像头范围内' };
    }

    // 检测是否为单腿站立（一只脚明显抬起）
    const feetHeightDiff = Math.abs(leftAnkle.y - rightAnkle.y);
    const centerX = (leftAnkle.x + rightAnkle.x) / 2;
    const bodyStability = Math.abs(nose.x - centerX);

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    if (feetHeightDiff > 0.1) { // 一只脚抬起
      isTargetPosition = true;

      if (bodyStability < 0.03 && feetHeightDiff > 0.15) {
        quality = 95;
        feedback = '单腿平衡控制优秀！';
      } else if (bodyStability < 0.05 && feetHeightDiff > 0.12) {
        quality = 80;
        feedback = '平衡良好，继续保持';
      } else {
        quality = 65;
        feedback = '注意保持身体平衡';
      }
    } else {
      feedback = '请抬起一只脚进行单腿站立';
    }

    return { quality, isTargetPosition, feedback, stability: bodyStability };
  } catch (error) {
    console.error('单腿平衡分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 动态平衡训练分析
const analyzeDynamicBalance = (landmarks) => {
  try {
    const leftAnkle = landmarks[27];
    const rightAnkle = landmarks[28];
    const nose = landmarks[0];

    if (!leftAnkle || !rightAnkle || !nose) {
      return { quality: 0, isTargetPosition: false, feedback: '请确保全身在摄像头范围内' };
    }

    // 检测步态和平衡（脚步交替和身体稳定性）
    const feetDistance = Math.abs(leftAnkle.x - rightAnkle.x);
    const centerX = (leftAnkle.x + rightAnkle.x) / 2;
    const bodyStability = Math.abs(nose.x - centerX);

    let quality = 0;
    let feedback = '';
    let isTargetPosition = false;

    // 动态平衡需要适当的步幅和身体稳定
    if (feetDistance > 0.05 && feetDistance < 0.3) {
      isTargetPosition = true;

      if (bodyStability < 0.04 && feetDistance > 0.1) {
        quality = 90;
        feedback = '动态平衡控制优秀！';
      } else if (bodyStability < 0.06) {
        quality = 75;
        feedback = '平衡良好，注意步幅';
      } else {
        quality = 60;
        feedback = '注意保持动态平衡';
      }
    } else {
      feedback = '请保持适当步幅进行动态平衡训练';
    }

    return { quality, isTargetPosition, feedback, stability: bodyStability };
  } catch (error) {
    console.error('动态平衡分析错误:', error);
    return { quality: 0, isTargetPosition: false, feedback: '分析出错，请重试' };
  }
};

// 降级到基础检测模式
const initBasicDetection = () => {
  console.log('使用基础检测模式');
  ElMessage.info('使用基础训练模式');
};

const startPoseDetection = () => {
  if (pose && videoElement.value) {
    // 使用真实AI检测
    const detectFrame = async () => {
      if (isTraining.value && videoElement.value) {
        await pose.send({ image: videoElement.value });
        requestAnimationFrame(detectFrame);
      }
    };
    detectFrame();
  } else {
    // 降级到模拟检测
    poseDetection = setInterval(() => {
      const quality = Math.floor(Math.random() * 30) + 70;
      currentQuality.value = quality;

      if (Math.random() > 0.7) {
        completedReps.value++;

        if (quality >= 80) {
          updateFeedback('动作标准，继续保持！', 'success', '👍');
        } else {
          updateFeedback('动作需要调整，注意姿势', 'warning', '⚠️');
        }

        if (completedReps.value >= targetReps.value) {
          completeExercise();
        }
      }
    }, 3000);
  }
};

const stopPoseDetection = () => {
  if (poseDetection) {
    clearInterval(poseDetection);
    poseDetection = null;
  }
};

const completeExercise = () => {
  // 标记训练完成
  const exercise = exerciseList.value.find(ex => ex.id === currentExercise.value.id);
  if (exercise) {
    exercise.completed = true;
  }

  // 更新统计数据
  trainingStats.value.weeklyProgress++;
  trainingStats.value.totalTime += trainingTime.value / 3600; // 转换为小时

  stopTraining();
  ElMessage.success(`恭喜完成${currentExercise.value.name}训练！`);
};

const saveTrainingRecord = () => {
  const record = {
    id: Date.now(),
    date: new Date(),
    exerciseName: currentExercise.value.name,
    duration: Math.floor(trainingTime.value / 60),
    quality: currentQuality.value,
    completedReps: completedReps.value,
    status: completedReps.value >= targetReps.value ? 'completed' : 'partial'
  };

  recentTrainingHistory.value.unshift(record);

  // 只保留最近10条记录
  if (recentTrainingHistory.value.length > 10) {
    recentTrainingHistory.value = recentTrainingHistory.value.slice(0, 10);
  }

  console.log('训练记录已保存:', record);
};

// 其他功能函数
const showExerciseSelector = () => {
  exerciseSelectorVisible.value = true;
};

const showDetailedStats = () => {
  detailedStatsVisible.value = true;
};

const showFullHistory = () => {
  ElMessage.info('查看完整训练历史');
};

const startQuickTraining = async () => {
  console.log('快速开始训练，当前摄像头状态:', showCamera.value);

  if (!showCamera.value) {
    ElMessage.info('正在开启摄像头...');
    await toggleCamera();

    // 等待摄像头完全开启
    let retryCount = 0;
    const maxRetries = 10;

    while (!showCamera.value && retryCount < maxRetries) {
      await new Promise(resolve => setTimeout(resolve, 500));
      retryCount++;
      console.log(`等待摄像头开启，重试次数: ${retryCount}`);
    }

    if (!showCamera.value) {
      ElMessage.error('摄像头开启失败，无法开始训练');
      return;
    }
  }

  // 摄像头已开启，开始训练
  setTimeout(() => {
    startTraining();
  }, 500);
};

const showTrainingPlan = () => {
  ElMessage.info('制定个性化训练计划');
};

const exportTrainingData = () => {
  const data = {
    stats: trainingStats.value,
    history: recentTrainingHistory.value,
    exercises: exerciseList.value
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `康复训练数据_${new Date().toISOString().split('T')[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);

  ElMessage.success('训练数据导出成功');
};

// 智能交互处理
const handleNavigationGesture = (action) => {
  console.log('康复训练页面手势导航:', action);

  // 将标准化的动作映射回原始手势进行处理
  const actionToGestureMap = {
    'zoom_in': 'thumbs_up',
    'stop_action': 'open_palm',
    'toggle_view': 'peace',
    'previous': 'point_left',
    'next': 'point_right',
    'scroll_top': 'point_up',
    'scroll_bottom': 'point_down',
    'zoom_out': 'fist',
    'confirm_action': 'ok_sign'
  };

  const gesture = actionToGestureMap[action];

  if (gesture) {
    if (isTraining.value) {
      // 训练中的手势控制
      switch (gesture) {
        case 'thumbs_up':
          updateFeedback('🤲 手势确认：动作完成！', 'success', '👍');
          completedReps.value++;
          ElMessage.success('🤲 手势控制：训练动作确认');
          break;
        case 'open_palm':
          stopTraining();
          ElMessage.success('🤲 手势控制：已停止训练');
          break;
        case 'peace':
          updateFeedback('🤲 继续加油！', 'info', '✌️');
          ElMessage.info('🤲 手势控制：训练鼓励');
          break;
      }
    } else {
      // 非训练状态的手势控制
      switch (gesture) {
        case 'thumbs_up':
          if (showCamera.value) {
            startTraining();
            ElMessage.success('🤲 手势控制：开始康复训练');
          } else {
            toggleCamera();
            ElMessage.success('🤲 手势控制：打开摄像头');
          }
          break;
        case 'open_palm':
          if (showCamera.value) {
            toggleCamera();
            ElMessage.success('🤲 手势控制：关闭摄像头');
          }
          break;
        case 'point_left':
          // 切换到上一个训练项目
          const currentIndex = exerciseList.value.findIndex(ex => ex.id === currentExercise.value.id);
          if (currentIndex > 0) {
            selectExercise(exerciseList.value[currentIndex - 1]);
            ElMessage.success('🤲 手势控制：切换到上一个训练项目');
          } else {
            ElMessage.warning('🤲 手势控制：已经是第一个训练项目');
          }
          break;
        case 'point_right':
          // 切换到下一个训练项目
          const nextIndex = exerciseList.value.findIndex(ex => ex.id === currentExercise.value.id);
          if (nextIndex < exerciseList.value.length - 1) {
            selectExercise(exerciseList.value[nextIndex + 1]);
            ElMessage.success('🤲 手势控制：切换到下一个训练项目');
          } else {
            ElMessage.warning('🤲 手势控制：已经是最后一个训练项目');
          }
          break;
      }
    }
  } else {
    // 处理其他标准手势
    switch (action) {
      case 'scroll_top':
        window.scrollTo({ top: 0, behavior: 'smooth' });
        ElMessage.success('🤲 手势控制：已返回页面顶部');
        break;
      case 'scroll_bottom':
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        ElMessage.success('🤲 手势控制：已滚动到页面底部');
        break;
      case 'zoom_out':
        document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString();
        ElMessage.success('🤲 手势控制：页面已缩小');
        break;
      case 'confirm_action':
        if (!isTraining.value && showCamera.value) {
          startTraining();
          ElMessage.success('🤲 手势控制：确认开始训练');
        }
        break;
      default:
        console.log('未处理的手势动作:', action);
    }
  }
};

const handleVoiceCommand = (command) => {
  console.log('语音命令:', command);

  if (command.type === 'training') {
    switch (command.action) {
      case 'start':
        startQuickTraining();
        break;
      case 'stop':
        stopTraining();
        break;
      case 'pause':
        // 暂停训练逻辑
        break;
    }
  } else if (command.type === 'camera') {
    if (command.action === 'toggle') {
      toggleCamera();
    }
  } else if (command.type === 'exercise') {
    // 语音选择训练项目
    const exerciseName = command.exerciseName;
    const exercise = exerciseList.value.find(ex =>
      ex.name.includes(exerciseName) || exerciseName.includes(ex.name)
    );
    if (exercise) {
      selectExercise(exercise);
    }
  } else if (command.type === 'navigation') {
    // 处理页面内导航命令
    switch (command.action) {
      case '开始训练':
      case '开始康复':
        startQuickTraining();
        break;
      case '停止训练':
      case '结束训练':
        stopTraining();
        break;
      case '打开摄像头':
      case '开启摄像头':
        if (!isCameraActive.value) {
          toggleCamera();
        }
        break;
      case '关闭摄像头':
        if (isCameraActive.value) {
          toggleCamera();
        }
        break;
      case '切换摄像头':
        toggleCamera();
        break;
      case '查看记录':
      case '训练记录':
        // 滚动到训练记录区域
        const recordsElement = document.querySelector('.training-records');
        if (recordsElement) {
          recordsElement.scrollIntoView({ behavior: 'smooth' });
        }
        break;
      case '个人信息':
      case '用户信息':
        // 滚动到个人信息区域
        const infoElement = document.querySelector('.user-info');
        if (infoElement) {
          infoElement.scrollIntoView({ behavior: 'smooth' });
        }
        break;
    }
  }
};

const handleVoiceResponse = (response) => {
  console.log('语音回复:', response);
};

const Exit = () => {
  // 停止所有训练活动
  if (isTraining.value) {
    stopTraining();
  }

  // 关闭摄像头
  if (showCamera.value) {
    toggleCamera();
  }

  // 重置登录信息
  loginStore.person125Info.role = '';
  loginStore.person125Info.name = '';
  loginStore.person125Info.id = '';
  loginStore.person125Info.state = false;

  // 跳转到登录页
  router.push('/login');
};

// 生命周期
onMounted(() => {
  // 检测浏览器支持
  browserSupport.value = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);

  if (!browserSupport.value) {
    ElMessage.error('您的浏览器不支持摄像头功能，请使用Chrome、Firefox等现代浏览器');
  }

  // 初始化训练数据
  updateExerciseList(); // 根据选中类别更新训练列表
  if (exerciseList.value.length > 0) {
    currentExercise.value = exerciseList.value[0];
    targetReps.value = currentExercise.value.targetReps || 10;
  }

  console.log('康复训练系统初始化完成');
  console.log('浏览器支持摄像头:', browserSupport.value);
  console.log('默认训练项目:', currentExercise.value);
});

onUnmounted(() => {
  // 清理资源
  if (trainingTimer) {
    clearInterval(trainingTimer);
  }
  if (poseDetection) {
    clearInterval(poseDetection);
  }
  if (showCamera.value) {
    toggleCamera();
  }
});
</script>

<style scoped>
/* 页面整体样式 */
.rehabilitation-page {
  min-height: 100vh;
  background: linear-gradient(135deg,
    #0a0a2e 0%,
    #16213e 25%,
    #0f3460 50%,
    #16213e 75%,
    #0a0a2e 100%);
  color: #fff;
  font-family: "微软雅黑", "PingFang SC", sans-serif;
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

.main-content {
  position: relative;
  z-index: 2;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 80px); /* 确保内容区域高度正确 */
}

/* 页面头部样式 */
.page-header {
  margin-bottom: 30px;
  position: relative;
  z-index: 10; /* 确保header在最上层 */
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
}

.header-content:hover {
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 12px 40px rgba(0, 255, 136, 0.2);
}

.rehab-avatar {
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
  background: #ccc;
}

.avatar-status.online {
  background: #00ff88;
}

.avatar-status.training {
  background: #ff6b35;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.header-text {
  flex: 1;
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

.page-subtitle {
  font-size: 16px;
  color: #ccc;
  margin: 0;
}

.training-status {
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

/* 摄像头区域样式 */
.camera-section {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.camera-container {
  position: relative;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  overflow: hidden;
  aspect-ratio: 16/9;
  width: 100%;
  max-width: 800px;
  max-height: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pose-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.training-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.7) 0%,
    transparent 30%,
    transparent 70%,
    rgba(0, 0, 0, 0.7) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
}

.training-info {
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  padding: 15px;
  backdrop-filter: blur(10px);
}

.current-exercise h3 {
  color: #00ff88;
  margin: 0 0 5px 0;
  font-size: 18px;
}

.current-exercise p {
  color: #ccc;
  margin: 0;
  font-size: 14px;
}

.training-metrics {
  display: flex;
  gap: 20px;
  margin-top: 15px;
}

.metric-item {
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 5px;
}

.metric-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #00ff88;
}

.metric-value.excellent { color: #00ff88; }
.metric-value.good { color: #ffeb3b; }
.metric-value.fair { color: #ff9800; }
.metric-value.poor { color: #f44336; }

.feedback-panel {
  align-self: center;
}

.feedback-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: bold;
  backdrop-filter: blur(10px);
}

.feedback-message.info {
  background: rgba(33, 150, 243, 0.8);
  border: 1px solid #2196f3;
}

.feedback-message.success {
  background: rgba(76, 175, 80, 0.8);
  border: 1px solid #4caf50;
}

.feedback-message.warning {
  background: rgba(255, 152, 0, 0.8);
  border: 1px solid #ff9800;
}

.feedback-message.error {
  background: rgba(244, 67, 54, 0.8);
  border: 1px solid #f44336;
}

.feedback-icon {
  font-size: 20px;
}

.camera-controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 15px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 25px;
  color: #00ff88;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.control-btn:hover {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
  transform: translateY(-2px);
}

.control-btn.active {
  background: #00ff88;
  color: #000;
  border-color: #00ff88;
}

.debug-btn {
  background: rgba(255, 193, 7, 0.1) !important;
  border-color: #ffc107 !important;
  color: #ffc107 !important;
}

/* 调试面板样式 */
.debug-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(30, 30, 60, 0.95));
  border: 2px solid #ffc107;
  border-radius: 15px;
  backdrop-filter: blur(20px);
  z-index: 10000;
  min-width: 400px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
}

.debug-content {
  padding: 20px;
}

.debug-content h4 {
  color: #ffc107;
  margin: 0 0 15px 0;
  font-size: 18px;
  text-align: center;
}

.debug-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
}

.debug-item:last-child {
  border-bottom: none;
}

.debug-item span:first-child {
  color: #ccc;
}

.status-on {
  color: #4caf50 !important;
  font-weight: bold;
}

.status-off {
  color: #f44336 !important;
  font-weight: bold;
}

.debug-close {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  color: #ffc107;
  font-size: 24px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.debug-close:hover {
  background: rgba(255, 193, 7, 0.2);
}

/* 摄像头占位符样式 */
.camera-placeholder {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(30, 30, 60, 0.8));
  border: 2px dashed rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  aspect-ratio: 16/9;
  width: 100%;
  max-width: 800px;
  max-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.placeholder-content {
  max-width: 500px;
  padding: 40px;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.placeholder-content h3 {
  color: #00ff88;
  font-size: 24px;
  margin: 0 0 10px 0;
}

.placeholder-content p {
  color: #ccc;
  font-size: 16px;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.placeholder-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
}

.placeholder-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.placeholder-btn.primary {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-color: #00ff88;
  color: #000;
}

.placeholder-btn.primary:hover {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.placeholder-btn.secondary {
  background: rgba(255, 193, 7, 0.1);
  border-color: #ffc107;
  color: #ffc107;
}

.placeholder-btn.secondary:hover {
  background: rgba(255, 193, 7, 0.2);
  transform: translateY(-2px);
}

.permission-tips {
  text-align: left;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.permission-tips h4 {
  color: #ffc107;
  font-size: 16px;
  margin: 0 0 15px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.permission-tips ul {
  margin: 0;
  padding-left: 20px;
  color: #ccc;
}

.permission-tips li {
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.4;
}

.permission-tips li:last-child {
  margin-bottom: 0;
}

/* 训练功能区域样式 */
.training-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.training-plan-card,
.stats-card,
.history-card {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.training-plan-card:hover,
.stats-card:hover,
.history-card:hover {
  border-color: rgba(0, 255, 136, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
}

.history-card {
  grid-column: 1 / -1;
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

.card-actions {
  display: flex;
  gap: 10px;
}

.select-btn,
.stats-btn,
.history-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  color: #00ff88;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.select-btn:hover,
.stats-btn:hover,
.history-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  transform: translateY(-1px);
}

.card-content {
  padding: 20px;
}

/* 训练项目网格 */
.exercise-grid {
  display: grid;
  gap: 15px;
}

.exercise-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.exercise-item:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: rgba(0, 255, 136, 0.3);
  transform: translateX(5px);
}

.exercise-item.active {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
}

.exercise-item.completed {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
}

.exercise-icon {
  font-size: 24px;
  width: 40px;
  text-align: center;
}

.exercise-info {
  flex: 1;
}

.exercise-info h4 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 16px;
}

.exercise-info p {
  margin: 0 0 8px 0;
  color: #ccc;
  font-size: 14px;
}

.exercise-meta {
  display: flex;
  gap: 15px;
}

.duration,
.difficulty {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.duration {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
}

.difficulty.easy {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.difficulty.medium {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.difficulty.hard {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.exercise-status {
  display: flex;
  align-items: center;
}

.status-icon {
  font-size: 20px;
}

.status-icon.completed {
  color: #4caf50;
}

.status-icon.active {
  color: #ff9800;
  animation: spin 2s linear infinite;
}

.status-icon.pending {
  color: #ccc;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 统计数据网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.stat-icon {
  font-size: 24px;
  width: 40px;
  text-align: center;
}

.stat-info {
  flex: 1;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #00ff88;
}

/* 进度条样式 */
.progress-section {
  margin-top: 20px;
}

.progress-item {
  margin-bottom: 15px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: #ccc;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ff88, #00cc6a);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* 训练历史列表 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.history-item:hover {
  background: rgba(0, 255, 136, 0.1);
  transform: translateX(5px);
}

.history-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
  padding: 10px;
  background: rgba(0, 255, 136, 0.1);
  border-radius: 8px;
}

.date-day {
  font-size: 18px;
  font-weight: bold;
  color: #00ff88;
  line-height: 1;
}

.date-month {
  font-size: 12px;
  color: #ccc;
}

.history-info {
  flex: 1;
}

.history-info h4 {
  margin: 0 0 5px 0;
  color: #fff;
  font-size: 16px;
}

.history-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
}

.history-meta .duration {
  color: #2196f3;
}

.history-meta .quality {
  font-weight: bold;
}

.history-meta .reps {
  color: #ccc;
}

.history-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.completed {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-badge.partial {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-badge.failed {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

/* 操作按钮区域 */
.action-section {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 30px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.primary {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-color: #00ff88;
  color: #000;
}

.action-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.action-btn.secondary {
  background: rgba(33, 150, 243, 0.1);
  border-color: #2196f3;
  color: #2196f3;
}

.action-btn.secondary:hover {
  background: rgba(33, 150, 243, 0.2);
  transform: translateY(-2px);
}

.action-btn.info {
  background: rgba(255, 193, 7, 0.1);
  border-color: #ffc107;
  color: #ffc107;
}

.action-btn.info:hover {
  background: rgba(255, 193, 7, 0.2);
  transform: translateY(-2px);
}

.action-btn.danger {
  background: rgba(244, 67, 54, 0.1);
  border-color: #f44336;
  color: #f44336;
}

.action-btn.danger:hover {
  background: rgba(244, 67, 54, 0.2);
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .training-section {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 15px;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .training-metrics {
    flex-direction: column;
    gap: 10px;
  }

  .action-section {
    flex-direction: column;
    align-items: center;
  }

  .action-btn {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
}
</style>