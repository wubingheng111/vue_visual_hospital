<template>
  <div class="online-consultation">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="consultation-avatar">
          <div class="avatar-circle">
            <span class="avatar-icon">👨‍⚕️</span>
          </div>
          <div class="avatar-status online"></div>
        </div>
        <div class="header-text">
          <h1 class="page-title">
            <span class="title-icon">🏥</span>
            在线问诊系统
          </h1>
          <p class="page-subtitle">AI智能匹配专业医生，提供便捷高效的在线医疗服务</p>
        </div>
        <div class="consultation-status">
          <div class="status-indicator active">
            <span class="status-dot"></span>
            医生在线服务中
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-bar">
        <div class="stat-card">
          <div class="stat-icon">👨‍⚕️</div>
          <div class="stat-info">
            <div class="stat-label">在线医生</div>
            <div class="stat-value">{{ totalDoctors }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💬</div>
          <div class="stat-info">
            <div class="stat-label">今日咨询</div>
            <div class="stat-value">{{ todayConsultations }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <div class="stat-label">平均评分</div>
            <div class="stat-value">{{ averageRating }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🕐</div>
          <div class="stat-info">
            <div class="stat-label">响应时间</div>
            <div class="stat-value">&lt;5分钟</div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧：搜索和筛选区域 -->
      <div class="left-panel">
        <!-- 疾病特征搜索 -->
        <div class="search-section">
          <div class="card-header">
            <h3>
              <span class="card-icon">🔍</span>
              疾病特征搜索
            </h3>
            <div class="search-status">
              <span class="status-badge" :class="{ active: hasSearchCriteria }">
                {{ hasSearchCriteria ? '✅ 已设置条件' : '⚠️ 请设置搜索条件' }}
              </span>
            </div>
          </div>

          <div class="card-content">
            <div class="search-form">
              <div class="form-group full-width">
                <label class="form-label">
                  <span class="label-icon">🩺</span>
                  症状描述
                </label>
                <textarea
                  v-model="searchForm.symptoms"
                  class="form-textarea"
                  rows="3"
                  placeholder="请详细描述您的症状，如：头痛、发热、咳嗽等"
                  @input="handleSymptomChange"
                ></textarea>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">🏥</span>
                    科室选择
                  </label>
                  <select
                    v-model="searchForm.department"
                    class="form-select"
                    @change="handleDepartmentChange"
                  >
                    <option value="">请选择科室</option>
                    <option
                      v-for="dept in departments"
                      :key="dept"
                      :value="dept"
                    >
                      {{ dept }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">🏢</span>
                    医院等级
                  </label>
                  <select
                    v-model="searchForm.hospitalLevel"
                    class="form-select"
                    @change="handleSearch"
                  >
                    <option value="">请选择医院等级</option>
                    <option value="三甲">三甲医院</option>
                    <option value="三乙">三乙医院</option>
                    <option value="二甲">二甲医院</option>
                    <option value="专科">专科医院</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">👨‍⚕️</span>
                    医生职称
                  </label>
                  <select
                    v-model="searchForm.position"
                    class="form-select"
                    @change="handleSearch"
                  >
                    <option value="">请选择医生职称</option>
                    <option value="主任医师">主任医师</option>
                    <option value="副主任医师">副主任医师</option>
                    <option value="主治医师">主治医师</option>
                    <option value="住院医师">住院医师</option>
                  </select>
                </div>
              </div>

              <div class="search-actions">
                <button
                  @click="handleSearch"
                  class="search-btn primary"
                  :disabled="isSearching"
                >
                  <span v-if="isSearching" class="loading-spinner"></span>
                  <span class="btn-icon">{{ isSearching ? '⏳' : '🔍' }}</span>
                  <span class="btn-text">{{ isSearching ? '搜索中...' : '智能搜索' }}</span>
                </button>
                <button @click="resetSearch" class="search-btn secondary">
                  <span class="btn-icon">🔄</span>
                  <span class="btn-text">重置</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速症状选择 -->
        <div class="quick-symptoms-card">
          <div class="card-header">
            <h3>
              <span class="card-icon">⚡</span>
              常见症状快选
            </h3>
          </div>
          <div class="card-content">
            <div class="symptom-grid">
              <button
                v-for="symptom in commonSymptoms"
                :key="symptom"
                @click="toggleSymptom(symptom)"
                class="symptom-tag"
                :class="{ active: selectedSymptoms.includes(symptom) }"
              >
                {{ symptom }}
              </button>
            </div>
          </div>
        </div>

        <!-- AI智能推荐 -->
        <div class="ai-recommendation-card" v-if="aiRecommendation">
          <div class="card-header">
            <h3>
              <span class="card-icon">🤖</span>
              AI智能推荐
            </h3>
            <div class="ai-status">
              <span class="status-badge active">
                ✨ AI分析完成
              </span>
            </div>
          </div>
          <div class="card-content">
            <div class="recommendation-content">
              <div class="recommendation-text">{{ aiRecommendation }}</div>
              <div class="recommendation-actions">
                <button @click="applyRecommendation" class="recommendation-btn">
                  <span class="btn-icon">✅</span>
                  采用建议
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：医生列表 -->
      <div class="right-panel">
        <!-- 搜索结果头部 -->
        <div class="results-header">
          <div class="results-info">
            <h3>
              <span class="results-icon">👨‍⚕️</span>
              搜索结果
            </h3>
            <span class="results-count">
              <span class="count-number">{{ filteredDoctors.length }}</span>
              位医生在线
            </span>
          </div>

          <div class="sort-options">
            <label class="sort-label">
              <span class="sort-icon">📊</span>
              排序方式
            </label>
            <select v-model="sortBy" @change="handleSort" class="sort-select">
              <option value="rating-desc">评分从高到低</option>
              <option value="patients-desc">患者数从多到少</option>
              <option value="fee-asc">挂号费从低到高</option>
              <option value="fee-desc">挂号费从高到低</option>
            </select>
          </div>
        </div>

        <!-- 医生卡片列表 -->
        <div class="doctors-list" v-loading="isSearching">
          <div
            v-for="doctor in paginatedDoctors"
            :key="doctor.name"
            class="doctor-card"
            @click="selectDoctor(doctor)"
          >
            <div class="doctor-header">
              <div class="doctor-avatar">
                <div class="avatar-circle">
                  <span class="avatar-text">{{ doctor.name.charAt(0) }}</span>
                </div>
                <div class="avatar-status" :class="{ online: doctor.isOnline, offline: !doctor.isOnline }"></div>
              </div>
              <div class="doctor-basic-info">
                <h4 class="doctor-name">{{ doctor.name }}</h4>
                <p class="doctor-position">{{ doctor.position }}</p>
                <div class="doctor-rating">
                  <div class="rating-stars">
                    <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= Math.floor(doctor.rating) }">⭐</span>
                  </div>
                  <span class="rating-score">{{ doctor.rating }}</span>
                </div>
              </div>
              <div class="doctor-status">
                <span class="status-tag" :class="{ online: doctor.isOnline, offline: !doctor.isOnline }">
                  {{ getStatusText(doctor) }}
                </span>
              </div>
            </div>

            <div class="doctor-details">
              <div class="detail-row">
                <span class="detail-label">科室：</span>
                <span class="detail-value">{{ doctor.department }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">医院：</span>
                <span class="detail-value">{{ doctor.hospital }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">擅长：</span>
                <span class="detail-value specialty-text">{{ doctor.specialty }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">患者数：</span>
                <span class="detail-value">{{ doctor.patientCount }}人</span>
              </div>
            </div>

            <div class="doctor-footer">
              <div class="price-info">
                <div class="price-item">
                  <span class="price-icon">💰</span>
                  <div class="price-details">
                    <span class="price-label">挂号费</span>
                    <span class="price-value">{{ doctor.registrationFee || '暂无' }}</span>
                  </div>
                </div>
                <div class="price-item">
                  <span class="price-icon">💊</span>
                  <div class="price-details">
                    <span class="price-label">门诊费</span>
                    <span class="price-value">{{ doctor.consultationFee || '暂无' }}</span>
                  </div>
                </div>
              </div>

              <div class="action-buttons">
                <button @click.stop="viewDoctorProfile(doctor)" class="action-btn secondary">
                  <span class="btn-icon">👁️</span>
                  查看详情
                </button>
                <button @click.stop="startConsultation(doctor)" class="action-btn primary">
                  <span class="btn-icon">💬</span>
                  立即咨询
                </button>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!isSearching && filteredDoctors.length === 0" class="empty-state">
            <div class="empty-content">
              <div class="empty-icon">🔍</div>
              <h3>未找到匹配的医生</h3>
              <p>请尝试调整搜索条件或症状描述</p>
              <div class="empty-actions">
                <button @click="resetSearch" class="empty-btn">
                  <span class="btn-icon">🔄</span>
                  重新搜索
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="filteredDoctors.length > pageSize">
          <div class="pagination-info">
            <span>共 {{ filteredDoctors.length }} 位医生，每页显示 {{ pageSize }} 位</span>
          </div>
          <div class="pagination-controls">
            <button
              @click="handlePageChange(currentPage - 1)"
              :disabled="currentPage <= 1"
              class="page-btn"
            >
              ← 上一页
            </button>
            <span class="page-info">{{ currentPage }} / {{ Math.ceil(filteredDoctors.length / pageSize) }}</span>
            <button
              @click="handlePageChange(currentPage + 1)"
              :disabled="currentPage >= Math.ceil(filteredDoctors.length / pageSize)"
              class="page-btn"
            >
              下一页 →
            </button>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import axios from 'axios'
import GestureControl from '@/components/GestureControl.vue'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

const router = useRouter()

// 响应式数据
const searchForm = ref({
  symptoms: '',
  department: '',
  hospitalLevel: '',
  position: ''
})

const selectedSymptoms = ref([])
const isSearching = ref(false)
const currentPage = ref(1)
const pageSize = ref(6)
const sortBy = ref('rating-desc')
const aiRecommendation = ref('')

// 统计数据
const totalDoctors = ref(156)
const todayConsultations = ref(1247)
const averageRating = ref(4.8)

// 科室列表
const departments = ref([
  '内科', '外科', '妇产科', '儿科', '眼科', '耳鼻喉科',
  '口腔科', '皮肤科', '神经科', '心理科', '骨科', '泌尿科'
])

// 常见症状
const commonSymptoms = ref([
  '头痛', '发热', '咳嗽', '胸痛', '腹痛', '恶心',
  '呕吐', '腹泻', '便秘', '失眠', '疲劳', '头晕'
])

// 医生数据
const doctors = ref([])

// 计算属性
const hasSearchCriteria = computed(() => {
  return searchForm.value.symptoms ||
         searchForm.value.department ||
         searchForm.value.hospitalLevel ||
         searchForm.value.position ||
         selectedSymptoms.value.length > 0
})

const filteredDoctors = computed(() => {
  let result = [...doctors.value]

  // 根据搜索条件过滤
  if (searchForm.value.department) {
    result = result.filter(doctor => doctor.department === searchForm.value.department)
  }

  if (searchForm.value.hospitalLevel) {
    // 这里可以根据医院等级过滤，暂时跳过
  }

  if (searchForm.value.position) {
    result = result.filter(doctor => doctor.position === searchForm.value.position)
  }

  if (searchForm.value.symptoms) {
    // 简单的症状匹配
    result = result.filter(doctor =>
      doctor.specialty.includes(searchForm.value.symptoms) ||
      doctor.department.includes(searchForm.value.symptoms)
    )
  }

  // 排序
  switch (sortBy.value) {
    case 'rating-desc':
      result.sort((a, b) => b.rating - a.rating)
      break
    case 'patients-desc':
      result.sort((a, b) => b.patientCount - a.patientCount)
      break
    case 'fee-asc':
      result.sort((a, b) => parseInt(a.consultationFee) - parseInt(b.consultationFee))
      break
    case 'fee-desc':
      result.sort((a, b) => parseInt(b.consultationFee) - parseInt(a.consultationFee))
      break
  }

  return result
})

const paginatedDoctors = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDoctors.value.slice(start, end)
})

// 从数据库获取医生数据
const fetchDoctors = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/doctors', {
      search: '' // 空搜索获取所有医生
    })

    if (response.data && Array.isArray(response.data)) {
      doctors.value = response.data.map(doctor => ({
        ...doctor,
        id: doctor.id || Math.random().toString(36).substring(2, 9), // 生成随机ID如果没有
        rating: doctor.rating || 4.5,
        patientCount: doctor.patientCount || 0,
        isOnline: Math.random() > 0.3, // 随机在线状态
        registrationFee: doctor.registrationFee || '30元',
        consultationFee: doctor.consultationFee || '100元',
        consultationUrl: doctor.url || `/consultation/${doctor.id}` // 使用医生主页URL
      }))
      totalDoctors.value = doctors.value.length
    }
  } catch (error) {
    console.error('获取医生数据失败:', error)
    ElMessage.error('获取医生数据失败，请稍后重试')
  }
}

