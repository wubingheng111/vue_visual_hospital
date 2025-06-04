/**
 * 百度地图服务工具类
 * API Key: xXqn0mRSh3C2sry9vDQbcpeHQvPmnbWc
 */

class BaiduMapService {
  constructor() {
    this.ak = 'xXqn0mRSh3C2sry9vDQbcpeHQvPmnbWc'
    this.map = null
    this.geolocation = null
    this.geocoder = null
  }

  /**
   * 等待百度地图API加载完成
   */
  async waitForBMapAPI() {
    // 如果API已经加载完成
    if (window.BMap && window.BMap.Map && window.baiduMapReady) {
      return Promise.resolve()
    }

    // 如果有动态加载函数，使用它
    if (window.loadBaiduMapAPI) {
      try {
        await window.loadBaiduMapAPI()
        return Promise.resolve()
      } catch (error) {
        console.error('动态加载百度地图API失败:', error)
        throw error
      }
    }

    // 备用方案：轮询检查
    return new Promise((resolve, reject) => {
      let checkCount = 0
      const maxChecks = 100 // 最多检查10秒

      const checkAPI = () => {
        checkCount++
        console.log(`检查百度地图API状态 (${checkCount}/${maxChecks})...`)

        if (window.BMap && window.BMap.Map) {
          console.log('百度地图API检查成功')
          resolve()
        } else if (checkCount >= maxChecks) {
          reject(new Error('百度地图API加载超时，请检查网络连接和API Key'))
        } else {
          setTimeout(checkAPI, 100)
        }
      }

      checkAPI()
    })
  }

  /**
   * 初始化地图
   * @param {string} containerId - 地图容器ID
   * @param {Object} options - 地图配置选项
   */
  async initMap(containerId, options = {}) {
    try {
      // 等待API加载完成
      await this.waitForBMapAPI()

      // 检查容器是否存在
      const container = document.getElementById(containerId)
      if (!container) {
        throw new Error(`地图容器 ${containerId} 不存在`)
      }

      // 确保容器有尺寸
      if (container.offsetWidth === 0 || container.offsetHeight === 0) {
        container.style.width = '100%'
        container.style.height = '400px'
      }

      // 创建地图实例
      this.map = new window.BMap.Map(containerId)

      // 设置默认中心点（北京）
      const defaultCenter = new window.BMap.Point(116.4074, 39.9042)
      this.map.centerAndZoom(defaultCenter, options.zoom || 12)

      // 启用地图功能
      this.map.enableScrollWheelZoom(true) // 启用滚轮放大缩小
      this.map.enableDragging(true) // 启用拖拽
      this.map.enableDoubleClickZoom(true) // 启用双击放大

      // 添加基本控件
      try {
        this.map.addControl(new window.BMap.NavigationControl())
        this.map.addControl(new window.BMap.ScaleControl())
      } catch (controlError) {
        console.warn('添加地图控件失败:', controlError)
      }

      // 初始化地理编码服务
      this.geocoder = new window.BMap.Geocoder()

      console.log('百度地图初始化成功')
      return this.map
    } catch (error) {
      console.error('地图初始化失败:', error)
      throw error
    }
  }

  /**
   * 获取当前位置
   */
  getCurrentPosition() {
    return new Promise((resolve, reject) => {
      if (!window.BMap) {
        reject(new Error('百度地图API未加载'))
        return
      }

      // 创建地理定位实例
      this.geolocation = new window.BMap.Geolocation()

      this.geolocation.getCurrentPosition((result) => {
        if (this.geolocation.getStatus() === window.BMAP_STATUS_SUCCESS) {
          const position = {
            longitude: result.point.lng,
            latitude: result.point.lat,
            accuracy: result.accuracy
          }

          // 获取地址信息
          this.getAddressByCoordinates(result.point.lng, result.point.lat)
            .then(address => {
              position.address = address
              resolve(position)
            })
            .catch(() => {
              position.address = '位置获取成功，地址解析失败'
              resolve(position)
            })
        } else {
          reject(new Error('定位失败：' + this.geolocation.getStatus()))
        }
      }, {
        enableHighAccuracy: true
      })
    })
  }

  /**
   * 根据坐标获取地址（逆地理编码）
   * @param {number} lng - 经度
   * @param {number} lat - 纬度
   */
  getAddressByCoordinates(lng, lat) {
    return new Promise((resolve, reject) => {
      if (!this.geocoder) {
        reject(new Error('地理编码服务未初始化'))
        return
      }

      const point = new window.BMap.Point(lng, lat)
      this.geocoder.getLocation(point, (result) => {
        if (result) {
          resolve(result.address)
        } else {
          reject(new Error('地址解析失败'))
        }
      })
    })
  }

  /**
   * 根据地址获取坐标（地理编码）
   * @param {string} address - 地址
   */
  getCoordinatesByAddress(address) {
    return new Promise((resolve, reject) => {
      if (!this.geocoder) {
        reject(new Error('地理编码服务未初始化'))
        return
      }

      this.geocoder.getPoint(address, (point) => {
        if (point) {
          resolve({
            longitude: point.lng,
            latitude: point.lat
          })
        } else {
          reject(new Error('地址解析失败'))
        }
      })
    })
  }

