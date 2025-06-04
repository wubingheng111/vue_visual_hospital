<template>
  <div class="hospital-navigation">
    <!-- 页面背景 -->
    <div class="page-background"></div>

    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="navigation-avatar">
          <div class="avatar-circle">
            <span class="avatar-icon">🏥</span>
          </div>
          <div class="avatar-status online"></div>
        </div>
        <div class="header-text">
          <h1 class="page-title">
            <span class="title-icon">🗺️</span>
            医院导航与预约系统
          </h1>
          <p class="page-subtitle">智能推荐医院，便捷预约挂号，精准导航服务</p>
        </div>
        <div class="location-status">
          <div class="status-indicator active">
            <span class="status-dot"></span>
            定位服务已开启
          </div>
        </div>
      </div>

      <!-- 快速统计 -->
      <div class="stats-bar">
        <div class="stat-card">
          <div class="stat-icon">🏥</div>
          <div class="stat-info">
            <div class="stat-label">合作医院</div>
            <div class="stat-value">{{ totalHospitals }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">👨‍⚕️</div>
          <div class="stat-info">
            <div class="stat-label">在线医生</div>
            <div class="stat-value">{{ onlineDoctors }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📅</div>
          <div class="stat-info">
            <div class="stat-label">今日预约</div>
            <div class="stat-value">{{ todayAppointments }}</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <div class="stat-label">平均评分</div>
            <div class="stat-value">{{ averageRating }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧：搜索和筛选 -->
      <div class="left-panel">
        <!-- 智能推荐 -->
        <div class="recommendation-section">
          <div class="card-header">
            <h3>
              <span class="card-icon">🤖</span>
              AI智能推荐
            </h3>
            <div class="recommendation-status">
              <span class="status-badge active">
                ✨ 基于症状推荐
              </span>
            </div>
          </div>
          <div class="card-content">
            <div class="symptom-input">
              <label class="form-label">
                <span class="label-icon">🩺</span>
                您的症状描述
              </label>
              <textarea
                v-model="symptomDescription"
                class="form-textarea"
                placeholder="请描述您的症状，AI将为您推荐最适合的医院和科室"
                rows="3"
                @input="handleSymptomAnalysis"
              ></textarea>
            </div>

            <div v-if="aiRecommendation" class="ai-recommendation">
              <div class="recommendation-header">
                <span class="recommendation-icon">💡</span>
                <span class="recommendation-title">AI推荐结果</span>
                <div v-if="aiRecommendation.urgency" class="urgency-badge" :class="aiRecommendation.urgency">
                  {{ getUrgencyText(aiRecommendation.urgency) }}
                </div>
              </div>

              <div v-if="aiRecommendation.isAnalyzing" class="analyzing-state">
                <div class="loading-spinner"></div>
                <span>{{ aiRecommendation.reason }}</span>
              </div>

              <div v-else class="recommendation-content">
                <div class="recommended-department">
                  <strong>🏥 推荐科室：</strong>{{ aiRecommendation.department }}
                </div>
                <div class="recommendation-reason">
                  <strong>📋 推荐理由：</strong>{{ aiRecommendation.reason }}
                </div>

                <!-- 可能病因 -->
                <div v-if="aiRecommendation.possibleCauses" class="possible-causes">
                  <strong>🔍 可能病因：</strong>
                  <div class="causes-list">
                    <span v-for="cause in aiRecommendation.possibleCauses" :key="cause" class="cause-tag">
                      {{ cause }}
                    </span>
                  </div>
                </div>

                <!-- 建议检查 -->
                <div v-if="aiRecommendation.recommendedTests" class="recommended-tests">
                  <strong>🧪 建议检查：</strong>
                  <div class="tests-list">
                    <span v-for="test in aiRecommendation.recommendedTests" :key="test" class="test-tag">
                      {{ test }}
                    </span>
                  </div>
                </div>

                <!-- 生活建议 -->
                <div v-if="aiRecommendation.suggestions" class="life-suggestions">
                  <strong>💡 生活建议：</strong>
                  <ul class="suggestions-list">
                    <li v-for="suggestion in aiRecommendation.suggestions" :key="suggestion">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>

                <!-- 推荐医院 -->
                <div v-if="aiRecommendation.recommendedHospitals && aiRecommendation.recommendedHospitals.length > 0" class="recommended-hospitals">
                  <strong>🏥 推荐医院：</strong>
                  <div class="hospitals-list">
                    <div v-for="hospital in aiRecommendation.recommendedHospitals" :key="hospital.id" class="recommended-hospital-item">
                      <div class="hospital-info">
                        <div class="hospital-name">{{ hospital.name }}</div>
                        <div class="hospital-details">
                          <span class="hospital-level">{{ hospital.level }}</span>
                          <span class="hospital-distance">{{ hospital.distance }}km</span>
                          <span class="hospital-rating">⭐{{ hospital.rating }}</span>
                        </div>
                      </div>
                      <button @click="selectRecommendedHospital(hospital)" class="select-hospital-btn">
                        选择
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="!aiRecommendation.isAnalyzing" class="recommendation-actions">
                <button @click="applyRecommendation" class="apply-btn">
                  <span class="btn-icon">✅</span>
                  采用推荐
                </button>
                <button @click="getDetailedAnalysis" class="detailed-btn">
                  <span class="btn-icon">📊</span>
                  详细分析
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 搜索筛选 -->
        <div class="search-section">
          <div class="card-header">
            <h3>
              <span class="card-icon">🔍</span>
              医院搜索
            </h3>
          </div>
          <div class="card-content">
            <div class="search-form">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🏥</span>
                  医院名称
                </label>
                <input
                  v-model="searchForm.hospitalName"
                  type="text"
                  class="form-input"
                  placeholder="输入医院名称"
                  @input="handleSearch"
                />
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">🏢</span>
                    医院等级
                  </label>
                  <select v-model="searchForm.hospitalLevel" class="form-select" @change="handleSearch">
                    <option value="">全部等级</option>
                    <option value="三级甲等">三甲医院</option>
                    <option value="三级乙等">三乙医院</option>
                    <option value="二级甲等">二甲医院</option>
                    <option value="二级乙等">二乙医院</option>
                    <option value="一级甲等">一甲医院</option>
                    <option value="专科医院">专科医院</option>
                    <option value="民营医院">民营医院</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">🏥</span>
                    科室类型
                  </label>
                  <select v-model="searchForm.department" class="form-select" @change="handleSearch">
                    <option value="">全部科室</option>

                    <!-- 内科系统 -->
                    <optgroup label="🫀 内科系统">
                      <option value="内科">内科</option>
                      <option value="心内科">心内科</option>
                      <option value="呼吸内科">呼吸内科</option>
                      <option value="消化内科">消化内科</option>
                      <option value="神经内科">神经内科</option>
                      <option value="内分泌科">内分泌科</option>
                      <option value="肾内科">肾内科</option>
                      <option value="血液内科">血液内科</option>
                      <option value="风湿免疫科">风湿免疫科</option>
                      <option value="感染科">感染科</option>
                      <option value="老年医学科">老年医学科</option>
                    </optgroup>

                    <!-- 外科系统 -->
                    <optgroup label="🔪 外科系统">
                      <option value="外科">外科</option>
                      <option value="普外科">普外科</option>
                      <option value="骨科">骨科</option>
                      <option value="神经外科">神经外科</option>
                      <option value="心胸外科">心胸外科</option>
                      <option value="泌尿外科">泌尿外科</option>
                      <option value="肝胆外科">肝胆外科</option>
                      <option value="血管外科">血管外科</option>
                      <option value="胃肠外科">胃肠外科</option>
                      <option value="乳腺外科">乳腺外科</option>
                      <option value="甲状腺外科">甲状腺外科</option>
                      <option value="整形外科">整形外科</option>
                      <option value="烧伤科">烧伤科</option>
                    </optgroup>

                    <!-- 妇儿科系统 -->
                    <optgroup label="👶 妇儿科系统">
                      <option value="妇产科">妇产科</option>
                      <option value="妇科">妇科</option>
                      <option value="产科">产科</option>
                      <option value="儿科">儿科</option>
                      <option value="新生儿科">新生儿科</option>
                      <option value="小儿外科">小儿外科</option>
                      <option value="小儿内科">小儿内科</option>
                      <option value="儿童保健科">儿童保健科</option>
                    </optgroup>

                    <!-- 专科系统 -->
                    <optgroup label="👁️ 五官专科">
                      <option value="眼科">眼科</option>
                      <option value="耳鼻喉科">耳鼻喉科</option>
                      <option value="口腔科">口腔科</option>
                      <option value="口腔颌面外科">口腔颌面外科</option>
                      <option value="口腔内科">口腔内科</option>
                      <option value="正畸科">正畸科</option>
                    </optgroup>

                    <!-- 皮肤性病科 -->
                    <optgroup label="🧴 皮肤性病科">
                      <option value="皮肤科">皮肤科</option>
                      <option value="性病科">性病科</option>
                      <option value="医疗美容科">医疗美容科</option>
                    </optgroup>

                    <!-- 肿瘤科系统 -->
                    <optgroup label="🎗️ 肿瘤科系统">
                      <option value="肿瘤科">肿瘤科</option>
                      <option value="肿瘤内科">肿瘤内科</option>
                      <option value="肿瘤外科">肿瘤外科</option>
                      <option value="放疗科">放疗科</option>
                      <option value="介入科">介入科</option>
                    </optgroup>

                    <!-- 精神心理科 -->
                    <optgroup label="🧠 精神心理科">
                      <option value="精神科">精神科</option>
                      <option value="心理科">心理科</option>
                      <option value="心理咨询科">心理咨询科</option>
                      <option value="睡眠医学科">睡眠医学科</option>
                    </optgroup>

                    <!-- 急诊重症 -->
                    <optgroup label="🚨 急诊重症">
                      <option value="急诊科">急诊科</option>
                      <option value="重症医学科">重症医学科</option>
                      <option value="急诊外科">急诊外科</option>
                      <option value="急诊内科">急诊内科</option>
                    </optgroup>

                    <!-- 康复理疗 -->
                    <optgroup label="🏃 康复理疗">
                      <option value="康复科">康复科</option>
                      <option value="理疗科">理疗科</option>
                      <option value="针灸科">针灸科</option>
                      <option value="推拿科">推拿科</option>
                      <option value="运动医学科">运动医学科</option>
                    </optgroup>

                    <!-- 中医科系统 -->
                    <optgroup label="🌿 中医科系统">
                      <option value="中医科">中医科</option>
                      <option value="中医内科">中医内科</option>
                      <option value="中医外科">中医外科</option>
                      <option value="中医妇科">中医妇科</option>
                      <option value="中医儿科">中医儿科</option>
                      <option value="中医骨伤科">中医骨伤科</option>
                      <option value="中医肛肠科">中医肛肠科</option>
                    </optgroup>

                    <!-- 医技科室 -->
                    <optgroup label="🔬 医技科室">
                      <option value="麻醉科">麻醉科</option>
                      <option value="病理科">病理科</option>
                      <option value="检验科">检验科</option>
                      <option value="放射科">放射科</option>
                      <option value="超声科">超声科</option>
                      <option value="核医学科">核医学科</option>
                      <option value="输血科">输血科</option>
                    </optgroup>

                    <!-- 其他专科 -->
                    <optgroup label="🏥 其他专科">
                      <option value="疼痛科">疼痛科</option>
                      <option value="营养科">营养科</option>
                      <option value="全科医学科">全科医学科</option>
                      <option value="预防保健科">预防保健科</option>
                      <option value="体检科">体检科</option>
                      <option value="职业病科">职业病科</option>
                      <option value="变态反应科">变态反应科</option>
                    </optgroup>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">📍</span>
                    距离范围
                  </label>
                  <select v-model="searchForm.distance" class="form-select" @change="handleSearch">
                    <option value="">不限距离</option>
                    <option value="1">1公里内</option>
                    <option value="3">3公里内</option>
                    <option value="5">5公里内</option>
                    <option value="10">10公里内</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span class="label-icon">📊</span>
                    排序方式
                  </label>
                  <select v-model="searchForm.sortBy" class="form-select" @change="handleSearch">
                    <option value="distance">距离优先</option>
                    <option value="rating">评分优先</option>
                    <option value="price">价格优先</option>
                    <option value="availability">可预约优先</option>
                  </select>
                </div>
              </div>

              <div class="search-actions">
                <button @click="getCurrentLocation" class="location-btn">
                  <span class="btn-icon">📍</span>
                  获取当前位置
                </button>
                <button @click="resetSearch" class="reset-btn">
                  <span class="btn-icon">🔄</span>
                  重置筛选
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：医院列表和地图 -->
      <div class="right-panel">
        <!-- 地图和列表切换 -->
        <div class="view-toggle">
          <button
            @click="currentView = 'list'"
            class="toggle-btn"
            :class="{ active: currentView === 'list' }"
          >
            <span class="btn-icon">📋</span>
            医院列表
          </button>
          <button
            @click="switchToMapView"
            class="toggle-btn"
            :class="{ active: currentView === 'map' }"
          >
            <span class="btn-icon">🗺️</span>
            地图模式
          </button>
        </div>

        <!-- 医院列表视图 -->
        <div v-if="currentView === 'list'" class="hospital-list-view">
          <div class="list-header">
            <div class="results-info">
              <h3>
                <span class="results-icon">🏥</span>
                搜索结果
              </h3>
              <span class="results-count">
                找到 <span class="count-number">{{ filteredHospitals.length }}</span> 家医院
              </span>
            </div>
          </div>

          <div class="hospitals-list" v-loading="isSearching">
            <div
              v-for="hospital in paginatedHospitals"
              :key="hospital.id"
              class="hospital-card"
              @click="selectHospital(hospital)"
            >
              <div class="hospital-header">
                <div class="hospital-avatar">
                  <div class="avatar-circle">
                    <span class="avatar-text">{{ hospital.name.charAt(0) }}</span>
                  </div>
                  <div class="hospital-level-badge" :class="hospital.level">
                    {{ hospital.level }}
                  </div>
                </div>
                <div class="hospital-basic-info">
                  <h4 class="hospital-name">{{ hospital.name }}</h4>
                  <p class="hospital-address">{{ hospital.address }}</p>
                  <div class="hospital-rating">
                    <div class="rating-stars">
                      <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= Math.floor(hospital.rating) }">⭐</span>
                    </div>
                    <span class="rating-score">{{ hospital.rating }}</span>
                    <span class="rating-count">({{ hospital.reviewCount }}条评价)</span>
                  </div>
                </div>
                <div class="hospital-distance">
                  <div class="distance-info">
                    <span class="distance-icon">📍</span>
                    <span class="distance-text">{{ hospital.distance }}km</span>
                  </div>
                </div>
              </div>

              <div class="hospital-details">
                <div class="detail-row">
                  <span class="detail-label">特色科室：</span>
                  <span class="detail-value specialty-text">{{ hospital.specialties.join('、') }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">营业时间：</span>
                  <span class="detail-value">{{ hospital.workingHours }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">联系电话：</span>
                  <span class="detail-value">{{ hospital.phone }}</span>
                </div>
              </div>

              <div class="hospital-footer">
                <div class="availability-info">
                  <div class="availability-item">
                    <span class="availability-icon">👨‍⚕️</span>
                    <div class="availability-details">
                      <span class="availability-label">可预约医生</span>
                      <span class="availability-value">{{ hospital.availableDoctors }}位</span>
                    </div>
                  </div>
                  <div class="availability-item">
                    <span class="availability-icon">📅</span>
                    <div class="availability-details">
                      <span class="availability-label">最早可约</span>
                      <span class="availability-value">{{ hospital.earliestAppointment }}</span>
                    </div>
                  </div>
                </div>

                <div class="action-buttons">
                  <button @click.stop="navigateToHospital(hospital)" class="action-btn secondary">
                    <span class="btn-icon">🧭</span>
                    导航
                  </button>
                  <button @click.stop="makeAppointment(hospital)" class="action-btn primary">
                    <span class="btn-icon">📅</span>
                    预约挂号
                  </button>
                </div>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-if="!isSearching && filteredHospitals.length === 0" class="empty-state">
              <div class="empty-content">
                <div class="empty-icon">🏥</div>
                <h3>未找到匹配的医院</h3>
                <p>请尝试调整搜索条件或扩大搜索范围</p>
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
          <div class="pagination-wrapper" v-if="filteredHospitals.length > pageSize">
            <div class="pagination-info">
              <span>共 {{ filteredHospitals.length }} 家医院，每页显示 {{ pageSize }} 家</span>
            </div>
            <div class="pagination-controls">
              <button
                @click="handlePageChange(currentPage - 1)"
                :disabled="currentPage <= 1"
                class="page-btn"
              >
                ← 上一页
              </button>
              <span class="page-info">{{ currentPage }} / {{ Math.ceil(filteredHospitals.length / pageSize) }}</span>
              <button
                @click="handlePageChange(currentPage + 1)"
                :disabled="currentPage >= Math.ceil(filteredHospitals.length / pageSize)"
                class="page-btn"
              >
                下一页 →
              </button>
            </div>
          </div>
        </div>

        <!-- 地图视图 -->
        <div v-else class="map-view">
          <div class="map-container">
            <!-- 增强的地图控制面板 -->
            <div class="map-controls">
              <div class="control-group primary">
                <button @click="refreshMap" class="control-btn" :disabled="!mapInitialized">
                  <span class="btn-icon">🔄</span>
                  <span class="btn-text">刷新地图</span>
                </button>
                <button @click="locateUser" class="control-btn" :class="{ loading: isLocating }">
                  <span class="btn-icon">{{ isLocating ? '⏳' : '📍' }}</span>
                  <span class="btn-text">{{ isLocating ? '定位中...' : '我的位置' }}</span>
                </button>
                <button @click="showAllHospitals" class="control-btn" :disabled="!mapInitialized">
                  <span class="btn-icon">🏥</span>
                  <span class="btn-text">显示全部</span>
                </button>
              </div>

              <div class="control-group secondary">
                <button @click="toggleMapStyle" class="control-btn">
                  <span class="btn-icon">🎨</span>
                  <span class="btn-text">{{ currentMapStyle === 'normal' ? '卫星图' : '标准图' }}</span>
                </button>
                <button @click="toggleTrafficLayer" class="control-btn" :class="{ active: showTraffic }">
                  <span class="btn-icon">🚦</span>
                  <span class="btn-text">实时路况</span>
                </button>
                <button @click="toggleClusterMode" class="control-btn" :class="{ active: clusterMode }">
                  <span class="btn-icon">📍</span>
                  <span class="btn-text">{{ clusterMode ? '取消聚合' : '标记聚合' }}</span>
                </button>
              </div>

              <div class="map-info">
                <div class="info-stats">
                  <span class="info-item">
                    <span class="info-icon">🏥</span>
                    <span class="info-text">{{ filteredHospitals.length }} 家医院</span>
                  </span>
                  <span class="info-item" v-if="mapInitialized">
                    <span class="info-icon">🗺️</span>
                    <span class="info-text">地图已就绪</span>
                  </span>
                  <span class="info-item" v-if="userLocation.address">
                    <span class="info-icon">📍</span>
                    <span class="info-text">{{ userLocation.address }}</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- 地图容器区域 -->
            <div class="map-wrapper">
              <!-- 地图加载状态 -->
              <div v-if="mapLoading" class="map-loading">
                <div class="loading-content">
                  <div class="loading-spinner"></div>
                  <h3>正在加载地图...</h3>
                  <p>{{ mapLoadingMessage }}</p>
                  <div class="loading-progress">
                    <div class="progress-bar" :style="{ width: mapLoadingProgress + '%' }"></div>
                  </div>
                </div>
              </div>

              <!-- 高德地图容器 -->
              <div id="amap-container" class="amap-container" v-show="mapInitialized"></div>

              <!-- 地图工具栏 -->
              <div v-if="mapInitialized" class="map-toolbar">
                <div class="toolbar-group">
                  <button @click="zoomIn" class="toolbar-btn" title="放大">
                    <span class="btn-icon">🔍</span>
                  </button>
                  <button @click="zoomOut" class="toolbar-btn" title="缩小">
                    <span class="btn-icon">🔍</span>
                  </button>
                  <button @click="resetMapView" class="toolbar-btn" title="重置视图">
                    <span class="btn-icon">🎯</span>
                  </button>
                </div>
                <div class="toolbar-group">
                  <button @click="toggleFullscreen" class="toolbar-btn" title="全屏">
                    <span class="btn-icon">{{ isFullscreen ? '🗗' : '🗖' }}</span>
                  </button>
                </div>
              </div>

              <!-- 地图失败时的智能备用界面 -->
              <div v-show="!mapInitialized && !mapLoading" class="map-fallback">
                <div class="fallback-content">
                  <div class="fallback-header">
                    <div class="fallback-icon">🗺️</div>
                    <h3>地图服务暂不可用</h3>
                    <p>正在尝试多种地图服务，为您提供最佳体验</p>
                  </div>

                  <!-- 多地图服务切换 -->
                  <div class="map-service-selector">
                    <h4>🔄 尝试其他地图服务</h4>
                    <div class="service-options">
                      <button @click="tryMapService('amap')" class="service-btn" :class="{ active: currentMapService === 'amap' }">
                        <span class="service-icon">🗺️</span>
                        <span class="service-name">高德地图</span>
                        <span class="service-status">{{ mapServiceStatus.amap }}</span>
                      </button>
                      <button @click="tryMapService('baidu')" class="service-btn" :class="{ active: currentMapService === 'baidu' }">
                        <span class="service-icon">🌐</span>
                        <span class="service-name">百度地图</span>
                        <span class="service-status">{{ mapServiceStatus.baidu }}</span>
                      </button>
                      <button @click="tryMapService('tencent')" class="service-btn" :class="{ active: currentMapService === 'tencent' }">
                        <span class="service-icon">🗺️</span>
                        <span class="service-name">腾讯地图</span>
                        <span class="service-status">{{ mapServiceStatus.tencent }}</span>
                      </button>
                    </div>
                  </div>

                  <!-- 智能医院列表备用显示 -->
                  <div class="smart-hospital-list">
                    <div class="list-header">
                      <h4>📍 智能医院推荐</h4>
                      <div class="list-controls">
                        <button @click="sortHospitalsByDistance" class="sort-btn">
                          <span class="btn-icon">📏</span>
                          按距离排序
                        </button>
                        <button @click="sortHospitalsByRating" class="sort-btn">
                          <span class="btn-icon">⭐</span>
                          按评分排序
                        </button>
                      </div>
                    </div>

                    <div class="smart-hospital-grid">
                      <div
                        v-for="hospital in filteredHospitals.slice(0, 6)"
                        :key="hospital.id"
                        class="smart-hospital-card"
                        @click="selectHospitalFromFallback(hospital)"
                      >
                        <div class="card-header">
                          <div class="hospital-avatar">
                            <span class="avatar-text">{{ hospital.name.charAt(0) }}</span>
                          </div>
                          <div class="hospital-basic">
                            <h5 class="hospital-name">{{ hospital.name }}</h5>
                            <p class="hospital-level">{{ hospital.level }}</p>
                          </div>
                          <div class="hospital-distance">
                            <span class="distance-value">{{ hospital.distance }}km</span>
                          </div>
                        </div>

                        <div class="card-content">
                          <div class="hospital-rating">
                            <span class="rating-stars">⭐⭐⭐⭐⭐</span>
                            <span class="rating-score">{{ hospital.rating }}</span>
                          </div>
                          <div class="hospital-specialties">
                            <span v-for="specialty in hospital.specialties.slice(0, 2)" :key="specialty" class="specialty-tag">
                              {{ specialty }}
                            </span>
                          </div>
                        </div>

                        <div class="card-actions">
                          <button @click.stop="navigateToHospital(hospital.name)" class="action-btn primary">
                            🧭 导航
                          </button>
                          <button @click.stop="makeAppointment(hospital)" class="action-btn secondary">
                            📅 预约
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 路线规划面板 - 暂时完全隐藏 -->
            <!--
            <div v-if="showRoutePanel" class="route-panel">
              <div class="panel-header">
                <h4>路线规划</h4>
                <button @click="closeRoutePanel" class="close-btn">×</button>
              </div>
              <div id="route-panel" class="route-content"></div>
            </div>
            -->
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
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import GestureControl from '@/components/GestureControl.vue'
import VoiceInteraction from '@/components/VoiceInteraction.vue'
import amapService from '@/utils/amapService.js'

// 响应式数据
const totalHospitals = ref(156)
const onlineDoctors = ref(1247)
const todayAppointments = ref(89)
const averageRating = ref(4.8)

// 搜索和筛选
const symptomDescription = ref('')
const searchForm = ref({
  hospitalName: '',
  hospitalLevel: '',
  department: '',
  distance: '',
  sortBy: 'distance'
})

// 视图控制
const currentView = ref('list')
const isSearching = ref(false)
const currentPage = ref(1)
const pageSize = ref(5)

// 地图相关
// const showRoutePanel = ref(false) // 暂时禁用路线面板
const mapInitialized = ref(false)
const currentMarkers = ref([])
const mapLoading = ref(false)
const mapLoadingMessage = ref('正在初始化地图服务...')
const mapLoadingProgress = ref(0)
const isLocating = ref(false)
const currentMapStyle = ref('normal') // 'normal' | 'satellite'
const showTraffic = ref(false)
const clusterMode = ref(false)
const isFullscreen = ref(false)
const currentMapService = ref('amap')
const mapServiceStatus = ref({
  amap: '检测中...',
  baidu: '检测中...',
  tencent: '检测中...'
})

// AI推荐
const aiRecommendation = ref(null)

// 用户位置
const userLocation = ref({
  latitude: 39.9042,
  longitude: 116.4074,
  address: '北京市朝阳区'
})

// 医院数据 - 从数据库获取
const hospitals = ref([])
const allHospitals = ref([]) // 存储所有医院数据用于筛选

// API调用函数
const fetchHospitalsFromDatabase = async () => {
  try {
    isSearching.value = true

    // 构建查询参数，只添加有效的参数
    const params = new URLSearchParams()

    if (searchForm.value.hospitalName && searchForm.value.hospitalName.trim()) {
      params.append('hospitalName', searchForm.value.hospitalName.trim())
    }

    if (searchForm.value.hospitalLevel && searchForm.value.hospitalLevel.trim()) {
      params.append('hospitalLevel', searchForm.value.hospitalLevel.trim())
    }

    if (searchForm.value.department && searchForm.value.department.trim()) {
      params.append('department', searchForm.value.department.trim())
    }

    // 处理地址参数，提取关键城市信息
    if (userLocation.value.address &&
        userLocation.value.address !== '当前位置' &&
        userLocation.value.address.trim()) {

      let locationKeyword = userLocation.value.address.trim()

      // 提取城市关键词，优化搜索匹配
      if (locationKeyword.includes('大连')) {
        locationKeyword = '大连'
      } else if (locationKeyword.includes('北京')) {
        locationKeyword = '北京'
      } else if (locationKeyword.includes('上海')) {
        locationKeyword = '上海'
      } else if (locationKeyword.includes('广州')) {
        locationKeyword = '广州'
      } else if (locationKeyword.includes('深圳')) {
        locationKeyword = '深圳'
      } else if (locationKeyword.includes('辽宁')) {
        locationKeyword = '辽宁'
      } else if (locationKeyword.includes('省') || locationKeyword.includes('市')) {
        // 提取省市名称
        const match = locationKeyword.match(/([\u4e00-\u9fa5]+[省市])/);
        if (match) {
          locationKeyword = match[1].replace(/[省市]$/, '');
        }
      }

      params.append('location', locationKeyword)
      console.log('处理后的位置关键词:', locationKeyword)
    }

    const url = `http://127.0.0.1:8000/api/hospitals${params.toString() ? '?' + params.toString() : ''}`
    console.log('请求URL:', url)

    const response = await fetch(url)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('API响应错误:', response.status, errorText)
      throw new Error(`获取医院数据失败: ${response.status}`)
    }

    const data = await response.json()
    console.log('获取到的医院数据:', data)

    // 检查新的API响应格式
    const hospitalList = data.hospitals || data // 兼容新旧格式
    const totalCount = data.total || hospitalList.length

    // 转换数据库字段到前端格式
    const transformedHospitals = hospitalList.map((hospital, index) => ({
      id: index + 1,
      name: hospital.医院名称 || '未知医院',
      level: hospital.医院等级 || '未知等级',
      address: hospital.医院地址 || '地址未知',
      phone: hospital.联系电话 || '电话未知',
      specialties: hospital.重点科室 ? hospital.重点科室.split('、') : ['综合科室'],
      departments: hospital.重点科室 ? hospital.重点科室.split('、') : ['综合科室'],
      operationType: hospital.经营方式 || '未知',
      // 模拟一些前端需要的字段
      rating: (Math.random() * 1 + 4).toFixed(1), // 4.0-5.0随机评分
      reviewCount: Math.floor(Math.random() * 3000) + 500, // 500-3500随机评价数
      distance: (Math.random() * 10 + 0.5).toFixed(1), // 0.5-10.5km随机距离
      workingHours: '08:00-17:00',
      availableDoctors: Math.floor(Math.random() * 50) + 20, // 20-70随机医生数
      earliestAppointment: ['今天下午', '明天上午', '明天下午', '后天上午'][Math.floor(Math.random() * 4)]
    }))

    allHospitals.value = transformedHospitals
    hospitals.value = transformedHospitals
    totalHospitals.value = totalCount // 更新总医院数

    ElMessage.success(`找到 ${transformedHospitals.length} 家医院，总共 ${totalCount} 家`)

    // 如果当前在地图视图，自动更新地图标记
    await updateMapWhenDataChanges()

  } catch (error) {
    console.error('获取医院数据失败:', error)
    ElMessage.error('获取医院数据失败，请稍后重试')

    // 如果API失败，使用一些示例数据
    const fallbackHospitals = [
      {
        id: 1,
        name: '北京协和医院',
        level: '三甲',
        address: '北京市东城区东单帅府园1号',
        phone: '010-69156114',
        specialties: ['内科', '外科'],
        departments: ['内科', '外科'],
        operationType: '公立',
        rating: '4.8',
        reviewCount: 2847,
        distance: '2.3',
        workingHours: '08:00-17:00',
        availableDoctors: 45,
        earliestAppointment: '明天上午'
      },
      {
        id: 2,
        name: '北京大学第一医院',
        level: '三甲',
        address: '北京市西城区西什库大街8号',
        phone: '010-83572211',
        specialties: ['泌尿外科', '肾内科'],
        departments: ['泌尿外科', '肾内科'],
        operationType: '公立',
        rating: '4.7',
        reviewCount: 1923,
        distance: '3.1',
        workingHours: '08:00-17:00',
        availableDoctors: 38,
        earliestAppointment: '后天下午'
      }
    ]

    allHospitals.value = fallbackHospitals
    hospitals.value = fallbackHospitals
  } finally {
    isSearching.value = false
  }
}

// 计算属性
const filteredHospitals = computed(() => {
  let filtered = hospitals.value

  // 按医院名称筛选
  if (searchForm.value.hospitalName) {
    filtered = filtered.filter(hospital =>
      hospital.name.toLowerCase().includes(searchForm.value.hospitalName.toLowerCase())
    )
  }

  // 按医院等级筛选
  if (searchForm.value.hospitalLevel) {
    filtered = filtered.filter(hospital => hospital.level === searchForm.value.hospitalLevel)
  }

  // 按科室筛选
  if (searchForm.value.department) {
    filtered = filtered.filter(hospital =>
      hospital.departments.some(dept => dept.includes(searchForm.value.department))
    )
  }

  // 按距离筛选
  if (searchForm.value.distance) {
    const maxDistance = parseInt(searchForm.value.distance)
    filtered = filtered.filter(hospital => parseFloat(hospital.distance) <= maxDistance)
  }

  // 排序
  switch (searchForm.value.sortBy) {
    case 'distance':
      filtered.sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance))
      break
    case 'rating':
      filtered.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating))
      break
    case 'availability':
      filtered.sort((a, b) => b.availableDoctors - a.availableDoctors)
      break
  }

  return filtered
})