// 搜索医生
const searchDoctors = async () => {
  isSearching.value = true

  try {
    // 构建搜索关键词
    let searchKeyword = ''

    if (searchForm.value.symptoms) {
      searchKeyword = searchForm.value.symptoms
    } else if (searchForm.value.department) {
      searchKeyword = searchForm.value.department
    } else if (searchForm.value.position) {
      searchKeyword = searchForm.value.position
    }

    const response = await axios.post('http://127.0.0.1:8000/api/doctors', {
      search: searchKeyword
    })

    if (response.data && Array.isArray(response.data)) {
      let filteredResults = response.data

      // 前端进一步过滤
      if (searchForm.value.department) {
        filteredResults = filteredResults.filter(doctor =>
          doctor.department && doctor.department.includes(searchForm.value.department)
        )
      }

      if (searchForm.value.position) {
        filteredResults = filteredResults.filter(doctor =>
          doctor.position && doctor.position.includes(searchForm.value.position)
        )
      }

      doctors.value = filteredResults.map(doctor => ({
        ...doctor,
        id: doctor.id || Math.random().toString(36).substring(2, 9), // 修复弃用警告
        rating: doctor.rating || 4.5,
        patientCount: doctor.patientCount || 0,
        isOnline: Math.random() > 0.3,
        registrationFee: doctor.registrationFee || '30元',
        consultationFee: doctor.consultationFee || '100元',
        consultationUrl: doctor.url || `/consultation/${doctor.id}`
      }))
    }

    // 获取AI推荐
    if (searchForm.value.symptoms) {
      await getAIRecommendation()
    }

    currentPage.value = 1

    ElMessage.success(`找到 ${doctors.value.length} 位匹配的医生`)
  } catch (error) {
    console.error('搜索失败:', error)
    ElMessage.error('搜索失败，请重试')
  } finally {
    isSearching.value = false
  }
}

