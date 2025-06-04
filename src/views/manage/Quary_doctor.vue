<template>
  <div class="online-consultation">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon">👨‍⚕️</span>
          在线问诊系统
        </h1>
        <p class="page-subtitle">根据疾病特征智能匹配专业医生，提供便捷的在线医疗服务</p>
      </div>

      <!-- 统计信息 -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-number">{{ totalDoctors }}</span>
          <span class="stat-label">在线医生</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ todayConsultations }}</span>
          <span class="stat-label">今日咨询</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ averageRating }}</span>
          <span class="stat-label">平均评分</span>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧：搜索和筛选区域 -->
      <div class="left-panel">
        <!-- 疾病特征搜索 -->
        <div class="search-section">
          <h3 class="section-title">
            <span class="section-icon">🔍</span>
            疾病特征搜索
          </h3>

          <div class="search-form">
            <div class="form-group">
              <label>症状描述</label>
              <el-input
                v-model="searchForm.symptoms"
                type="textarea"
                :rows="3"
                placeholder="请详细描述您的症状，如：头痛、发热、咳嗽等"
                @input="handleSymptomChange"
              />
            </div>

            <div class="form-group">
              <label>科室选择</label>
              <el-select
                v-model="searchForm.department"
                placeholder="请选择科室"
                clearable
                @change="handleDepartmentChange"
              >
                <el-option
                  v-for="dept in departments"
                  :key="dept"
                  :label="dept"
                  :value="dept"
                />
              </el-select>
            </div>

            <div class="form-group">
              <label>医院等级</label>
              <el-select
                v-model="searchForm.hospitalLevel"
                placeholder="请选择医院等级"
                clearable
                @change="handleSearch"
              >
                <el-option label="三甲医院" value="三甲" />
                <el-option label="三乙医院" value="三乙" />
                <el-option label="二甲医院" value="二甲" />
                <el-option label="专科医院" value="专科" />
              </el-select>
            </div>

            <div class="form-group">
              <label>医生职称</label>
              <el-select
                v-model="searchForm.position"
                placeholder="请选择医生职称"
                clearable
                @change="handleSearch"
              >
                <el-option label="主任医师" value="主任医师" />
                <el-option label="副主任医师" value="副主任医师" />
                <el-option label="主治医师" value="主治医师" />
                <el-option label="住院医师" value="住院医师" />
              </el-select>
            </div>

            <div class="search-actions">
              <el-button type="primary" @click="handleSearch" :loading="isSearching">
                <span class="btn-icon">🔍</span>
                智能搜索
              </el-button>
              <el-button @click="resetSearch">
                <span class="btn-icon">🔄</span>
                重置
              </el-button>
            </div>
          </div>
        </div>

        <!-- 快速症状选择 -->
        <div class="quick-symptoms">
          <h4>常见症状快选</h4>
          <div class="symptom-tags">
            <el-tag
              v-for="symptom in commonSymptoms"
              :key="symptom"
              :type="selectedSymptoms.includes(symptom) ? 'primary' : ''"
              @click="toggleSymptom(symptom)"
              class="symptom-tag"
            >
              {{ symptom }}
            </el-tag>
          </div>
        </div>

        <!-- AI智能推荐 -->
        <div class="ai-recommendation" v-if="aiRecommendation">
          <h4>
            <span class="ai-icon">🤖</span>
            AI智能推荐
          </h4>
          <div class="recommendation-content">
            <p>{{ aiRecommendation }}</p>
          </div>
        </div>
      </div>

      <!-- 右侧：医生列表 -->
      <div class="right-panel">
        <!-- 搜索结果头部 -->
        <div class="results-header">
          <div class="results-info">
            <h3>搜索结果</h3>
            <span class="results-count">找到 {{ filteredDoctors.length }} 位医生</span>
          </div>

          <div class="sort-options">
            <el-select v-model="sortBy" @change="handleSort" placeholder="排序方式">
              <el-option label="评分从高到低" value="rating-desc" />
              <el-option label="患者数从多到少" value="patients-desc" />
              <el-option label="挂号费从低到高" value="fee-asc" />
              <el-option label="挂号费从高到低" value="fee-desc" />
            </el-select>
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
                <span class="avatar-text">{{ doctor.name.charAt(0) }}</span>
              </div>
              <div class="doctor-basic-info">
                <h4 class="doctor-name">{{ doctor.name }}</h4>
                <p class="doctor-position">{{ doctor.position }}</p>
                <div class="doctor-rating">
                  <el-rate
                    v-model="doctor.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                </div>
              </div>
              <div class="doctor-status">
                <el-tag :type="getStatusType(doctor)" size="small">
                  {{ getStatusText(doctor) }}
                </el-tag>
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
                  <span class="price-label">挂号费：</span>
                  <span class="price-value">{{ doctor.registrationFee || '暂无' }}</span>
                </div>
                <div class="price-item">
                  <span class="price-label">门诊费：</span>
                  <span class="price-value">{{ doctor.consultationFee || '暂无' }}</span>
                </div>
              </div>

              <div class="action-buttons">
                <el-button size="small" @click.stop="viewDoctorProfile(doctor)">
                  查看详情
                </el-button>
                <el-button type="primary" size="small" @click.stop="startConsultation(doctor)">
                  立即咨询
                </el-button>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!isSearching && filteredDoctors.length === 0" class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>未找到匹配的医生</h3>
            <p>请尝试调整搜索条件或症状描述</p>
            <el-button @click="resetSearch">重新搜索</el-button>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="filteredDoctors.length > pageSize">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="filteredDoctors.length"
            layout="prev, pager, next, jumper"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>

    <!-- 医生详情弹窗 -->
    <el-dialog
      v-model="showDoctorDetail"
      title="医生详情"
      width="600px"
      :before-close="closeDoctorDetail"
    >
      <div v-if="selectedDoctor" class="doctor-detail-content">
        <div class="detail-header">
          <div class="doctor-avatar-large">
            <span class="avatar-text">{{ selectedDoctor.name.charAt(0) }}</span>
          </div>
          <div class="doctor-info">
            <h2>{{ selectedDoctor.name }}</h2>
            <p class="position">{{ selectedDoctor.position }}</p>
            <p class="hospital">{{ selectedDoctor.hospital }} - {{ selectedDoctor.department }}</p>
            <div class="rating-large">
              <el-rate
                v-model="selectedDoctor.rating"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value}分"
              />
              <span class="patient-count">（{{ selectedDoctor.patientCount }}位患者评价）</span>
            </div>
          </div>
        </div>

        <div class="detail-body">
          <div class="detail-section">
            <h4>专业擅长</h4>
            <p class="specialty-detail">{{ selectedDoctor.specialty }}</p>
          </div>

          <div class="detail-section">
            <h4>收费标准</h4>
            <div class="fee-info">
              <div class="fee-item">
                <span class="fee-label">挂号费：</span>
                <span class="fee-amount">{{ selectedDoctor.registrationFee || '暂无' }}</span>
              </div>
              <div class="fee-item">
                <span class="fee-label">门诊费：</span>
                <span class="fee-amount">{{ selectedDoctor.consultationFee || '暂无' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeDoctorDetail">关闭</el-button>
          <el-button type="primary" @click="startConsultation(selectedDoctor)">
            立即咨询
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 智能交互组件 -->
    <GestureControl
      @gestureDetected="handleGestureDetected"
      @navigationGesture="handleNavigationGesture"
    />
    <VoiceInteraction
      @voiceCommand="handleVoiceCommand"
      @voiceResponse="handleVoiceResponse"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage, ElNotification, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'
import GestureControl from '@/components/GestureControl.vue'
import VoiceInteraction from '@/components/VoiceInteraction.vue'

const router = useRouter()

// 响应式数据
const searchForm = reactive({
  symptoms: '',
  department: '',
  hospitalLevel: '',
  position: ''
})

const allDoctors = ref([])
const filteredDoctors = ref([])
const selectedSymptoms = ref([])
const isSearching = ref(false)
const currentPage = ref(1)
const pageSize = ref(6)
const sortBy = ref('rating-desc')
const selectedDoctor = ref(null)
const showDoctorDetail = ref(false)
const aiRecommendation = ref('')

// 统计数据
const totalDoctors = ref(0)
const todayConsultations = ref(1247)
const averageRating = ref(4.8)

// 科室列表
const departments = ref([
  '内科', '外科', '妇科', '儿科', '眼科', '耳鼻喉科',
  '皮肤科', '神经科', '心内科', '呼吸科', '消化科',
  '泌尿科', '骨科', '肿瘤科', '精神科', '急诊科'
])

// 常见症状
const commonSymptoms = ref([
  '头痛', '发热', '咳嗽', '腹痛', '胸痛', '呼吸困难',
  '恶心呕吐', '腹泻', '失眠', '头晕', '皮疹', '关节痛'
])

// 计算属性
const paginatedDoctors = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDoctors.value.slice(start, end)
})

