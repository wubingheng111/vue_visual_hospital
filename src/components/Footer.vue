<template>
  <footer class="modern-footer">
    <div class="footer-container">
      <!-- 左侧信息 -->
      <div class="footer-left">
        <div class="footer-logo">
          <span class="logo-icon">🏥</span>
          <span class="logo-text">医慧之翼</span>
        </div>
      </div>

      <!-- 中间功能链接 -->
      <div class="footer-center">
        <div class="footer-links">
          <router-link to="/" class="footer-link">数据可视化</router-link>
          <router-link to="/intelligent-consultation" class="footer-link">智能问诊</router-link>
          <router-link to="/quary-doctor" class="footer-link">在线问诊</router-link>
          <router-link to="/personal" class="footer-link">康复训练</router-link>
          <router-link to="/health-analytics" class="footer-link">医院导航</router-link>
        </div>
      </div>

      <!-- 右侧版权信息 -->
      <div class="footer-right">
        <div class="footer-copyright">
          © {{ currentYear }} 医慧之翼智能医疗平台 · 基于AI技术驱动健康
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

// 获取当前年份
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.modern-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(135deg,
    rgba(0, 0, 0, 0.95) 0%,
    rgba(20, 20, 40, 0.95) 50%,
    rgba(0, 0, 0, 0.95) 100%);
  backdrop-filter: blur(20px);
  border-top: 2px solid rgba(0, 255, 136, 0.3);
  color: #ffffff;
  font-family: "微软雅黑", "PingFang SC", sans-serif;
  z-index: 1000;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.5);
}

.footer-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 8px 20px;
  gap: 20px;
  height: 40px;
}

/* 左侧区域 */
.footer-left {
  flex: 0 0 200px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 18px;
  animation: pulse 2s infinite;
}

.logo-text {
  font-size: 16px;
  font-weight: bold;
  color: #00ff88;
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}

/* 中间区域 */
.footer-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.footer-links {
  display: flex;
  gap: 25px;
  align-items: center;
}

.footer-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 12px;
  transition: all 0.3s ease;
  position: relative;
  white-space: nowrap;
}

.footer-link:hover {
  color: #00ff88;
  text-shadow: 0 0 5px rgba(0, 255, 136, 0.5);
}

.footer-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: #00ff88;
  transition: width 0.3s ease;
}

.footer-link:hover::after {
  width: 100%;
}

/* 右侧区域 */
.footer-right {
  flex: 0 0 300px;
  text-align: right;
}

.footer-copyright {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.2;
}

/* 动画效果 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .footer-container {
    padding: 8px 15px;
    gap: 15px;
  }

  .footer-left {
    flex: 0 0 150px;
  }

  .footer-right {
    flex: 0 0 250px;
  }

  .footer-links {
    gap: 20px;
  }

  .footer-link {
    font-size: 11px;
  }
}

@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    height: auto;
    padding: 10px;
    gap: 8px;
  }

  .footer-left,
  .footer-right {
    flex: none;
    text-align: center;
  }

  .footer-links {
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .footer-copyright {
    text-align: center;
    font-size: 10px;
  }
}
</style>