  /**
   * 在地图上添加标记点
   * @param {Array} hospitals - 医院列表
   */
  addHospitalMarkers(hospitals) {
    if (!this.map) {
      console.error('地图未初始化')
      return
    }

    // 清除现有标记
    this.map.clearOverlays()

    const markers = []

    hospitals.forEach((hospital, index) => {
      // 如果医院有坐标信息，直接使用
      if (hospital.longitude && hospital.latitude) {
        this.createMarker(hospital, hospital.longitude, hospital.latitude, markers)
      } else {
        // 否则通过地址获取坐标
        this.getCoordinatesByAddress(hospital.address)
          .then(coords => {
            this.createMarker(hospital, coords.longitude, coords.latitude, markers)
          })
          .catch(error => {
            console.warn(`医院 ${hospital.name} 地址解析失败:`, error)
          })
      }
    })

    return markers
  }

  /**
   * 创建标记点
   */
  createMarker(hospital, lng, lat, markers) {
    const point = new window.BMap.Point(lng, lat)

    // 创建自定义图标，不显示数字
    const icon = new window.BMap.Icon(
      'data:image/svg+xml;base64,' + btoa(`
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">
          <circle cx="14" cy="14" r="12" fill="#00ff88" stroke="#fff" stroke-width="2"/>
          <text x="14" y="18" text-anchor="middle" fill="#1a1a2e" font-size="14" font-weight="bold">🏥</text>
        </svg>
      `),
      new window.BMap.Size(28, 28),
      {
        anchor: new window.BMap.Size(14, 14)
      }
    )

    const marker = new window.BMap.Marker(point, { icon: icon })

    // 创建信息窗口
    const infoWindow = new window.BMap.InfoWindow(`
      <div style="padding: 10px; min-width: 200px;">
        <h4 style="margin: 0 0 8px 0; color: #333;">${hospital.name}</h4>
        <p style="margin: 4px 0; color: #666;"><strong>等级：</strong>${hospital.level}</p>
        <p style="margin: 4px 0; color: #666;"><strong>地址：</strong>${hospital.address}</p>
        <p style="margin: 4px 0; color: #666;"><strong>电话：</strong>${hospital.phone}</p>
        <p style="margin: 4px 0; color: #666;"><strong>科室：</strong>${hospital.departments?.join('、') || '综合科室'}</p>
        <div style="margin-top: 10px;">
          <button onclick="window.navigateToHospital('${hospital.name}', ${lng}, ${lat})"
                  style="background: #00ff88; color: white; border: none; padding: 5px 10px; border-radius: 3px; margin-right: 5px; cursor: pointer;">
            导航
          </button>
          <button onclick="window.makeAppointment('${hospital.name}')"
                  style="background: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
            预约
          </button>
        </div>
      </div>
    `)

    // 点击标记显示信息窗口
    marker.addEventListener('click', () => {
      this.map.openInfoWindow(infoWindow, point)
    })

    this.map.addOverlay(marker)
    markers.push({ marker, hospital, point })
  }

  /**
   * 规划路线
   * @param {Object} start - 起点坐标 {lng, lat}
   * @param {Object} end - 终点坐标 {lng, lat}
   */
  planRoute(start, end) {
    if (!this.map) {
      console.error('地图未初始化')
      return
    }

    // 创建驾车路线规划实例
    const driving = new window.BMap.DrivingRoute(this.map, {
      renderOptions: {
        map: this.map,
        autoViewport: true,
        panel: 'route-panel' // 如果有路线面板的话
      },
      onSearchComplete: (results) => {
        if (driving.getStatus() === window.BMAP_STATUS_SUCCESS) {
          const route = results.getPlan(0).getRoute(0)
          console.log('路线规划成功:', {
            distance: route.getDistance(),
            duration: route.getDuration()
          })
        }
      }
    })

    const startPoint = new window.BMap.Point(start.lng, start.lat)
    const endPoint = new window.BMap.Point(end.lng, end.lat)

    driving.search(startPoint, endPoint)
  }

  /**
   * 设置地图中心点
   * @param {number} lng - 经度
   * @param {number} lat - 纬度
   * @param {number} zoom - 缩放级别
   */
  setCenter(lng, lat, zoom = 15) {
    if (!this.map) {
      console.error('地图未初始化')
      return
    }

    const point = new window.BMap.Point(lng, lat)
    this.map.centerAndZoom(point, zoom)
  }

  /**
   * 计算两点间距离
   * @param {Object} point1 - 点1 {lng, lat}
   * @param {Object} point2 - 点2 {lng, lat}
   * @returns {number} 距离（米）
   */
  calculateDistance(point1, point2) {
    if (!window.BMap) {
      return 0
    }

    const p1 = new window.BMap.Point(point1.lng, point1.lat)
    const p2 = new window.BMap.Point(point2.lng, point2.lat)

    return this.map.getDistance(p1, p2)
  }

  /**
   * 销毁地图
   */
  destroy() {
    if (this.map) {
      this.map.clearOverlays()
      this.map = null
    }
    this.geocoder = null
    this.geolocation = null
  }
}

// 创建单例实例
const baiduMapService = new BaiduMapService()

export default baiduMapService