// 生命周期
onMounted(async () => {
  await fetchDoctors()
  initializeData()
})

// 获取医生数据
const fetchDoctors = async () => {
  try {
    isSearching.value = true
    const response = await axios.post('http://127.0.0.1:8000/api/doctors', {
      search: ''
    })

    if (response.data && Array.isArray(response.data)) {
      allDoctors.value = response.data.map(doctor => ({
        ...doctor,
        rating: doctor.rating || 0,
        patientCount: doctor.patientCount || 0,
        registrationFee: doctor.registrationFee || '暂无',
        consultationFee: doctor.consultationFee || '暂无',
        specialty: doctor.specialty || '暂无专业描述',
        isOnline: Math.random() > 0.3 // 模拟在线状态
      }))

      filteredDoctors.value = [...allDoctors.value]
      totalDoctors.value = allDoctors.value.length
    }
  } catch (error) {
    console.error('获取医生数据失败:', error)
    ElMessage.error('获取医生数据失败，请稍后重试')
  } finally {
    isSearching.value = false
  }
}

// 初始化数据
const initializeData = () => {
  // 计算平均评分
  if (allDoctors.value.length > 0) {
    const totalRating = allDoctors.value.reduce((sum, doctor) => sum + (doctor.rating || 0), 0)
    averageRating.value = Number((totalRating / allDoctors.value.length).toFixed(1))
  }
}