// 方法
const handleSearch = async () => {
  await searchDoctors()
}

const resetSearch = () => {
  searchForm.value = {
    symptoms: '',
    department: '',
    hospitalLevel: '',
    position: ''
  }
  selectedSymptoms.value = []
  aiRecommendation.value = ''
  currentPage.value = 1
}

const toggleSymptom = (symptom) => {
  const index = selectedSymptoms.value.indexOf(symptom)
  if (index > -1) {
    selectedSymptoms.value.splice(index, 1)
  } else {
    selectedSymptoms.value.push(symptom)
  }

  // 更新症状描述
  searchForm.value.symptoms = selectedSymptoms.value.join('、')
}

const handleSymptomChange = () => {
  // 症状变化时获取AI推荐
  if (searchForm.value.symptoms) {
    getAIRecommendation()
  } else {
    aiRecommendation.value = ''
  }
}

const handleDepartmentChange = () => {
  handleSearch()
}

const handleSort = () => {
  // 排序逻辑在计算属性中处理
}

const handlePageChange = (page) => {
  currentPage.value = page
}

const selectDoctor = (doctor) => {
  ElNotification({
    title: '医生信息',
    message: `您选择了 ${doctor.name} 医生`,
    type: 'info'
  })
}

const viewDoctorProfile = (doctor) => {
  ElNotification({
    title: '医生详情',
    message: `正在查看 ${doctor.name} 医生的详细信息`,
    type: 'info'
  })
}

