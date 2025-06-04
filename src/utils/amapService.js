/**
 * 高德地图服务工具类
 * 免费API，更稳定可靠
 */

class AmapService {
  constructor() {
    this.ak = '1d064b3bc45a733c6b39466111c1c6ea' // 您的高德地图API Key
    this.securityKey = '7ee9d5db8b29546d418ddc7edf515eb9' // 安全密钥
    this.map = null
    this.geocoder = null
    this.markers = []
  }

  /**
   * 等待高德地图API加载完成
   */
  async waitForAmapAPI() {
    return new Promise((resolve, reject) => {
      if (window.AMap) {
        resolve()
        return
      }

      let checkCount = 0
      const maxChecks = 100

      const checkAPI = () => {
        checkCount++
        console.log(`检查高德地图API状态 (${checkCount}/${maxChecks})...`)

        if (window.AMap) {
          console.log('高德地图API检查成功')
          resolve()
        } else if (checkCount >= maxChecks) {
          reject(new Error('高德地图API加载超时'))
        } else {
          setTimeout(checkAPI, 100)
        }
      }

      checkAPI()
    })
  }

  /**
   * 动态加载高德地图API
   */
  loadAmapAPI() {
    return new Promise((resolve, reject) => {
      if (window.AMap) {
        resolve()
        return
      }

      // 使用全局的loadAmapAPI函数
      if (window.loadAmapAPI) {
        window.loadAmapAPI()
          .then(() => {
            console.log('高德地图API加载成功')
            resolve()
          })
          .catch((error) => {
            console.error('高德地图API加载失败:', error)
            reject(error)
          })
      } else {
        reject(new Error('全局loadAmapAPI函数不存在'))
      }
    })
  }

  /**
   * 初始化地图
   */
  async initMap(containerId, options = {}) {
    try {
      // 首先尝试加载API
      if (!window.AMap) {
        console.log('高德地图API未加载，开始加载...')
        await this.loadAmapAPI()
      }

      await this.waitForAmapAPI()

      const container = document.getElementById(containerId)
      if (!container) {
        throw new Error(`地图容器 ${containerId} 不存在`)
      }

      // 确保容器有尺寸
      if (container.offsetWidth === 0 || container.offsetHeight === 0) {
        container.style.width = '100%'
        container.style.height = '500px'
      }

      this.map = new window.AMap.Map(containerId, {
        zoom: options.zoom || 12,
        center: [116.4074, 39.9042], // 北京
        mapStyle: 'amap://styles/dark', // 深色主题
        viewMode: '2D'
      })

      // 初始化地理编码服务
      this.geocoder = new window.AMap.Geocoder()

      console.log('高德地图初始化成功')
      return this.map
    } catch (error) {
      console.error('地图初始化失败:', error)
      throw error
    }
  }

  /**
   * 获取当前位置
   */
  async getCurrentPosition() {
    return new Promise(async (resolve, reject) => {
      try {
        // 确保API已加载
        if (!window.AMap) {
          console.log('高德地图API未加载，开始加载...')
          await this.loadAmapAPI()
          await this.waitForAmapAPI()
        }

        // 使用高德地图的定位服务
        window.AMap.plugin('AMap.Geolocation', () => {
          const geolocation = new window.AMap.Geolocation({
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0,
            convert: true,
            showButton: false,
            buttonPosition: 'LB',
            showMarker: false,
            showCircle: false,
            panToLocation: false,
            zoomToAccuracy: false
          })

          geolocation.getCurrentPosition((status, result) => {
            if (status === 'complete') {
              const position = {
                longitude: result.position.lng,
                latitude: result.position.lat,
                address: result.formattedAddress || result.addressComponent?.city || result.addressComponent?.province || '大连市'
              }

              // 如果没有获取到详细地址，尝试逆地理编码
              if (!result.formattedAddress || result.formattedAddress === '位置获取成功') {
                this.getAddressByCoordinates(result.position.lng, result.position.lat)
                  .then(address => {
                    position.address = address
                    console.log('定位成功（含逆地理编码）:', position)
                    resolve(position)
                  })
                  .catch(() => {
                    // 如果逆地理编码失败，根据坐标判断城市
                    position.address = this.getCityByCoordinates(result.position.lng, result.position.lat)
                    console.log('定位成功（坐标推断）:', position)
                    resolve(position)
                  })
              } else {
                console.log('定位成功:', position)
                resolve(position)
              }
            } else {
              console.error('定位失败:', result)
              reject(new Error(`定位失败: ${result.message || '未知错误'}`))
            }
          })
        })
      } catch (error) {
        console.error('定位服务初始化失败:', error)
        reject(error)
      }
    })
  }