// 症状变化处理
const handleSymptomChange = async () => {
  if (searchForm.symptoms.length > 5) {
    await getAIRecommendation()
  }
  await handleSearch()
}

// 科室变化处理
const handleDepartmentChange = async () => {
  await handleSearch()
}

// 智能搜索
const handleSearch = async () => {
  try {
    isSearching.value = true

    let filtered = [...allDoctors.value]

    // 按症状筛选
    if (searchForm.symptoms) {
      const symptoms = searchForm.symptoms.toLowerCase()
      filtered = filtered.filter(doctor =>
        doctor.specialty.toLowerCase().includes(symptoms) ||
        doctor.department.toLowerCase().includes(symptoms)
      )
    }

    // 按科室筛选
    if (searchForm.department) {
      filtered = filtered.filter(doctor =>
        doctor.department.includes(searchForm.department)
      )
    }

    // 按医院等级筛选
    if (searchForm.hospitalLevel) {
      filtered = filtered.filter(doctor =>
        doctor.hospital.includes(searchForm.hospitalLevel)
      )
    }

    // 按职称筛选
    if (searchForm.position) {
      filtered = filtered.filter(doctor =>
        doctor.position.includes(searchForm.position)
      )
    }

    // 按选中症状筛选
    if (selectedSymptoms.value.length > 0) {
      filtered = filtered.filter(doctor =>
        selectedSymptoms.value.some(symptom =>
          doctor.specialty.includes(symptom)
        )
      )
    }

    filteredDoctors.value = filtered
    currentPage.value = 1

    // 如果有搜索结果，获取AI推荐
    if (filtered.length > 0 && searchForm.symptoms) {
      await getAIRecommendation()
    }

  } catch (error) {
    console.error('搜索失败:', error)
    ElMessage.error('搜索失败，请稍后重试')
  } finally {
    isSearching.value = false
  }
}

// 获取AI推荐
const getAIRecommendation = async () => {
  if (!searchForm.symptoms) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/chat', {
      message: `根据症状"${searchForm.symptoms}"，请推荐合适的科室和注意事项`,
      name: '',
      location: '',
      problem: searchForm.symptoms
    })

    if (response.data && response.data.response) {
      // 提取简短的推荐信息
      const recommendation = response.data.response.substring(0, 200) + '...'
      aiRecommendation.value = recommendation
    }
  } catch (error) {
    console.error('获取AI推荐失败:', error)
  }
}