const paginatedHospitals = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredHospitals.value.slice(start, end)
})

// 症状分析和AI推荐
const handleSymptomAnalysis = async () => {
  if (!symptomDescription.value.trim()) {
    aiRecommendation.value = null
    return
  }

  // 显示分析中状态
  aiRecommendation.value = {
    department: '分析中...',
    reason: 'AI正在分析您的症状，请稍候...',
    isAnalyzing: true
  }

  // 模拟AI分析（实际项目中可以调用真实的AI API）
  setTimeout(() => {
    const symptoms = symptomDescription.value.toLowerCase()
    const recommendation = analyzeSymptoms(symptoms)

    // 基于症状推荐和用户位置，推荐具体医院
    const recommendedHospitals = getRecommendedHospitals(recommendation.department)

    aiRecommendation.value = {
      ...recommendation,
      recommendedHospitals,
      isAnalyzing: false
    }
  }, 2000)
}

// 症状分析逻辑
const analyzeSymptoms = (symptoms) => {
  const symptomDatabase = {
    // 神经系统
    '头痛|头疼|偏头痛|头晕|眩晕|失眠|健忘|抽搐|癫痫|中风|脑梗|面瘫': {
      department: '神经内科',
      reason: '头痛、头晕等症状可能涉及神经系统疾病，建议神经内科专业诊断',
      urgency: '中等',
      suggestions: ['避免熬夜', '保持规律作息', '减少压力'],
      possibleCauses: ['偏头痛', '紧张性头痛', '血管性头痛', '颅内压增高'],
      recommendedTests: ['头颅CT', '脑电图', '血压监测']
    },

    // 心血管系统
    '胸痛|心痛|心慌|心悸|胸闷|气短|心律不齐|高血压|低血压': {
      department: '心内科',
      reason: '胸痛、心悸等症状需要排除心血管疾病，建议心内科专业评估',
      urgency: '较高',
      suggestions: ['避免剧烈运动', '保持情绪稳定', '戒烟限酒'],
      possibleCauses: ['冠心病', '心律不齐', '心肌炎', '心脏神经症'],
      recommendedTests: ['心电图', '心脏彩超', '心肌酶检查']
    },

    // 呼吸系统
    '咳嗽|咳痰|呼吸困难|气喘|哮喘|胸闷|气促|咯血': {
      department: '呼吸内科',
      reason: '呼吸系统症状需要专业的肺功能评估和呼吸道检查',
      urgency: '中等',
      suggestions: ['避免吸烟', '远离过敏原', '保持室内空气流通'],
      possibleCauses: ['支气管炎', '哮喘', '肺炎', '过敏性鼻炎'],
      recommendedTests: ['胸部X光', '肺功能检查', '血常规']
    },

    // 消化系统
    '腹痛|胃痛|恶心|呕吐|腹泻|便秘|消化不良|胃胀|反酸|烧心|便血': {
      department: '消化内科',
      reason: '消化系统症状需要专业的胃肠道检查和诊断',
      urgency: '中等',
      suggestions: ['规律饮食', '避免辛辣食物', '少食多餐'],
      possibleCauses: ['胃炎', '胃溃疡', '肠炎', '消化不良'],
      recommendedTests: ['胃镜检查', '腹部B超', '大便常规']
    },

    // 内分泌系统
    '糖尿病|血糖高|多饮|多尿|消瘦|甲亢|甲减|肥胖': {
      department: '内分泌科',
      reason: '血糖异常、甲状腺疾病等内分泌问题需要专科诊治',
      urgency: '中等',
      suggestions: ['控制饮食', '规律运动', '定期监测'],
      possibleCauses: ['糖尿病', '甲状腺功能异常', '代谢综合征'],
      recommendedTests: ['血糖检查', '甲状腺功能', '糖化血红蛋白']
    },

    // 肾脏泌尿系统
    '尿频|尿急|尿痛|血尿|腰痛|水肿|蛋白尿': {
      department: '肾内科',
      reason: '泌尿系统症状可能涉及肾脏疾病，需要专业评估',
      urgency: '中等',
      suggestions: ['多饮水', '避免憋尿', '注意个人卫生'],
      possibleCauses: ['泌尿系感染', '肾炎', '肾结石'],
      recommendedTests: ['尿常规', '肾功能', '泌尿系B超']
    },

    // 发热感染
    '发热|发烧|感冒|流感|咽痛|嗓子疼|扁桃体炎': {
      department: '内科',
      reason: '发热症状需要全面检查确定感染源和病因',
      urgency: '中等',
      suggestions: ['多休息', '多喝水', '避免受凉'],
      possibleCauses: ['病毒感染', '细菌感染', '上呼吸道感染'],
      recommendedTests: ['血常规', 'C反应蛋白', '咽拭子培养']
    },

    // 骨科
    '腰痛|背痛|关节痛|骨痛|扭伤|骨折|颈椎病|肩周炎|膝关节痛': {
      department: '骨科',
      reason: '骨骼、关节、肌肉疼痛需要骨科专业诊断和治疗',
      urgency: '中等',
      suggestions: ['避免重体力劳动', '适当休息', '热敷缓解'],
      possibleCauses: ['腰椎间盘突出', '关节炎', '肌肉劳损'],
      recommendedTests: ['X光检查', 'MRI', '骨密度检查']
    },

    // 皮肤科
    '皮疹|湿疹|过敏|瘙痒|皮肤病|荨麻疹|痤疮|脱发': {
      department: '皮肤科',
      reason: '皮肤症状需要皮肤科专业诊断，确定过敏原或病因',
      urgency: '较低',
      suggestions: ['避免抓挠', '保持皮肤清洁', '避免过敏原'],
      possibleCauses: ['过敏性皮炎', '湿疹', '荨麻疹'],
      recommendedTests: ['过敏原检测', '皮肤镜检查']
    },

    // 眼科
    '视力下降|眼痛|眼红|眼干|流泪|飞蚊症|闪光|复视': {
      department: '眼科',
      reason: '眼部症状需要眼科专业检查，及时诊治避免视力损害',
      urgency: '中等',
      suggestions: ['避免用眼过度', '定期休息', '保持眼部卫生'],
      possibleCauses: ['近视', '干眼症', '结膜炎', '青光眼'],
      recommendedTests: ['视力检查', '眼压测量', '眼底检查']
    },

    // 耳鼻喉科
    '耳痛|耳鸣|听力下降|鼻塞|流鼻涕|打鼾|声音嘶哑|咽痛': {
      department: '耳鼻喉科',
      reason: '耳鼻喉症状需要专科检查，排除感染或结构异常',
      urgency: '中等',
      suggestions: ['避免噪音', '保持鼻腔清洁', '戒烟限酒'],
      possibleCauses: ['中耳炎', '鼻炎', '咽炎', '听力损失'],
      recommendedTests: ['听力检查', '鼻内镜', '咽喉镜']
    },

    // 妇科
    '月经不调|痛经|白带异常|盆腔痛|乳房胀痛|阴道出血': {
      department: '妇科',
      reason: '妇科症状需要专业检查，维护女性生殖健康',
      urgency: '中等',
      suggestions: ['注意个人卫生', '规律作息', '避免过度劳累'],
      possibleCauses: ['月经失调', '妇科炎症', '内分泌紊乱'],
      recommendedTests: ['妇科检查', 'B超', '激素检查']
    },

    // 精神心理科
    '抑郁|焦虑|失眠|恐惧|强迫|幻觉|妄想|情绪低落': {
      department: '精神科',
      reason: '精神心理症状需要专业评估和治疗，维护心理健康',
      urgency: '中等',
      suggestions: ['保持规律作息', '适当运动', '寻求社会支持'],
      possibleCauses: ['抑郁症', '焦虑症', '失眠症', '强迫症'],
      recommendedTests: ['心理评估', '精神状态检查', '睡眠监测']
    },

    // 肿瘤科
    '肿块|包块|淋巴结肿大|不明原因消瘦|持续疼痛|异常出血': {
      department: '肿瘤科',
      reason: '肿块或异常症状需要排除肿瘤可能，建议及时检查',
      urgency: '较高',
      suggestions: ['定期体检', '健康饮食', '避免致癌因素'],
      possibleCauses: ['良性肿瘤', '恶性肿瘤', '淋巴结炎'],
      recommendedTests: ['CT检查', '病理检查', '肿瘤标志物']
    }
  }

  // 匹配症状
  for (const [pattern, info] of Object.entries(symptomDatabase)) {
    const regex = new RegExp(pattern)
    if (regex.test(symptoms)) {
      return info
    }
  }

  // 默认推荐
  return {
    department: '内科',
    reason: '建议先到内科进行初步诊断，医生会根据具体情况转诊到相应专科',
    urgency: '中等',
    suggestions: ['保持良好作息', '均衡饮食', '适量运动'],
    possibleCauses: ['需要进一步检查确定'],
    recommendedTests: ['基础体检', '血常规', '尿常规']
  }
}