const startConsultation = async (doctor) => {
  try {
    const result = await ElMessageBox.confirm(
      `确定要与 ${doctor.name} 医生开始咨询吗？`,
      '确认咨询',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )

    if (result === 'confirm') {
      // 如果医生有自定义的咨询URL，则跳转到该URL
      if (doctor.consultationUrl) {
        // 如果是外部链接，在新窗口打开
        if (doctor.consultationUrl.startsWith('http')) {
          window.open(doctor.consultationUrl, '_blank')
        } else {
          // 内部路由跳转
          router.push({
            path: doctor.consultationUrl,
            query: {
              doctorId: doctor.id,
              doctorName: doctor.name,
              department: doctor.department,
              hospital: doctor.hospital
            }
          })
        }
      } else {
        // 默认跳转到智能问诊页面
        router.push({
          path: '/intelligent-consultation',
          query: {
            doctorId: doctor.id,
            doctorName: doctor.name,
            department: doctor.department,
            hospital: doctor.hospital
          }
        })
      }

      ElNotification({
        title: '咨询开始',
        message: `正在为您连接 ${doctor.name} 医生...`,
        type: 'success',
        duration: 3000
      })
    }
  } catch (error) {
    // 用户取消操作
  }
}

const getAIRecommendation = async () => {
  if (!searchForm.value.symptoms) return

  try {
    // 模拟AI推荐
    const recommendations = [
      '根据您的症状，建议您咨询内科医生',
      '建议您先进行基础检查，如血常规、尿常规',
      '您的症状可能与消化系统相关，建议咨询消化内科',
      '建议您注意休息，多喝水，如症状持续请及时就医'
    ]

    const randomRecommendation = recommendations[Math.floor(Math.random() * recommendations.length)]
    aiRecommendation.value = randomRecommendation
  } catch (error) {
    console.error('获取AI推荐失败:', error)
  }
}