// 重置搜索
const resetSearch = () => {
  searchForm.symptoms = ''
  searchForm.department = ''
  searchForm.hospitalLevel = ''
  searchForm.position = ''
  selectedSymptoms.value = []
  aiRecommendation.value = ''
  filteredDoctors.value = [...allDoctors.value]
  currentPage.value = 1
}

// 切换症状标签
const toggleSymptom = (symptom: string) => {
  const index = selectedSymptoms.value.indexOf(symptom)
  if (index > -1) {
    selectedSymptoms.value.splice(index, 1)
  } else {
    selectedSymptoms.value.push(symptom)
  }
  handleSearch()
}

// 排序处理
const handleSort = () => {
  const sorted = [...filteredDoctors.value]

  switch (sortBy.value) {
    case 'rating-desc':
      sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0))
      break
    case 'patients-desc':
      sorted.sort((a, b) => (b.patientCount || 0) - (a.patientCount || 0))
      break
    case 'fee-asc':
      sorted.sort((a, b) => {
        const aFee = parseFloat(a.registrationFee?.replace(/[^\d.]/g, '') || '0')
        const bFee = parseFloat(b.registrationFee?.replace(/[^\d.]/g, '') || '0')
        return aFee - bFee
      })
      break
    case 'fee-desc':
      sorted.sort((a, b) => {
        const aFee = parseFloat(a.registrationFee?.replace(/[^\d.]/g, '') || '0')
        const bFee = parseFloat(b.registrationFee?.replace(/[^\d.]/g, '') || '0')
        return bFee - aFee
      })
      break
  }

  filteredDoctors.value = sorted
}

// 分页处理
const handlePageChange = (page: number) => {
  currentPage.value = page
}

// 选择医生
const selectDoctor = (doctor: any) => {
  selectedDoctor.value = doctor
  showDoctorDetail.value = true
}

// 查看医生详情
const viewDoctorProfile = (doctor: any) => {
  selectedDoctor.value = doctor
  showDoctorDetail.value = true
}

// 关闭医生详情
const closeDoctorDetail = () => {
  showDoctorDetail.value = false
  selectedDoctor.value = null
}