// 基于科室和位置推荐医院
const getRecommendedHospitals = (department) => {
  if (!hospitals.value.length) return []

  // 筛选有该科室的医院
  let suitableHospitals = hospitals.value.filter(hospital => {
    const departments = hospital.departments || hospital.specialties || []
    return departments.some(dept =>
      dept.includes(department.replace('科', '')) ||
      dept.includes(department)
    )
  })

  // 如果没有找到专门的科室，推荐综合医院
  if (suitableHospitals.length === 0) {
    suitableHospitals = hospitals.value.filter(hospital =>
      hospital.level.includes('三级') || hospital.level.includes('二级')
    )
  }

  // 按照综合评分排序（距离 + 等级 + 评分）
  return suitableHospitals
    .map(hospital => ({
      ...hospital,
      score: calculateHospitalScore(hospital)
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 3) // 推荐前3家
}

// 计算医院综合评分
const calculateHospitalScore = (hospital) => {
  let score = 0

  // 距离评分（距离越近分数越高）
  const distance = parseFloat(hospital.distance) || 10
  score += Math.max(0, 10 - distance) * 2

  // 等级评分
  if (hospital.level.includes('三级甲等')) score += 10
  else if (hospital.level.includes('三级')) score += 8
  else if (hospital.level.includes('二级甲等')) score += 6
  else if (hospital.level.includes('二级')) score += 4

  // 评分评分
  const rating = parseFloat(hospital.rating) || 4.0
  score += rating * 2

  // 可用医生数量评分
  const doctors = hospital.availableDoctors || 20
  score += Math.min(doctors / 10, 5)

  return score
}

// 获取紧急程度文本
const getUrgencyText = (urgency) => {
  const urgencyMap = {
    '较高': '🔴 较紧急',
    '中等': '🟡 一般',
    '较低': '🟢 不紧急'
  }
  return urgencyMap[urgency] || '🟡 一般'
}

// 选择推荐的医院
const selectRecommendedHospital = (hospital) => {
  // 自动填充搜索条件
  searchForm.value.hospitalName = hospital.name
  searchForm.value.department = aiRecommendation.value.department

  // 执行搜索
  handleSearch()

  ElMessage.success(`已选择 ${hospital.name}，为您筛选相关信息`)
}

// 获取详细分析
const getDetailedAnalysis = async () => {
  if (!aiRecommendation.value) return

  ElMessage.info('正在获取详细分析...')

  // 模拟调用更详细的AI分析
  setTimeout(() => {
    const detailedInfo = {
      ...aiRecommendation.value,
      detailedAnalysis: {
        riskFactors: ['年龄因素', '生活习惯', '遗传因素'],
        preventionMeasures: ['定期体检', '健康饮食', '适量运动', '充足睡眠'],
        followUpAdvice: '建议1-2周后复查，如症状加重请及时就医',
        emergencySignals: ['症状突然加重', '出现新的症状', '持续高热不退']
      }
    }

    // 这里可以打开一个详细分析的模态框
    ElMessage.success('详细分析已生成，请查看推荐内容')

    // 更新推荐信息
    aiRecommendation.value = detailedInfo
  }, 1500)
}

// 采用AI推荐
const applyRecommendation = () => {
  if (aiRecommendation.value && !aiRecommendation.value.isAnalyzing) {
    searchForm.value.department = aiRecommendation.value.department
    handleSearch()
    ElMessage.success('已采用AI推荐，为您筛选相关医院')
  }
}

// 搜索处理
const handleSearch = async () => {
  currentPage.value = 1
  await fetchHospitalsFromDatabase()
  // 搜索完成后，如果在地图视图，自动更新地图标记
  await updateMapWhenDataChanges()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    hospitalName: '',
    hospitalLevel: '',
    department: '',
    distance: '',
    sortBy: 'distance'
  }
  symptomDescription.value = ''
  aiRecommendation.value = null
  currentPage.value = 1
  ElMessage.info('搜索条件已重置')
}

// 获取当前位置
const getCurrentLocation = async () => {
  try {
    ElMessage.info('正在获取您的位置...')

    // 优先使用高德地图定位服务
    try {
      const position = await amapService.getCurrentPosition()
      userLocation.value = {
        latitude: position.latitude,
        longitude: position.longitude,
        address: position.address
      }
      ElMessage.success(`位置获取成功：${position.address}`)
      handleSearch()
      return
    } catch (amapError) {
      console.warn('高德地图定位失败，尝试浏览器定位:', amapError)
    }

    // 备用：使用浏览器原生定位
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const coords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          }

          // 尝试通过高德地图逆地理编码获取地址
          let address = '当前位置'
          try {
            // @ts-ignore
            if (window.AMap) {
              // @ts-ignore
              const geocoder = new window.AMap.Geocoder()
              const result = await new Promise((resolve, reject) => {
                geocoder.getAddress([coords.longitude, coords.latitude], (status, result) => {
                  if (status === 'complete' && result.regeocode) {
                    resolve(result.regeocode.formattedAddress)
                  } else {
                    reject(new Error('逆地理编码失败'))
                  }
                })
              })
              address = result
            } else {
              // 根据坐标推断城市
              address = getCityByCoordinates(coords.longitude, coords.latitude)
            }
          } catch (error) {
            console.warn('逆地理编码失败，使用坐标推断:', error)
            address = getCityByCoordinates(coords.longitude, coords.latitude)
          }

          userLocation.value = {
            latitude: coords.latitude,
            longitude: coords.longitude,
            address: address
          }
          ElMessage.success(`位置获取成功：${address}`)
          handleSearch()
        },
        () => {
          ElMessage.error('位置获取失败，使用默认位置')
          userLocation.value = {
            latitude: 39.9042,
            longitude: 116.4074,
            address: '北京市'
          }
          handleSearch()
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      )
    } else {
      ElMessage.error('浏览器不支持定位功能，使用默认位置')
      userLocation.value = {
        latitude: 39.9042,
        longitude: 116.4074,
        address: '北京市'
      }
      handleSearch()
    }
  } catch (error) {
    console.error('定位服务异常:', error)
    ElMessage.error('定位服务异常，使用默认位置')
    userLocation.value = {
      latitude: 39.9042,
      longitude: 116.4074,
      address: '北京市'
    }
    handleSearch()
  }
}

