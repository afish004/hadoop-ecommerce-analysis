// src/api/service.js
// 真实后端API调用（替换Mock数据）

import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理响应
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 如果401未授权，清除token并跳转登录
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('currentUser')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ==================== 认证 API ====================

/**
 * 用户注册
 * @param {Object} userData - {username, email, password}
 */
export function register(userData) {
  return api.post('/auth/register', userData)
}

/**
 * 用户登录
 * @param {Object} userData - {username, password}
 */
export function login(userData) {
  return api.post('/auth/login', userData)
}

// ==================== Dashboard API ====================

/**
 * 获取驾驶舱数据 (支持日期筛选)
 * @param {string} startDate - YYYY-MM-DD
 * @param {string} endDate - YYYY-MM-DD
 */
export function fetchDashboardData(startDate, endDate) {
  const params = {}
  if (startDate) params.start_date = startDate
  if (endDate) params.end_date = endDate
  return api.get('/data/dashboard', { params })
}

/**
 * 获取转化数据
 */
export function fetchConversionData() {
  return api.get('/data/conversion')
}

/**
 * 获取商品数据
 */
export function fetchProductData() {
  return api.get('/data/product')
}

/**
 * 获取用户洞察数据
 */
export function fetchUserInsightData() {
  return api.get('/data/user-insight')
}

/**
 * 获取预测数据
 */
export function fetchPredictionData() {
  return api.get('/data/prediction')
}