const applyRecommendation = () => {
  ElMessage.success('已采用AI推荐建议')
  // 这里可以根据AI推荐自动填充搜索条件
}

const getStatusText = (doctor) => {
  return doctor.isOnline ? '在线' : '离线'
}

// 智能交互处理函数

// 处理导航手势 - 优化版（避免重复执行）
const handleNavigationGesture = (action) => {
  console.log('在线问诊页面导航手势:', action)

  switch (action) {
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
    case 'zoom_in':
      // 放大页面
      document.body.style.zoom = (parseFloat(document.body.style.zoom || 1) + 0.1).toString()
      ElMessage.success('🤲 手势控制：页面已放大')
      break
    case 'zoom_out':
      // 缩小页面
      document.body.style.zoom = Math.max(0.5, parseFloat(document.body.style.zoom || 1) - 0.1).toString()
      ElMessage.success('🤲 手势控制：页面已缩小')
      break
    case 'confirm_action':
      // 执行搜索操作
      if (hasSearchCriteria.value) {
        handleSearch()
        ElMessage.success('🤲 手势控制：已执行智能搜索')
      } else {
        ElMessage.warning('🤲 手势控制：请先设置搜索条件')
      }
      break
    case 'previous':
      // 上一页
      if (currentPage.value > 1) {
        handlePageChange(currentPage.value - 1)
        ElMessage.success('🤲 手势控制：已切换到上一页')
      } else {
        ElMessage.warning('🤲 手势控制：已经是第一页了')
      }
      break
    case 'next':
      // 下一页
      const maxPage = Math.ceil(filteredDoctors.value.length / pageSize.value)
      if (currentPage.value < maxPage) {
        handlePageChange(currentPage.value + 1)
        ElMessage.success('🤲 手势控制：已切换到下一页')
      } else {
        ElMessage.warning('🤲 手势控制：已经是最后一页了')
      }
      break
    case 'stop_action':
      // 停止当前操作
      if (isSearching.value) {
        // 这里可以添加取消搜索的逻辑
        ElMessage.info('🤲 手势控制：已停止当前操作')
      }
      break
    case 'toggle_view':
      // 切换视图模式（可以切换医生卡片的显示模式）
      ElMessage.info('🤲 手势控制：切换视图模式')
      break
    default:
      console.log('未处理的手势动作:', action)
  }
}