// 根据坐标推断城市（备用方案）
const getCityByCoordinates = (lng, lat) => {
  // 大连市坐标范围大致为：经度120.5-122.5，纬度38.5-40.5
  if (lng >= 120.5 && lng <= 122.5 && lat >= 38.5 && lat <= 40.5) {
    return '大连市'
  }
  // 北京市坐标范围大致为：经度115.5-117.5，纬度39.5-41.0
  else if (lng >= 115.5 && lng <= 117.5 && lat >= 39.5 && lat <= 41.0) {
    return '北京市'
  }
  // 上海市坐标范围大致为：经度120.8-122.2，纬度30.7-31.9
  else if (lng >= 120.8 && lng <= 122.2 && lat >= 30.7 && lat <= 31.9) {
    return '上海市'
  }
  // 广州市坐标范围大致为：经度112.9-114.5，纬度22.5-24.0
  else if (lng >= 112.9 && lng <= 114.5 && lat >= 22.5 && lat <= 24.0) {
    return '广州市'
  }
  // 深圳市坐标范围大致为：经度113.7-114.7，纬度22.4-22.9
  else if (lng >= 113.7 && lng <= 114.7 && lat >= 22.4 && lat <= 22.9) {
    return '深圳市'
  }
  else {
    return '当前城市'
  }
}