  /**
   * 根据坐标获取地址信息
   */
  getAddressByCoordinates(lng, lat) {
    return new Promise((resolve, reject) => {
      if (!this.geocoder) {
        reject(new Error('地理编码服务未初始化'))
        return
      }

      this.geocoder.getAddress([lng, lat], (status, result) => {
        if (status === 'complete' && result.regeocode) {
          const address = result.regeocode.formattedAddress
          resolve(address)
        } else {
          reject(new Error('逆地理编码失败'))
        }
      })
    })
  }

  /**
   * 根据坐标推断城市（备用方案）
   */
  getCityByCoordinates(lng, lat) {
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

  /**
   * 地理编码
   */
  getCoordinatesByAddress(address) {
    return new Promise((resolve, reject) => {
      if (!this.geocoder) {
        reject(new Error('地理编码服务未初始化'))
        return
      }

      this.geocoder.getLocation(address, (status, result) => {
        if (status === 'complete' && result.geocodes.length > 0) {
          const location = result.geocodes[0].location
          resolve({
            longitude: location.lng,
            latitude: location.lat
          })
        } else {
          reject(new Error('地址解析失败'))
        }
      })
    })
  }

  /**
   * 添加医院标记
   */
  addHospitalMarkers(hospitals) {
    if (!this.map) {
      console.error('地图未初始化')
      return []
    }

    // 清除现有标记
    this.clearMarkers()

    hospitals.forEach(hospital => {
      if (hospital.longitude && hospital.latitude) {
        this.createMarker(hospital, hospital.longitude, hospital.latitude)
      } else {
        // 通过地址获取坐标
        this.getCoordinatesByAddress(hospital.address)
          .then(coords => {
            this.createMarker(hospital, coords.longitude, coords.latitude)
          })
          .catch(error => {
            console.warn(`医院 ${hospital.name} 地址解析失败:`, error)
          })
      }
    })

    return this.markers
  }

  /**
   * 创建标记点
   */
  createMarker(hospital, lng, lat) {
    const marker = new window.AMap.Marker({
      position: [lng, lat],
      title: hospital.name,
      // 使用自定义医院图标，不显示数字
      icon: new window.AMap.Icon({
        size: new window.AMap.Size(28, 28),
        image: 'data:image/svg+xml;base64,' + btoa(`
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">
            <circle cx="14" cy="14" r="12" fill="#00ff88" stroke="#fff" stroke-width="2"/>
            <text x="14" y="18" text-anchor="middle" fill="#1a1a2e" font-size="14" font-weight="bold">🏥</text>
          </svg>
        `),
        imageOffset: new window.AMap.Pixel(-14, -14)
      })
    })

    // 创建信息窗口
    const infoWindow = new window.AMap.InfoWindow({
      content: `
        <div style="padding: 10px; min-width: 200px;">
          <h4 style="margin: 0 0 8px 0; color: #333;">${hospital.name}</h4>
          <p style="margin: 4px 0; color: #666;"><strong>等级：</strong>${hospital.level}</p>
          <p style="margin: 4px 0; color: #666;"><strong>地址：</strong>${hospital.address}</p>
          <p style="margin: 4px 0; color: #666;"><strong>电话：</strong>${hospital.phone}</p>
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
      `
    })

    marker.on('click', () => {
      infoWindow.open(this.map, marker.getPosition())
    })

    this.map.add(marker)
    this.markers.push(marker)
  }

  /**
   * 路线规划
   */
  planRoute(start, end) {
    if (!this.map) {
      console.error('地图未初始化')
      return
    }

    this.map.plugin('AMap.Driving', () => {
      const driving = new window.AMap.Driving({
        map: this.map,
        panel: 'route-panel'
      })

      driving.search([start.lng, start.lat], [end.lng, end.lat], (status, result) => {
        if (status === 'complete') {
          console.log('路线规划成功:', result)
        } else {
          console.error('路线规划失败:', result)
        }
      })
    })
  }

  /**
   * 设置地图中心
   */
  setCenter(lng, lat, zoom = 15) {
    if (!this.map) {
      console.error('地图未初始化')
      return
    }

    this.map.setZoomAndCenter(zoom, [lng, lat])
  }

  /**
   * 清除标记
   */
  clearMarkers() {
    if (this.markers.length > 0) {
      this.map.remove(this.markers)
      this.markers = []
    }
  }

  /**
   * 销毁地图
   */
  destroy() {
    if (this.map) {
      this.clearMarkers()
      this.map.destroy()
      this.map = null
    }
    this.geocoder = null
  }
}

// 创建单例实例
const amapService = new AmapService()

export default amapService