// 处理语音命令
const handleVoiceCommand = (command) => {
  console.log('在线问诊页面语音命令:', command)

  if (command.type === 'navigation') {
    switch (command.action) {
      case '搜索医生':
      case '查找医生':
      case '智能搜索':
        if (hasSearchCriteria.value) {
          handleSearch()
          ElMessage.success('正在为您搜索医生')
        } else {
          ElMessage.warning('请先设置搜索条件或描述症状')
        }
        break
      case '重置搜索':
      case '清除条件':
        resetSearch()
        ElMessage.success('已重置搜索条件')
        break
      case '上一页':
        if (currentPage.value > 1) {
          handlePageChange(currentPage.value - 1)
          ElMessage.success('已切换到上一页')
        } else {
          ElMessage.warning('已经是第一页了')
        }
        break
      case '下一页':
        const maxPage = Math.ceil(filteredDoctors.value.length / pageSize.value)
        if (currentPage.value < maxPage) {
          handlePageChange(currentPage.value + 1)
          ElMessage.success('已切换到下一页')
        } else {
          ElMessage.warning('已经是最后一页了')
        }
        break
      case '返回顶部':
        window.scrollTo({ top: 0, behavior: 'smooth' })
        ElMessage.success('已返回页面顶部')
        break
    }
  } else if (command.type === 'search') {
    // 处理搜索相关的语音命令
    if (command.department) {
      searchForm.value.department = command.department
      ElMessage.success(`已选择科室：${command.department}`)
      handleSearch()
    }
    if (command.symptoms) {
      searchForm.value.symptoms = command.symptoms
      ElMessage.success(`已设置症状：${command.symptoms}`)
      handleSearch()
    }
  } else if (command.type === 'doctor') {
    // 处理医生相关的语音命令
    if (command.action === '咨询第一个医生' && paginatedDoctors.value.length > 0) {
      startConsultation(paginatedDoctors.value[0])
    }
  }
}