// 安全的Base64编码函数，支持中文字符
const safeBase64Encode = (str) => {
  try {
    // 使用encodeURIComponent和btoa的组合来处理中文字符
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (_, p1) => {
      return String.fromCharCode(parseInt(p1, 16))
    }))
  } catch (error) {
    console.warn('Base64编码失败，使用备用方案:', error)
    // 备用方案：直接返回完整的data URL
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(str)
  }
}

// 创建医院标记图标
const createHospitalIcon = () => {
  // 使用简化的SVG，避免emoji字符导致的编码问题
  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">
    <circle cx="14" cy="14" r="12" fill="#00ff88" stroke="#fff" stroke-width="2"/>
    <rect x="11" y="8" width="6" height="2" fill="#1a1a2e"/>
    <rect x="13" y="6" width="2" height="6" fill="#1a1a2e"/>
    <rect x="11" y="18" width="6" height="2" fill="#1a1a2e"/>
    <rect x="13" y="16" width="2" height="6" fill="#1a1a2e"/>
  </svg>`

  // 直接使用UTF-8编码，避免Base64编码问题
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent)
}

// 创建用户位置标记图标
const createUserLocationIcon = () => {
  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
    <circle cx="16" cy="16" r="14" fill="#007bff" stroke="#fff" stroke-width="3"/>
    <circle cx="16" cy="16" r="6" fill="#fff"/>
  </svg>`

  // 直接使用UTF-8编码，避免Base64编码问题
  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent)
}

// 增强的地图相关方法
const initializeMap = async () => {
  try {
    console.log('开始初始化地图...')
    mapLoading.value = true
    mapLoadingProgress.value = 0
    mapLoadingMessage.value = '正在检测地图服务...'

    // 检测地图服务可用性
    await checkMapServices()
    mapLoadingProgress.value = 20

    // 等待DOM更新
    await nextTick()
    mapLoadingMessage.value = '正在准备地图容器...'

    // 确保地图容器存在
    const mapContainer = document.getElementById('amap-container')
    if (!mapContainer) {
      throw new Error('地图容器不存在')
    }
    mapLoadingProgress.value = 40

    console.log('地图容器已找到，开始初始化高德地图...')
    mapLoadingMessage.value = '正在加载地图API...'

    // 初始化地图
    await amapService.initMap('amap-container', {
      zoom: 12,
      mapStyle: currentMapStyle.value === 'satellite' ? 'amap://styles/satellite' : 'amap://styles/normal'
    })
    mapLoadingProgress.value = 70

    console.log('地图初始化成功，设置中心点...')
    mapLoadingMessage.value = '正在定位用户位置...'

    // 设置地图中心为用户位置
    if (userLocation.value.longitude && userLocation.value.latitude) {
      amapService.setCenter(userLocation.value.longitude, userLocation.value.latitude)
    }
    mapLoadingProgress.value = 85

    // 标记地图已初始化
    mapInitialized.value = true
    mapLoadingMessage.value = '正在加载医院标记...'

    // 显示医院标记
    await addHospitalMarkersToMap()
    mapLoadingProgress.value = 100

    // 启用交通图层（如果需要）
    if (showTraffic.value) {
      toggleTrafficLayer()
    }

    ElMessage.success('地图初始化成功')
  } catch (error) {
    console.error('地图初始化失败:', error)
    mapInitialized.value = false
    mapServiceStatus.value.amap = '不可用'
    ElMessage.error(`地图加载失败: ${error.message}`)
  } finally {
    mapLoading.value = false
    mapLoadingProgress.value = 0
  }
}

// 检测地图服务可用性
const checkMapServices = async () => {
  const services = ['amap', 'baidu', 'tencent']

  for (const service of services) {
    try {
      mapServiceStatus.value[service] = '检测中...'

      // 模拟检测逻辑（实际项目中可以ping相应的API）
      await new Promise(resolve => setTimeout(resolve, 500))

      if (service === 'amap') {
        // 检测高德地图API
        mapServiceStatus.value[service] = window.AMap ? '可用' : '不可用'
      } else {
        // 其他地图服务暂时标记为可用
        mapServiceStatus.value[service] = '可用'
      }
    } catch (error) {
      mapServiceStatus.value[service] = '不可用'
    }
  }
}

// 切换地图样式
const toggleMapStyle = () => {
  if (!amapService.map) return

  currentMapStyle.value = currentMapStyle.value === 'normal' ? 'satellite' : 'normal'

  const newStyle = currentMapStyle.value === 'satellite' ? 'amap://styles/satellite' : 'amap://styles/normal'
  amapService.map.setMapStyle(newStyle)

  ElMessage.success(`已切换到${currentMapStyle.value === 'satellite' ? '卫星' : '标准'}地图`)
}

// 切换交通图层
const toggleTrafficLayer = () => {
  if (!amapService.map) return

  showTraffic.value = !showTraffic.value

  if (showTraffic.value) {
    // 添加交通图层
    amapService.map.plugin('AMap.TileLayer.Traffic', () => {
      const trafficLayer = new window.AMap.TileLayer.Traffic({
        zIndex: 10
      })
      amapService.map.add(trafficLayer)
      amapService.trafficLayer = trafficLayer
    })
    ElMessage.success('已开启实时路况')
  } else {
    // 移除交通图层
    if (amapService.trafficLayer) {
      amapService.map.remove(amapService.trafficLayer)
      amapService.trafficLayer = null
    }
    ElMessage.success('已关闭实时路况')
  }
}

// 切换标记聚合模式
const toggleClusterMode = () => {
  clusterMode.value = !clusterMode.value

  if (clusterMode.value) {
    // 启用标记聚合
    ElMessage.success('已启用标记聚合模式')
  } else {
    // 禁用标记聚合
    ElMessage.success('已禁用标记聚合模式')
  }

  // 重新添加医院标记
  addHospitalMarkersToMap()
}

// 地图缩放控制
const zoomIn = () => {
  if (amapService.map) {
    amapService.map.zoomIn()
  }
}

const zoomOut = () => {
  if (amapService.map) {
    amapService.map.zoomOut()
  }
}

// 重置地图视图
const resetMapView = () => {
  if (amapService.map && userLocation.value.longitude && userLocation.value.latitude) {
    amapService.map.setZoomAndCenter(12, [userLocation.value.longitude, userLocation.value.latitude])
    ElMessage.success('已重置地图视图')
  }
}

// 全屏切换
const toggleFullscreen = () => {
  const mapContainer = document.getElementById('amap-container')
  if (!mapContainer) return

  if (!isFullscreen.value) {
    if (mapContainer.requestFullscreen) {
      mapContainer.requestFullscreen()
    } else if (mapContainer.webkitRequestFullscreen) {
      mapContainer.webkitRequestFullscreen()
    } else if (mapContainer.mozRequestFullScreen) {
      mapContainer.mozRequestFullScreen()
    }
    isFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen()
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen()
    }
    isFullscreen.value = false
  }
}

// 尝试不同的地图服务
const tryMapService = async (service) => {
  currentMapService.value = service
  mapInitialized.value = false

  ElMessage.info(`正在切换到${service === 'amap' ? '高德' : service === 'baidu' ? '百度' : '腾讯'}地图...`)

  try {
    if (service === 'amap') {
      await initializeMap()
    } else {
      // 其他地图服务的初始化逻辑
      ElMessage.warning(`${service}地图服务暂未实现，请使用高德地图`)
    }
  } catch (error) {
    ElMessage.error(`${service}地图服务不可用`)
  }
}

// 添加医院标记到地图
const addHospitalMarkersToMap = async () => {
  try {
    if (!mapInitialized.value || !amapService.map) {
      console.log('地图未初始化，跳过添加标记')
      return
    }

    if (filteredHospitals.value.length === 0) {
      console.log('没有医院数据，跳过添加标记')
      return
    }

    console.log(`准备添加 ${filteredHospitals.value.length} 个医院标记`)

    // 清除之前的标记
    if (currentMarkers.value.length > 0) {
      currentMarkers.value.forEach(marker => {
        amapService.map.remove(marker)
      })
      currentMarkers.value = []
    }

    // 为每个医院添加标记
    const markers = []
    for (const hospital of filteredHospitals.value) {
      try {
        // 获取医院坐标
        let lng, lat
        if (hospital.longitude && hospital.latitude) {
          lng = hospital.longitude
          lat = hospital.latitude
        } else {
          // 使用地理编码获取坐标
          const coords = await getCoordinatesByAddress(hospital.address)
          lng = coords.longitude
          lat = coords.latitude
        }

        // @ts-ignore
        const marker = new window.AMap.Marker({
          position: [lng, lat],
          title: hospital.name,
          // 使用安全的医院图标创建函数
          // @ts-ignore
          icon: new window.AMap.Icon({
            // @ts-ignore
            size: new window.AMap.Size(28, 28),
            image: createHospitalIcon(),
            // @ts-ignore
            imageOffset: new window.AMap.Pixel(-14, -14)
          })
        })

        // 创建信息窗口
        // @ts-ignore
        const infoWindow = new window.AMap.InfoWindow({
          content: `
            <div style="
              background: linear-gradient(135deg, #1a1a2e, #2a2a4e);
              padding: 12px;
              border-radius: 8px;
              box-shadow: 0 4px 15px rgba(0,0,0,0.3);
              color: white;
              font-family: '微软雅黑', sans-serif;
              min-width: 200px;
              max-width: 250px;
            ">
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 16px;">🏥</span>
                <h4 style="margin: 0; color: #00ff88; font-size: 14px; font-weight: bold;">${hospital.name}</h4>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 8px; font-size: 11px;">
                <span style="background: rgba(0,255,136,0.2); padding: 2px 6px; border-radius: 10px; color: #00ff88;">${hospital.level}</span>
                <span style="background: rgba(0,136,255,0.2); padding: 2px 6px; border-radius: 10px; color: #0088ff;">${hospital.distance}km</span>
              </div>
              <div style="display: flex; gap: 6px; margin-top: 8px;">
                <button onclick="navigateToHospital('${hospital.name}', ${lng}, ${lat})"
                        style="
                          background: #00ff88;
                          color: #1a1a2e;
                          border: none;
                          padding: 4px 8px;
                          border-radius: 4px;
                          font-size: 10px;
                          font-weight: bold;
                          cursor: pointer;
                          transition: all 0.2s ease;
                        "
                        onmouseover="this.style.background='#00cc6a'"
                        onmouseout="this.style.background='#00ff88'">
                  🧭 导航
                </button>
                <button onclick="makeAppointment('${hospital.name}')"
                        style="
                          background: #007bff;
                          color: white;
                          border: none;
                          padding: 4px 8px;
                          border-radius: 4px;
                          font-size: 10px;
                          font-weight: bold;
                          cursor: pointer;
                          transition: all 0.2s ease;
                        "
                        onmouseover="this.style.background='#0056b3'"
                        onmouseout="this.style.background='#007bff'">
                  📅 预约
                </button>
              </div>
            </div>
          `,
          offset: new window.AMap.Pixel(0, -30)
        })

        // 点击标记显示信息窗口
        marker.on('click', () => {
          infoWindow.open(amapService.map, marker.getPosition())
        })

        amapService.map.add(marker)
        markers.push(marker)

      } catch (error) {
        console.warn(`添加医院标记失败: ${hospital.name}`, error)
      }
    }

    currentMarkers.value = markers

    // 调整地图视野以显示所有标记
    if (markers.length > 0) {
      amapService.map.setFitView(markers, false, [20, 20, 20, 20])
    }

    console.log(`成功添加 ${markers.length} 个医院标记`)

  } catch (error) {
    console.error('添加医院标记失败:', error)
  }
}