// 开始咨询
const startConsultation = async (doctor: any) => {
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
      // 跳转到智能问诊页面，并传递医生信息
      router.push({
        path: '/intelligent-consultation',
        query: {
          doctorName: doctor.name,
          department: doctor.department,
          hospital: doctor.hospital
        }
      })

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

// 获取医生状态类型
const getStatusType = (doctor: any) => {
  return doctor.isOnline ? 'success' : 'info'
}

// 获取医生状态文本
const getStatusText = (doctor: any) => {
  return doctor.isOnline ? '在线' : '离线'
}

// 手势控制处理
const handleGestureDetected = (gesture: any) => {
  switch (gesture.type) {
    case 'swipe_up':
      // 向上滑动，滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
      break
    case 'swipe_down':
      // 向下滑动，滚动到底部
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
      break
    case 'swipe_left':
      // 向左滑动，下一页
      if (currentPage.value < Math.ceil(filteredDoctors.value.length / pageSize.value)) {
        handlePageChange(currentPage.value + 1)
      }
      break
    case 'swipe_right':
      // 向右滑动，上一页
      if (currentPage.value > 1) {
        handlePageChange(currentPage.value - 1)
      }
      break
  }
}

// 导航手势处理
const handleNavigationGesture = (direction: string) => {
  switch (direction) {
    case 'up':
      window.scrollTo({ top: 0, behavior: 'smooth' })
      break
    case 'down':
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
      break
  }
}

// 语音命令处理
const handleVoiceCommand = (command: any) => {
  switch (command.action) {
    case 'search_doctors':
      if (command.text) {
        searchForm.symptoms = command.text
        handleSearch()
      }
      break
    case 'reset_search':
      resetSearch()
      break
    case 'next_page':
      if (currentPage.value < Math.ceil(filteredDoctors.value.length / pageSize.value)) {
        handlePageChange(currentPage.value + 1)
      }
      break
    case 'prev_page':
      if (currentPage.value > 1) {
        handlePageChange(currentPage.value - 1)
      }
      break
  }
}

// 语音响应处理
const handleVoiceResponse = (response: string) => {
  ElNotification({
    title: '语音助手',
    message: response,
    type: 'info',
    duration: 3000
  })
}
</script>

<style scoped>
.online-consultation {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #ffffff;
}

/* 页面头部样式 */
.page-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 15px 0;
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-icon {
  font-size: 2.8rem;
  margin-right: 15px;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #b0b0b0;
  margin: 0;
}

/* 统计信息栏 */
.stats-bar {
  display: flex;
  justify-content: center;
  gap: 60px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #b0b0b0;
}

/* 主要内容区域 */
.main-content {
  display: flex;
  gap: 30px;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 左侧面板 */
.left-panel {
  flex: 0 0 350px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: fit-content;
}

.search-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-icon {
  font-size: 1.5rem;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.95rem;
}

.search-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-icon {
  margin-right: 8px;
}

/* 快速症状选择 */
.quick-symptoms {
  margin-bottom: 30px;
}

.quick-symptoms h4 {
  color: #ffffff;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.symptom-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.symptom-tag {
  cursor: pointer;
  transition: all 0.3s ease;
}

.symptom-tag:hover {
  transform: scale(1.05);
}

/* AI推荐区域 */
.ai-recommendation {
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 15px;
  padding: 20px;
}

.ai-recommendation h4 {
  color: #00d4ff;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ai-icon {
  font-size: 1.3rem;
}

.recommendation-content p {
  color: #e0e0e0;
  line-height: 1.6;
  margin: 0;
}

/* 右侧面板 */
.right-panel {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 搜索结果头部 */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.results-info h3 {
  color: #ffffff;
  margin: 0 0 5px 0;
  font-size: 1.4rem;
}

.results-count {
  color: #b0b0b0;
  font-size: 0.9rem;
}

/* 医生卡片列表 */
.doctors-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.doctor-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.doctor-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.doctor-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.doctor-avatar {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
}

.doctor-basic-info {
  flex: 1;
}

.doctor-name {
  color: #ffffff;
  margin: 0 0 5px 0;
  font-size: 1.2rem;
  font-weight: bold;
}

.doctor-position {
  color: #b0b0b0;
  margin: 0 0 10px 0;
  font-size: 0.9rem;
}

.doctor-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.doctor-status {
  align-self: flex-start;
}

.doctor-details {
  margin-bottom: 15px;
}

.detail-row {
  display: flex;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.detail-label {
  color: #b0b0b0;
  min-width: 60px;
}

.detail-value {
  color: #ffffff;
  flex: 1;
}

.specialty-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.doctor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.price-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.price-item {
  font-size: 0.85rem;
}

.price-label {
  color: #b0b0b0;
}

.price-value {
  color: #00d4ff;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #b0b0b0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #ffffff;
  margin-bottom: 10px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

/* 医生详情弹窗 */
.doctor-detail-content {
  color: #333;
}

.detail-header {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.doctor-avatar-large {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
}

.doctor-info h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.doctor-info .position {
  color: #666;
  margin: 0 0 5px 0;
}

.doctor-info .hospital {
  color: #666;
  margin: 0 0 15px 0;
}

.rating-large {
  display: flex;
  align-items: center;
  gap: 10px;
}

.patient-count {
  color: #999;
  font-size: 0.9rem;
}

.detail-section {
  margin-bottom: 25px;
}

.detail-section h4 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.specialty-detail {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.fee-info {
  display: flex;
  gap: 30px;
}

.fee-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.fee-label {
  color: #666;
}

.fee-amount {
  color: #00d4ff;
  font-weight: bold;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    flex-direction: column;
  }

  .left-panel {
    flex: none;
  }

  .doctors-list {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }
}

@media (max-width: 768px) {
  .stats-bar {
    flex-direction: column;
    gap: 20px;
  }

  .doctors-list {
    grid-template-columns: 1fr;
  }

  .doctor-footer {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}
</style>








