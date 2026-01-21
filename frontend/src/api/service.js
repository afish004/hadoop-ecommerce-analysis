// src/api/service.js

import {
  dashboardData,
  generateDynamicTrend, // 引入新写的函数
  conversionData,
  productData,
  userInsightData,
  predictionData
} from './mockData.js'

function mockRequest(data, delay = 200) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ code: 200, message: 'success', data: data })
    }, delay)
  })
}

// ==================== Dashboard API ====================

/**
 * 获取驾驶舱数据 (支持日期筛选)
 * @param {string} startDate - YYYY-MM-DD
 * @param {string} endDate - YYYY-MM-DD
 */
export function fetchDashboardData(startDate, endDate) {
  // 1. 获取基础数据
  const responseData = { ...dashboardData }
  
  // 2. 如果传了日期，动态生成这段时间的趋势图
  if (startDate && endDate) {
    const dynamicTrend = generateDynamicTrend(startDate, endDate)
    responseData.pvuvTrend = dynamicTrend // 覆盖原本的趋势数据
    
    // 简单模拟：根据天数动态计算总指标 (可选)
    // 这样选3天和选30天，上面的数字卡片数值会不一样，更真实
    const days = dynamicTrend.xAxis.length
    responseData.metrics = {
      gmv: Math.floor(days * 1500000 + Math.random() * 100000),
      pv: Math.floor(days * 300000 + Math.random() * 50000),
      uv: Math.floor(days * 50000 + Math.random() * 10000)
    }
  }
  
  return mockRequest(responseData)
}

// ... 其他原有接口保持不变，请复制之前的 Conversion, Product 等接口 ...
export function fetchConversionData() { return mockRequest(conversionData) }
export function fetchProductData() { return mockRequest(productData) }
export function fetchUserInsightData() { return mockRequest(userInsightData) }
export function fetchPredictionData() { return mockRequest(predictionData) }