const locateUser = async () => {
  try {
    isLocating.value = true
    ElMessage.info('正在获取您的位置...')

    const position = await amapService.getCurrentPosition()
    userLocation.value = {
      latitude: position.latitude,
      longitude: position.longitude,
      address: position.address
    }

    // 设置地图中心为用户位置
    if (mapInitialized.value && amapService.map) {
      amapService.setCenter(position.longitude, position.latitude, 15)

      // 添加用户位置标记
      const userMarker = new window.AMap.Marker({
        position: [position.longitude, position.latitude],
        icon: new window.AMap.Icon({
          size: new window.AMap.Size(32, 32),
          image: createUserLocationIcon(),
          imageOffset: new window.AMap.Pixel(-16, -16)
        }),
        title: '我的位置'
      })

      amapService.map.add(userMarker)
    }

    ElMessage.success(`定位成功：${position.address}`)

    // 重新搜索附近医院
    await handleSearch()
  } catch (error) {
    console.error('定位失败:', error)
    let errorMessage = '定位失败'

    if (error.code === 1) {
      errorMessage = '定位权限被拒绝，请在浏览器设置中允许位置访问'
    } else if (error.code === 2) {
      errorMessage = '无法获取位置信息，请检查网络连接'
    } else if (error.code === 3) {
      errorMessage = '定位超时，请重试'
    }

    ElMessage.error(errorMessage)
  } finally {
    isLocating.value = false
  }
}

const showAllHospitals = async () => {
  if (mapInitialized.value && filteredHospitals.value.length > 0) {
    await addHospitalMarkersToMap()
    ElMessage.success(`已显示 ${filteredHospitals.value.length} 家医院`)
  } else {
    ElMessage.warning('暂无医院数据或地图未初始化')
  }
}

// 备用界面的医院排序方法
const sortHospitalsByDistance = () => {
  hospitals.value.sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance))
  ElMessage.success('已按距离排序')
}

const sortHospitalsByRating = () => {
  hospitals.value.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating))
  ElMessage.success('已按评分排序')
}

// 从备用界面选择医院
const selectHospitalFromFallback = (hospital) => {
  ElMessage.success(`已选择 ${hospital.name}`)
  // 可以在这里添加更多选择医院后的逻辑，比如跳转到详情页
}

// 刷新地图
const refreshMap = async () => {
  if (!mapInitialized.value) {
    await initializeMap()
  } else {
    await addHospitalMarkersToMap()
    ElMessage.success('地图已刷新')
  }
}

// 路线面板相关函数 - 暂时禁用
/*
const closeRoutePanel = () => {
  showRoutePanel.value = false
  // 清空路线面板内容
  const routePanel = document.getElementById('route-panel')
  if (routePanel) {
    routePanel.innerHTML = ''
  }
}
*/

const testMapAPI = () => {
  console.log('=== 高德地图API状态检查 ===')
  // @ts-ignore
  console.log('window.AMap:', !!window.AMap)
  // @ts-ignore
  console.log('window.AMap.Map:', !!(window.AMap && window.AMap.Map))
  // @ts-ignore
  console.log('window.amapReady:', !!window.amapReady)
  console.log('mapInitialized:', mapInitialized.value)
  console.log('地图容器存在:', !!document.getElementById('amap-container'))

  const container = document.getElementById('amap-container')
  if (container) {
    console.log('容器尺寸:', {
      width: container.offsetWidth,
      height: container.offsetHeight,
      display: window.getComputedStyle(container).display,
      visibility: window.getComputedStyle(container).visibility
    })
  }

  ElMessage.info('API状态已输出到控制台，请查看开发者工具')
}

const loadMapAPI = async () => {
  try {
    ElMessage.info('正在加载高德地图API...')

    // @ts-ignore
    if (window.loadAmapAPI) {
      // @ts-ignore
      await window.loadAmapAPI()
      ElMessage.success('高德地图API加载成功！')
    } else {
      ElMessage.error('动态加载函数不存在')
    }
  } catch (error) {
    console.error('加载高德地图API失败:', error)
    ElMessage.error(`API加载失败: ${error.message}`)
  }
}

// 使用模拟地图
const useSimulatedMap = () => {
  ElMessage.info('启用模拟地图模式')
  mapInitialized.value = true

  // 创建一个简单的模拟地图界面
  const mapContainer = document.getElementById('amap-container')
  if (mapContainer) {
    mapContainer.innerHTML = `
      <div style="width: 100%; height: 100%; background: linear-gradient(135deg, #1e3c72, #2a5298); display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; position: relative;">
        <div style="position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;">
          <h4 style="margin: 0; color: #00ff88;">🗺️ 模拟地图视图</h4>
          <p style="margin: 5px 0 0 0; font-size: 12px;">显示 ${filteredHospitals.value.length} 家医院</p>
        </div>

        <div style="text-align: center; z-index: 10;">
          <div style="font-size: 48px; margin-bottom: 20px;">🏥</div>
          <h3 style="margin: 0 0 10px 0;">医院分布图</h3>
          <p style="margin: 0; opacity: 0.8;">模拟显示医院位置信息</p>
        </div>

        <div style="position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; max-width: 300px;">
          <h5 style="margin: 0 0 10px 0; color: #00ff88;">📍 附近医院</h5>
          ${filteredHospitals.value.slice(0, 3).map(hospital => `
            <div style="margin-bottom: 8px; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 5px;">
              <div style="font-weight: bold; font-size: 14px;">${hospital.name}</div>
              <div style="font-size: 12px; opacity: 0.8;">${hospital.distance}km • ${hospital.level}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `
  }
}

// 打开外部地图导航
const openExternalMap = (hospital) => {
  const name = encodeURIComponent(hospital.name)

  // 尝试从医院数据中获取坐标，如果没有则使用默认坐标
  let longitude = hospital.longitude || userLocation.value.longitude
  let latitude = hospital.latitude || userLocation.value.latitude

  // 如果医院有距离信息，可以估算大概位置（这里简化处理）
  if (hospital.distance && !hospital.longitude) {
    // 简单的坐标偏移估算（实际项目中应该使用地理编码）
    const distance = parseFloat(hospital.distance)
    const offsetLng = (Math.random() - 0.5) * distance * 0.01
    const offsetLat = (Math.random() - 0.5) * distance * 0.01
    longitude = userLocation.value.longitude + offsetLng
    latitude = userLocation.value.latitude + offsetLat
  }

  // 创建多个地图选项
  const mapOptions = [
    {
      name: '百度地图',
      url: `https://api.map.baidu.com/direction?origin=${userLocation.value.latitude},${userLocation.value.longitude}&destination=${latitude},${longitude}&mode=driving&region=全国&output=html&src=webapp.baidu.openAPIdemo`
    },
    {
      name: '高德地图',
      url: `https://uri.amap.com/navigation?from=${userLocation.value.longitude},${userLocation.value.latitude}&to=${longitude},${latitude}&name=${name}&src=mypage`
    },
    {
      name: '腾讯地图',
      url: `https://apis.map.qq.com/uri/v1/routeplan?type=drive&from=我的位置&fromcoord=${userLocation.value.latitude},${userLocation.value.longitude}&to=${name}&tocoord=${latitude},${longitude}&referer=myapp`
    },
    {
      name: '谷歌地图',
      url: `https://www.google.com/maps/dir/${userLocation.value.latitude},${userLocation.value.longitude}/${latitude},${longitude}`
    }
  ]

  // 创建一个更友好的选择界面
  showNavigationOptions(hospital, mapOptions)
}

// 显示导航选项
const showNavigationOptions = (hospital, mapOptions) => {
  // 创建模态框
  const modal = document.createElement('div')
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
  `

  const content = document.createElement('div')
  content.style.cssText = `
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    border-radius: 15px;
    padding: 30px;
    max-width: 500px;
    width: 90%;
    color: white;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  `

  content.innerHTML = `
    <div style="text-align: center; margin-bottom: 25px;">
      <h3 style="margin: 0 0 10px 0; color: #00ff88;">🧭 选择导航方式</h3>
      <p style="margin: 0; color: #ccc; font-size: 14px;">
        目的地：${hospital.name}<br>
        地址：${hospital.address}
      </p>
    </div>

    <div style="display: grid; gap: 15px;">
      ${mapOptions.map((option, index) => `
        <button
          onclick="openMapApp('${option.url}')"
          style="
            background: rgba(0, 255, 136, 0.1);
            border: 2px solid rgba(0, 255, 136, 0.3);
            border-radius: 10px;
            padding: 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
          "
          onmouseover="this.style.background='rgba(0, 255, 136, 0.2)'; this.style.borderColor='#00ff88'"
          onmouseout="this.style.background='rgba(0, 255, 136, 0.1)'; this.style.borderColor='rgba(0, 255, 136, 0.3)'"
        >
          ${getMapIcon(option.name)} ${option.name}
        </button>
      `).join('')}
    </div>

    <div style="display: flex; gap: 15px; margin-top: 25px;">
      <button
        onclick="copyAddress('${hospital.name} ${hospital.address}')"
        style="
          flex: 1;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.3);
          border-radius: 8px;
          padding: 12px;
          color: white;
          cursor: pointer;
          font-size: 14px;
        "
      >
        📋 复制地址
      </button>
      <button
        onclick="closeNavigationModal()"
        style="
          flex: 1;
          background: rgba(255, 0, 0, 0.2);
          border: 1px solid rgba(255, 0, 0, 0.3);
          border-radius: 8px;
          padding: 12px;
          color: white;
          cursor: pointer;
          font-size: 14px;
        "
      >
        ❌ 取消
      </button>
    </div>
  `

  modal.appendChild(content)
  document.body.appendChild(modal)

  // 添加全局函数
  window.openMapApp = (url) => {
    window.open(url, '_blank')
    ElMessage.success('正在打开地图导航')
    closeNavigationModal()
  }

  window.copyAddress = (address) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(address)
      ElMessage.success('地址已复制到剪贴板')
    } else {
      ElMessage.info(`地址：${address}`)
    }
    closeNavigationModal()
  }

  window.closeNavigationModal = () => {
    document.body.removeChild(modal)
    delete window.openMapApp
    delete window.copyAddress
    delete window.closeNavigationModal
  }

  // 点击背景关闭
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeNavigationModal()
    }
  })
}

// 获取地图图标
const getMapIcon = (mapName) => {
  const icons = {
    '百度地图': '🟦',
    '高德地图': '🟩',
    '腾讯地图': '🟨',
    '谷歌地图': '🟥'
  }
  return icons[mapName] || '🗺️'
}

// 分页处理
const handlePageChange = (page) => {
  if (page >= 1 && page <= Math.ceil(filteredHospitals.value.length / pageSize.value)) {
    currentPage.value = page
  }
}

// 选择医院
const selectHospital = (hospital) => {
  ElMessage.info(`您选择了 ${hospital.name}`)
  // 这里可以跳转到医院详情页面
}

// 导航到医院
const navigateToHospital = async (hospital) => {
  try {
    // 如果是从地图标记点调用，参数可能是字符串
    let hospitalName, lng, lat

    if (typeof hospital === 'string') {
      // 从地图标记点调用的情况
      hospitalName = arguments[0]
      lng = arguments[1]
      lat = arguments[2]
    } else {
      // 从医院列表调用的情况
      hospitalName = hospital.name

      // 尝试获取医院坐标
      if (hospital.longitude && hospital.latitude) {
        lng = hospital.longitude
        lat = hospital.latitude
      } else {
        // 如果没有坐标，尝试通过地理编码获取
        try {
          const coords = await getCoordinatesByAddress(hospital.address)
          lng = coords.longitude
          lat = coords.latitude
        } catch (error) {
          console.warn('地理编码失败，使用估算坐标:', error)
          // 使用估算坐标作为备用方案
          const distance = parseFloat(hospital.distance) || 5
          const offsetLng = (Math.random() - 0.5) * distance * 0.01
          const offsetLat = (Math.random() - 0.5) * distance * 0.01
          lng = userLocation.value.longitude + offsetLng
          lat = userLocation.value.latitude + offsetLat
        }
      }
    }

    // 优先使用外部地图导航
    const useExternalNavigation = confirm(
      `选择导航方式：\n\n` +
      `确定：使用外部地图应用导航\n` +
      `取消：在当前页面显示路线\n\n` +
      `目的地：${hospitalName}`
    )

    if (useExternalNavigation) {
      // 使用外部地图导航
      openExternalMapNavigation(hospital, lng, lat)
    } else {
      // 使用内置地图显示路线
      await showInternalRoute(hospitalName, lng, lat)
    }

  } catch (error) {
    console.error('导航失败:', error)
    ElMessage.error('导航功能暂时不可用，请稍后重试')
  }
}

// 外部地图导航
const openExternalMapNavigation = (hospital, lng, lat) => {
  const name = encodeURIComponent(hospital.name)

  // 创建导航URL
  const mapOptions = [
    {
      name: '百度地图',
      url: `https://api.map.baidu.com/direction?origin=${userLocation.value.latitude},${userLocation.value.longitude}&destination=${lat},${lng}&mode=driving&region=全国&output=html&src=webapp.baidu.openAPIdemo`
    },
    {
      name: '高德地图',
      url: `https://uri.amap.com/navigation?from=${userLocation.value.longitude},${userLocation.value.latitude}&to=${lng},${lat}&name=${name}&src=mypage`
    },
    {
      name: '腾讯地图',
      url: `https://apis.map.qq.com/uri/v1/routeplan?type=drive&from=我的位置&fromcoord=${userLocation.value.latitude},${userLocation.value.longitude}&to=${name}&tocoord=${lat},${lng}&referer=myapp`
    }
  ]

  // 显示导航选项
  showNavigationOptions(hospital, mapOptions)
}