// 处理语音回复
const handleVoiceResponse = (response) => {
  console.log('在线问诊页面语音回复:', response)

  // 处理语音识别的搜索内容
  if (response.question) {
    // 智能解析语音内容
    const text = response.question.toLowerCase()

    // 检测科室关键词
    const departmentKeywords = {
      '内科': ['内科', '感冒', '发热', '头痛', '咳嗽'],
      '外科': ['外科', '外伤', '骨折', '手术'],
      '妇产科': ['妇科', '产科', '妇产科', '怀孕', '月经'],
      '儿科': ['儿科', '小儿', '孩子', '婴儿'],
      '眼科': ['眼科', '眼睛', '视力', '近视'],
      '耳鼻喉科': ['耳鼻喉', '耳朵', '鼻子', '喉咙', '咽喉'],
      '皮肤科': ['皮肤科', '皮肤', '湿疹', '过敏'],
      '心理科': ['心理', '抑郁', '焦虑', '失眠']
    }

    // 自动匹配科室
    for (const [dept, keywords] of Object.entries(departmentKeywords)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        searchForm.value.department = dept
        ElMessage.success(`根据您的描述，已自动选择${dept}`)
        break
      }
    }

    // 设置症状描述
    searchForm.value.symptoms = response.question
    ElMessage.success('已根据语音设置症状描述')

    // 自动执行搜索
    setTimeout(() => {
      handleSearch()
    }, 1000)
  }
}

// 生命周期
onMounted(async () => {
  // 初始化加载所有医生数据
  await fetchDoctors()

  // 显示语音交互提示
  setTimeout(() => {
    ElNotification({
      title: '💡 智能交互提示',
      message: '您可以使用语音描述症状或手势操作页面。例如说"我头痛发热"来搜索医生。',
      type: 'info',
      duration: 5000
    })
  }, 2000)
})
</script>

