/**
 * API Service 中介层
 * 
 * 策略：当前使用 Mock 数据 + 模拟网络延迟
 * 未来联调真实后端时，只需修改此文件，将 mockRequest 替换为 axios 请求
 * 页面组件代码无需任何改动
 */

import {
  dashboardData,
  conversionData,
  productData,
  userInsightData,
  predictionData
} from './mockData.js'

/**
 * 模拟网络请求（带延迟）
 * @param {*} data - 要返回的数据
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Promise}
 */
function mockRequest(data, delay = 200) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        code: 200,
        message: 'success',
        data: data
      })
    }, delay)
  })
}

// ==================== Dashboard API ====================

/**
 * 获取驾驶舱数据
 */
export function fetchDashboardData() {
  return mockRequest(dashboardData)
}

/**
 * 获取核心指标
 */
export function fetchMetrics() {
  return mockRequest(dashboardData.metrics)
}

/**
 * 获取 PV/UV 趋势数据
 */
export function fetchPVUVTrend() {
  return mockRequest(dashboardData.pvuvTrend)
}

/**
 * 获取品类销售数据
 */
export function fetchCategorySales() {
  return mockRequest(dashboardData.categorySales)
}

// ==================== Conversion API ====================

/**
 * 获取转化分析数据
 */
export function fetchConversionData() {
  return mockRequest(conversionData)
}

/**
 * 获取漏斗图数据
 */
export function fetchFunnelData() {
  return mockRequest(conversionData.funnel)
}

/**
 * 获取行为分布数据
 */
export function fetchEventDistribution() {
  return mockRequest(conversionData.eventDistribution)
}

// ==================== Product API ====================

/**
 * 获取商品分析数据
 */
export function fetchProductData() {
  return mockRequest(productData)
}

/**
 * 获取品牌 TOP10 数据
 */
export function fetchBrandTop10() {
  return mockRequest(productData.brandTop10)
}

/**
 * 获取品类词云数据
 */
export function fetchCategoryWordCloud() {
  return mockRequest(productData.categoryWordCloud)
}

/**
 * 获取价格敏感度数据
 */
export function fetchPriceSensitivity() {
  return mockRequest(productData.priceSensitivity)
}

// ==================== UserInsight API ====================

/**
 * 获取用户洞察数据
 */
export function fetchUserInsightData() {
  return mockRequest(userInsightData)
}

/**
 * 获取用户分层数据
 */
export function fetchUserSegmentation() {
  return mockRequest(userInsightData.userSegmentation)
}

// ==================== Prediction API ====================

/**
 * 获取预测数据
 */
export function fetchPredictionData() {
  return mockRequest(predictionData)
}

/**
 * 获取历史数据
 */
export function fetchHistoricalData() {
  return mockRequest(predictionData.historical)
}

/**
 * 获取预测数据
 */
export function fetchForecastData() {
  return mockRequest(predictionData.forecast)
}

// ==================== 未来真实后端联调示例 ====================

/**
 * 未来联调真实后端时的示例代码（注释状态）
 * 
 * import axios from 'axios'
 * 
 * const request = axios.create({
 *   baseURL: '/api',
 *   timeout: 5000
 * })
 * 
 * export function fetchDashboardData() {
 *   return request.get('/dashboard')
 * }
 * 
 * export function fetchConversionData() {
 *   return request.get('/conversion')
 * }
 * 
 * // ... 其他接口
 */