// 内置地图路线显示
const showInternalRoute = async (hospitalName, lng, lat) => {
  try {
    if (!mapInitialized.value) {
      await initializeMap()
    }

    // 切换到地图视图
    await switchToMapView()

    // 在地图上显示路线（简化版）
    // @ts-ignore
    if (window.AMap && amapService.map) {
      // 清除之前的路线
      amapService.map.clearMap()

      // 添加起点和终点标记
      // @ts-ignore
      const startMarker = new window.AMap.Marker({
        position: [userLocation.value.longitude, userLocation.value.latitude],
        title: '我的位置',
        // @ts-ignore
        icon: new window.AMap.Icon({
          // @ts-ignore
          size: new window.AMap.Size(25, 34),
          image: 'https://webapi.amap.com/theme/v1.3/markers/n/start.png'
        })
      })

      // @ts-ignore
      const endMarker = new window.AMap.Marker({
        position: [lng, lat],
        title: hospitalName,
        // @ts-ignore
        icon: new window.AMap.Icon({
          // @ts-ignore
          size: new window.AMap.Size(25, 34),
          image: 'https://webapi.amap.com/theme/v1.3/markers/n/end.png'
        })
      })

      amapService.map.add([startMarker, endMarker])

      // 调整地图视野
      amapService.map.setFitView([startMarker, endMarker])

      ElMessage.success(`已在地图上标记到 ${hospitalName} 的位置`)
    } else {
      ElMessage.warning('地图服务不可用，建议使用外部地图导航')
    }

    // 只有在成功添加路线后才显示面板
    // showRoutePanel.value = true
  } catch (error) {
    console.error('内置路线显示失败:', error)
    ElMessage.error('路线显示失败，建议使用外部地图导航')
  }
}

// 通过地址获取坐标（简化版地理编码）
const getCoordinatesByAddress = async (address) => {
  // 这里可以调用地理编码API，现在使用简化的估算方法
  return new Promise((resolve, reject) => {
    // 模拟地理编码延迟
    setTimeout(() => {
      // 根据地址关键词估算大概坐标
      let baseLng = userLocation.value.longitude
      let baseLat = userLocation.value.latitude

      // 简单的地址解析（实际项目中应该使用真实的地理编码API）
      if (address.includes('大连')) {
        baseLng = 121.6147
        baseLat = 38.9140
      } else if (address.includes('北京')) {
        baseLng = 116.4074
        baseLat = 39.9042
      } else if (address.includes('上海')) {
        baseLng = 121.4737
        baseLat = 31.2304
      } else if (address.includes('广州')) {
        baseLng = 113.2644
        baseLat = 23.1291
      } else if (address.includes('深圳')) {
        baseLng = 114.0579
        baseLat = 22.5431
      }

      // 添加随机偏移
      const offsetLng = (Math.random() - 0.5) * 0.02
      const offsetLat = (Math.random() - 0.5) * 0.02

      resolve({
        longitude: baseLng + offsetLng,
        latitude: baseLat + offsetLat
      })
    }, 500)
  })
}

// 预约挂号
const makeAppointment = (hospital) => {
  ElMessage.success(`正在跳转到 ${hospital.name} 的预约页面`)
  // 这里可以跳转到预约页面
}

// 智能交互处理
const handleNavigationGesture = (action) => {
  console.log('医院导航手势导航:', action)

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
      // 搜索医院
      if (searchForm.keyword.trim()) {
        searchHospitals()
        ElMessage.success('🤲 手势控制：开始搜索医院')
      } else {
        ElMessage.warning('🤲 手势控制：请先输入搜索关键词')
      }
      break
    default:
      console.log('未处理的手势动作:', action)
  }
}

const handleVoiceCommand = (command) => {
  console.log('语音命令:', command)
  if (command.type === 'system') {
    if (command.action === 'refresh') {
      location.reload()
    }
  }
}

const handleVoiceResponse = (response) => {
  console.log('语音回复:', response)
}

// 监听视图切换，初始化地图
const switchToMapView = async () => {
  currentView.value = 'map'

  // 确保UI状态正确
  ensureUIState()

  // 等待DOM更新后初始化地图
  await nextTick()

  // 额外等待一点时间确保DOM完全渲染
  await new Promise(resolve => setTimeout(resolve, 100))

  if (!mapInitialized.value) {
    await initializeMap()
  } else {
    // 如果地图已初始化，更新医院标记
    await addHospitalMarkersToMap()
  }
}

// 监听医院数据变化，自动更新地图标记
const updateMapWhenDataChanges = async () => {
  if (currentView.value === 'map' && mapInitialized.value) {
    await addHospitalMarkersToMap()
  }
}

// 确保UI状态正确
const ensureUIState = () => {
  // 确保路线面板是关闭的 - 暂时禁用
  // showRoutePanel.value = false

  // 清空路线面板内容 - 暂时禁用
  /*
  const routePanel = document.getElementById('route-panel')
  if (routePanel) {
    routePanel.innerHTML = ''
  }
  */

  console.log('UI状态已重置')
}

// 生命周期
onMounted(async () => {
  // 确保UI状态正确
  ensureUIState()

  // 初始化医院数据
  await fetchHospitalsFromDatabase()

  // 模拟实时数据更新
  setInterval(() => {
    // 更新统计数据
    totalHospitals.value = hospitals.value.length || 156
    onlineDoctors.value = 1200 + Math.floor(Math.random() * 100)
    todayAppointments.value = 80 + Math.floor(Math.random() * 20)
  }, 30000) // 30秒更新一次
})

// 组件卸载时清理地图
onUnmounted(() => {
  if (mapInitialized.value) {
    amapService.destroy()
  }
})

// 将导航函数暴露到全局，供地图标记点使用
window.navigateToHospital = navigateToHospital
window.makeAppointment = (hospitalName) => {
  ElMessage.success(`正在跳转到 ${hospitalName} 的预约页面`)
  // 这里可以跳转到预约页面
}
</script>