<style scoped>
/* 整体页面样式 */
.online-consultation {
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

.title-icon {
  font-size: 32px;
}

.page-subtitle {
  font-size: 16px;
  color: #ccc;
  margin: 0;
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

/* 状态栏 */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 25px;
}

.stat-card {
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

.stat-card:hover {
  border-color: rgba(0, 255, 136, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
}

.stat-card .stat-icon {
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
  font-size: 18px;
  font-weight: bold;
  color: #00ff88;
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

.left-panel {
  flex: 0 0 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  flex: 1;
}

/* 搜索区域 */
.search-section,
.quick-symptoms-card,
.ai-recommendation-card {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.search-section:hover,
.quick-symptoms-card:hover,
.ai-recommendation-card:hover {
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

.card-icon {
  font-size: 20px;
}

.search-status,
.ai-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-badge:not(.active) {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.card-content {
  padding: 20px;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
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

.search-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.search-btn.primary {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
  flex: 1;
}

.search-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.search-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  color: #00ff88;
}

.search-btn.secondary:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 16px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
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

.symptom-tag:hover,
.symptom-tag.active {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 255, 136, 0.2);
}

/* AI推荐区域 */
.recommendation-content {
  background: rgba(0, 255, 136, 0.1);
  border-radius: 10px;
  padding: 15px;
  border-left: 4px solid #00ff88;
}

.recommendation-text {
  color: #e0e0e0;
  line-height: 1.6;
  margin-bottom: 15px;
}

.recommendation-actions {
  display: flex;
  justify-content: flex-end;
}

.recommendation-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(0, 255, 136, 0.2);
  border: 1px solid #00ff88;
  border-radius: 20px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recommendation-btn:hover {
  background: #00ff88;
  color: #000;
  transform: translateY(-1px);
}

/* 搜索结果头部 */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.results-header:hover {
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
}

.results-info h3 {
  margin: 0 0 5px 0;
  color: #00ff88;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.results-icon {
  font-size: 20px;
}

.results-count {
  color: #ccc;
  font-size: 14px;
}

.count-number {
  color: #00ff88;
  font-weight: bold;
  font-size: 16px;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-label {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #ccc;
  font-size: 14px;
}

.sort-icon {
  font-size: 16px;
}

.sort-select {
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-select:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
}

/* 医生列表 */
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.doctor-card {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  padding: 25px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.doctor-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 15px 40px rgba(0, 255, 136, 0.2);
}

.doctor-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.doctor-avatar {
  position: relative;
  flex-shrink: 0;
}

.doctor-avatar .avatar-circle {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.doctor-avatar .avatar-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 3px solid #fff;
}

.doctor-avatar .avatar-status.online {
  background: #00ff88;
  animation: pulse 2s infinite;
}

.doctor-avatar .avatar-status.offline {
  background: #f44336;
}

.avatar-text {
  font-size: 24px;
  font-weight: bold;
  color: #000;
}

.doctor-basic-info {
  flex: 1;
}

.doctor-name {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
}

.doctor-position {
  margin: 0 0 12px 0;
  color: #00ff88;
  font-size: 14px;
  font-weight: 500;
}

.doctor-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 14px;
  opacity: 0.3;
  transition: all 0.2s ease;
}

.star.filled {
  opacity: 1;
}

.rating-score {
  color: #00ff88;
  font-weight: bold;
  font-size: 14px;
}

.doctor-status {
  flex-shrink: 0;
}

.status-tag {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
  border: 1px solid;
}

.status-tag.online {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border-color: #4caf50;
}

.status-tag.offline {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border-color: #f44336;
}

/* 医生详情信息 */
.doctor-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  border: 1px solid rgba(0, 255, 136, 0.2);
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-label {
  color: #ccc;
  font-size: 12px;
  min-width: 70px;
}

.detail-value {
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
}

.specialty-text {
  color: #00ff88;
}

/* 医生卡片底部 */
.doctor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 255, 136, 0.2);
}

.price-info {
  display: flex;
  gap: 20px;
}

.price-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-icon {
  font-size: 16px;
  color: #00ff88;
}

.price-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.price-label {
  color: #ccc;
  font-size: 12px;
}

.price-value {
  color: #00ff88;
  font-weight: bold;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.action-btn.primary {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 136, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  color: #00ff88;
}

.action-btn.secondary:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

/* 空状态 */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
  max-width: 400px;
  padding: 40px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-content h3 {
  margin: 0 0 15px 0;
  color: #00ff88;
  font-size: 20px;
}

.empty-content p {
  margin: 0 0 25px 0;
  color: #ccc;
  line-height: 1.5;
}

.empty-actions {
  display: flex;
  justify-content: center;
}

.empty-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty-btn:hover {
  background: linear-gradient(135deg, #00cc6a, #009955);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
  padding: 20px;
}

.pagination-info {
  color: #ccc;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.page-btn {
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 25px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.page-btn:hover:not(:disabled) {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.page-info {
  color: #00ff88;
  font-weight: bold;
  font-size: 16px;
  min-width: 80px;
  text-align: center;
}

/* 动画效果 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 255, 136, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.doctor-card {
  animation: fadeInUp 0.6s ease-out;
}

.doctor-card:nth-child(2) {
  animation-delay: 0.1s;
}

.doctor-card:nth-child(3) {
  animation-delay: 0.2s;
}

.doctor-card:nth-child(4) {
  animation-delay: 0.3s;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    flex-direction: column;
  }

  .left-panel {
    flex: none;
    width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .online-consultation {
    padding-top: 60px;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 15px;
    padding: 20px;
  }

  .consultation-avatar .avatar-circle {
    width: 60px;
    height: 60px;
    font-size: 24px;
  }

  .page-title {
    font-size: 24px;
  }

  .stats-bar {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .main-content {
    padding: 15px;
    gap: 20px;
  }

  .doctor-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .doctor-avatar .avatar-circle {
    width: 60px;
    height: 60px;
    font-size: 20px;
  }

  .doctor-details {
    grid-template-columns: 1fr;
  }

  .doctor-footer {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .price-info {
    justify-content: center;
  }

  .action-buttons {
    justify-content: center;
  }

  .pagination-controls {
    flex-direction: column;
    gap: 10px;
  }

  .symptom-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 15px;
  }

  .page-title {
    font-size: 20px;
  }

  .main-content {
    padding: 10px;
  }

  .doctor-card {
    padding: 20px;
  }

  .search-actions {
    flex-direction: column;
  }

  .symptom-grid {
    grid-template-columns: 1fr;
  }
}
</style>