<style scoped>
/* 整体页面样式 */
.hospital-navigation {
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

.navigation-avatar {
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

.location-status {
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

/* 卡片样式 */
.recommendation-section,
.search-section {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.recommendation-section:hover,
.search-section:hover {
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

.recommendation-status {
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

.card-content {
  padding: 20px;
}

/* 表单样式 */
.symptom-input,
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
  min-height: 80px;
}

/* AI推荐样式 */
.ai-recommendation {
  background: rgba(0, 255, 136, 0.1);
  border-radius: 10px;
  padding: 15px;
  border-left: 4px solid #00ff88;
  margin-top: 15px;
}

.recommendation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.recommendation-icon {
  font-size: 18px;
}

.recommendation-title {
  font-weight: bold;
  color: #00ff88;
}

.recommendation-content {
  margin-bottom: 15px;
}

.recommended-department,
.recommendation-reason {
  margin-bottom: 8px;
  color: #e0e0e0;
  font-size: 14px;
  line-height: 1.4;
}

.recommendation-actions {
  display: flex;
  justify-content: flex-end;
}

.apply-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(0, 255, 136, 0.2);
  border: 1px solid #00ff88;
  border-radius: 20px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apply-btn:hover {
  background: #00ff88;
  color: #000;
  transform: translateY(-1px);
}

/* 搜索操作按钮 */
.search-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.location-btn,
.reset-btn {
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

.location-btn {
  background: rgba(0, 136, 255, 0.2);
  border: 2px solid rgba(0, 136, 255, 0.3);
  color: #0088ff;
  flex: 1;
}

.location-btn:hover {
  background: rgba(0, 136, 255, 0.3);
  border-color: #0088ff;
  transform: translateY(-2px);
}

.reset-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(0, 255, 136, 0.3);
  color: #00ff88;
}

.reset-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

/* 视图切换 */
.view-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 25px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.toggle-btn:hover {
  background: rgba(0, 255, 136, 0.1);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.toggle-btn.active {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #000;
  border-color: #00ff88;
}

.btn-icon {
  font-size: 16px;
}

/* 医院列表样式 */
.list-header {
  margin-bottom: 20px;
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

.hospitals-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hospital-card {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  padding: 25px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.hospital-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 15px 40px rgba(0, 255, 136, 0.2);
}

.hospital-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.hospital-avatar {
  position: relative;
  flex-shrink: 0;
}

.hospital-avatar .avatar-circle {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
}

.avatar-text {
  font-size: 24px;
  font-weight: bold;
  color: #000;
}

.hospital-level-badge {
  position: absolute;
  bottom: -5px;
  right: -5px;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: bold;
  border: 2px solid #fff;
}

.hospital-level-badge.三甲 {
  background: #ff6b6b;
  color: #fff;
}

.hospital-level-badge.三乙 {
  background: #4ecdc4;
  color: #fff;
}

.hospital-level-badge.二甲 {
  background: #45b7d1;
  color: #fff;
}

.hospital-level-badge.专科 {
  background: #f9ca24;
  color: #000;
}

.hospital-basic-info {
  flex: 1;
}

.hospital-name {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
}

.hospital-address {
  margin: 0 0 12px 0;
  color: #ccc;
  font-size: 14px;
}

.hospital-rating {
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

.rating-count {
  color: #ccc;
  font-size: 12px;
}

.hospital-distance {
  flex-shrink: 0;
}

.distance-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.distance-icon {
  font-size: 20px;
  color: #0088ff;
}

.distance-text {
  color: #0088ff;
  font-weight: bold;
  font-size: 14px;
}

.hospital-details {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
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
  min-width: 80px;
}

.detail-value {
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
}

.specialty-text {
  color: #00ff88;
}

.hospital-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 255, 136, 0.2);
}

.availability-info {
  display: flex;
  gap: 20px;
}

.availability-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.availability-icon {
  font-size: 16px;
  color: #00ff88;
}

.availability-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.availability-label {
  color: #ccc;
  font-size: 12px;
}

.availability-value {
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

/* 空状态样式 */
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

/* 分页样式 */
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

/* 地图视图样式 */
.map-view {
  height: 500px;
  /* 重置所有可能的空间 */
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.map-container {
  position: relative;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(30, 30, 60, 0.3));
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  overflow: hidden;
  backdrop-filter: blur(10px);
  /* 确保没有多余的空间 */
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 增强的地图控制面板 */
.map-controls {
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: rgba(0, 0, 0, 0.85);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.control-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.control-group.primary .control-btn {
  background: rgba(0, 255, 136, 0.15);
  border: 2px solid rgba(0, 255, 136, 0.4);
}

.control-group.secondary .control-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  min-width: 120px;
  justify-content: center;
}

.control-btn:hover {
  background: rgba(0, 255, 136, 0.25);
  border-color: #00ff88;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.control-btn.active {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
  color: #fff;
}

.control-btn.loading {
  animation: pulse 1.5s infinite;
}

.control-btn .btn-icon {
  font-size: 16px;
}

.control-btn .btn-text {
  font-weight: 500;
}

.map-info {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 15px;
}

.info-stats {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ccc;
  font-size: 14px;
}

.info-icon {
  font-size: 16px;
}

.info-text {
  font-weight: 500;
}

.amap-container {
  width: 100%;
  height: 100%;
  border-radius: 15px;
  flex: 1;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 路线面板样式 - 暂时注释掉 */
/*
.route-panel {
  position: absolute;
  top: 80px;
  right: 15px;
  width: 300px;
  max-height: 400px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 10px;
  backdrop-filter: blur(15px);
  z-index: 20;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
}

.panel-header h4 {
  margin: 0;
  color: #00ff88;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 107, 107, 0.2);
}

.route-content {
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
  color: #ffffff;
  font-size: 14px;
}
*/

/* 地图加载状态 */
.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(30, 30, 60, 0.8));
  border-radius: 15px;
  z-index: 5;
}

.loading-content {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(0, 255, 136, 0.3);
  border-top: 4px solid #00ff88;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-content h3 {
  color: #00ff88;
  font-size: 24px;
  margin-bottom: 10px;
}

.loading-content p {
  color: #ccc;
  font-size: 16px;
  margin-bottom: 20px;
}

.loading-progress {
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin: 0 auto;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #00ff88, #00cc6a);
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* 地图工具栏 */
.map-toolbar {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toolbar-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  padding: 10px;
  backdrop-filter: blur(10px);
}

.toolbar-btn {
  width: 40px;
  height: 40px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 8px;
  color: #00ff88;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.toolbar-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
  transform: scale(1.1);
}

/* 地图备用界面样式 */
.map-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(30, 30, 60, 0.4));
  border-radius: 15px;
  flex: 1;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}

.fallback-content {
  text-align: center;
  padding: 40px;
  max-width: 900px;
  width: 100%;
}

.fallback-header {
  margin-bottom: 30px;
}

/* 地图服务选择器 */
.map-service-selector {
  margin: 30px 0;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  border: 1px solid rgba(0, 255, 136, 0.2);
}

.map-service-selector h4 {
  color: #00ff88;
  font-size: 18px;
  margin-bottom: 15px;
}

.service-options {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.service-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.service-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
}

.service-btn.active {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
  color: #00ff88;
}

.service-icon {
  font-size: 24px;
}

.service-name {
  font-weight: 600;
  font-size: 14px;
}

.service-status {
  font-size: 12px;
  opacity: 0.8;
}

/* 智能医院列表 */
.smart-hospital-list {
  margin-top: 30px;
  text-align: left;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.list-header h4 {
  color: #00ff88;
  font-size: 20px;
  margin: 0;
}

.list-controls {
  display: flex;
  gap: 10px;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 15px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
}

.smart-hospital-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.smart-hospital-card {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 15px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.smart-hospital-card:hover {
  border-color: rgba(0, 255, 136, 0.5);
  background: rgba(0, 255, 136, 0.05);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 255, 136, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.hospital-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  color: #000;
  font-weight: bold;
  font-size: 18px;
}

.hospital-basic {
  flex: 1;
}

.hospital-name {
  color: #fff;
  font-size: 16px;
  margin: 0 0 5px 0;
  font-weight: 600;
}

.hospital-level {
  color: #00ff88;
  font-size: 12px;
  margin: 0;
}

.hospital-distance {
  text-align: right;
}

.distance-value {
  color: #00ff88;
  font-size: 14px;
  font-weight: bold;
}

.card-content {
  margin-bottom: 15px;
}

.hospital-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.rating-stars {
  color: #ffd700;
  font-size: 14px;
}

.rating-score {
  color: #ccc;
  font-size: 14px;
}

.hospital-specialties {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.specialty-tag {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  font-weight: 500;
}

.action-btn.primary {
  background: rgba(0, 255, 136, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.4);
  color: #00ff88;
}

.action-btn.primary:hover {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #fff;
}

.fallback-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.8;
}

.fallback-content h3 {
  color: #00ff88;
  font-size: 24px;
  margin-bottom: 10px;
}

.fallback-content p {
  color: #ccc;
  font-size: 16px;
  margin-bottom: 30px;
}

.fallback-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 40px;
}

.fallback-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(0, 255, 136, 0.2);
  border: 2px solid rgba(0, 255, 136, 0.3);
  border-radius: 25px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.fallback-btn:hover {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
  transform: translateY(-2px);
}

.fallback-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
}

.fallback-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
}

.fallback-hospital-list {
  text-align: left;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 10px;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.fallback-hospital-list h4 {
  color: #00ff88;
  font-size: 18px;
  margin-bottom: 15px;
  text-align: center;
}

.simple-hospital-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.simple-hospital-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.simple-hospital-item:hover {
  border-color: rgba(0, 255, 136, 0.3);
  background: rgba(0, 255, 136, 0.05);
}

.hospital-info h5 {
  color: #ffffff;
  font-size: 16px;
  margin: 0 0 5px 0;
}

.hospital-info p {
  color: #ccc;
  font-size: 14px;
  margin: 0 0 5px 0;
}

.hospital-distance {
  color: #00ff88;
  font-size: 12px;
  font-weight: bold;
}

.simple-btn {
  padding: 6px 12px;
  background: rgba(0, 255, 136, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 15px;
  color: #00ff88;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.simple-btn:hover {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
}

.simple-btn.secondary {
  background: rgba(0, 136, 255, 0.2);
  border-color: rgba(0, 136, 255, 0.3);
  color: #0088ff;
}

.simple-btn.secondary:hover {
  background: rgba(0, 136, 255, 0.3);
  border-color: #0088ff;
}

/* API错误信息样式 */
.api-error-info {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 10px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
  color: #ff6b6b;
  font-size: 14px;
}

.error-icon {
  font-size: 18px;
}

.solution-links {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.solution-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(0, 255, 136, 0.2);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 20px;
  color: #00ff88;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.solution-link:hover {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
  transform: translateY(-1px);
  text-decoration: none;
  color: #00ff88;
}

.solution-link.btn {
  background: rgba(0, 136, 255, 0.2);
  border-color: rgba(0, 136, 255, 0.3);
  color: #0088ff;
}

.solution-link.btn:hover {
  background: rgba(0, 136, 255, 0.3);
  border-color: #0088ff;
  color: #0088ff;
}

.hospital-meta {
  display: flex;
  gap: 10px;
  margin-top: 5px;
}

.hospital-level {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: bold;
}

.hospital-actions {
  display: flex;
  gap: 8px;
  flex-direction: column;
}



.map-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-content {
  text-align: center;
  max-width: 500px;
  padding: 40px;
}

.map-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.map-content h3 {
  color: #00ff88;
  font-size: 24px;
  margin: 0 0 15px 0;
}

.map-content p {
  color: #ccc;
  font-size: 16px;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.map-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  text-align: left;
}

.feature-item {
  padding: 10px 15px;
  background: rgba(0, 255, 136, 0.1);
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 14px;
  border-left: 3px solid #00ff88;
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

.hospital-card {
  animation: fadeInUp 0.6s ease-out;
}

.hospital-card:nth-child(2) {
  animation-delay: 0.1s;
}

.hospital-card:nth-child(3) {
  animation-delay: 0.2s;
}

.hospital-card:nth-child(4) {
  animation-delay: 0.3s;
}

.hospital-card:nth-child(5) {
  animation-delay: 0.4s;
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
  .hospital-navigation {
    padding-top: 60px;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 15px;
    padding: 20px;
  }

  .navigation-avatar .avatar-circle {
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

  .hospital-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .hospital-avatar .avatar-circle {
    width: 60px;
    height: 60px;
    font-size: 20px;
  }

  .hospital-footer {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .availability-info {
    justify-content: center;
  }

  .action-buttons {
    justify-content: center;
  }

  .pagination-controls {
    flex-direction: column;
    gap: 10px;
  }

  .map-features {
    grid-template-columns: 1fr;
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

  .hospital-card {
    padding: 20px;
  }

  .search-actions {
    flex-direction: column;
  }

  .view-toggle {
    flex-direction: column;
  }
}

/* 增强的AI推荐样式 */
.ai-recommendation {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  margin-top: 15px;
  color: white;
}

.recommendation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.recommendation-header .left-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.recommendation-icon {
  font-size: 24px;
}

.recommendation-title {
  font-size: 18px;
  font-weight: bold;
}

.urgency-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.urgency-badge.较高 {
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid #ff4444;
}

.urgency-badge.中等 {
  background: rgba(255, 193, 7, 0.2);
  border: 1px solid #ffc107;
}

.urgency-badge.较低 {
  background: rgba(40, 167, 69, 0.2);
  border: 1px solid #28a745;
}

.analyzing-state {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  text-align: center;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.recommendation-content {
  margin-bottom: 15px;
}

.recommended-department,
.recommendation-reason {
  margin-bottom: 15px;
  line-height: 1.6;
}

.possible-causes,
.recommended-tests,
.life-suggestions,
.recommended-hospitals {
  margin-bottom: 15px;
}

.causes-list,
.tests-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.cause-tag,
.test-tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.suggestions-list {
  margin: 8px 0 0 20px;
  padding: 0;
}

.suggestions-list li {
  margin-bottom: 5px;
  line-height: 1.4;
}

.recommended-hospital-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
}

.hospital-info .hospital-name {
  font-weight: bold;
  margin-bottom: 4px;
}

.hospital-details {
  display: flex;
  gap: 12px;
  font-size: 12px;
  opacity: 0.9;
}

.hospital-level,
.hospital-distance,
.hospital-rating {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 12px;
}

.select-hospital-btn {
  background: #00ff88;
  color: #1a1a2e;
  border: none;
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-hospital-btn:hover {
  background: #00cc6a;
  transform: translateY(-1px);
}

.recommendation-actions {
  display: flex;
  gap: 10px;
}

.apply-btn,
.detailed-btn {
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.apply-btn {
  background: #00ff88;
  color: #1a1a2e;
}

.detailed-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.apply-btn:hover {
  background: #00cc6a;
  transform: translateY(-2px);
}

.detailed-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}
</style>
