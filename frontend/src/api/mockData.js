// Mock 数据生成工具函数

// 模拟品牌列表
const BRANDS = ['xiaomi', 'apple', 'samsung', 'huawei', 'oppo', 'vivo', 'lenovo', 'asus', 'dell', 'hp']

// 模拟品类代码
const CATEGORIES = [
  'electronics.smartphone',
  'electronics.tablet',
  'computers.notebook',
  'computers.desktop',
  'appliances.kitchen',
  'appliances.climate',
  'accessories.headphone',
  'accessories.case'
]

// 行为类型
const EVENT_TYPES = ['view', 'cart', 'purchase', 'remove_from_cart']

// 生成时间标签（24小时）
export function generateHourLabels() {
  return Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`)
}

// 生成日期标签
export function generateDateLabels(startOffset, endOffset) {
  const dates = []
  const today = new Date()
  
  for (let i = startOffset; i <= endOffset; i++) {
    const date = new Date(today)
    date.setDate(date.getDate() + i)
    dates.push(date.toISOString().split('T')[0])
  }
  
  return dates
}

// 生成趋势数据（带随机波动）
export function generateTrendData(count, min, max) {
  return Array.from({ length: count }, () => 
    Math.floor(Math.random() * (max - min + 1)) + min
  )
}

// ==================== Dashboard 数据 ====================

export const dashboardData = {
  // 核心指标
  metrics: {
    gmv: 12580000,      // 总销售额（元）
    pv: 1580000,        // 总访问量
    uv: 350000          // 独立访客数
  },
  
  // 24小时 PV/UV 趋势
  pvuvTrend: {
    xAxis: generateHourLabels(),
    series: [
      {
        name: 'PV',
        data: generateTrendData(24, 50000, 80000)
      },
      {
        name: 'UV',
        data: generateTrendData(24, 10000, 20000)
      }
    ]
  },
  
  // 分类销售占比
  categorySales: [
    { name: 'electronics.smartphone', value: 4500000 },
    { name: 'computers.notebook', value: 3200000 },
    { name: 'appliances.kitchen', value: 2800000 },
    { name: 'electronics.tablet', value: 1200000 },
    { name: 'accessories.headphone', value: 880000 }
  ]
}

// ==================== Conversion 数据 ====================

export const conversionData = {
  // 漏斗图数据（必须递减）
  funnel: [
    { name: '浏览', value: 1000000 },
    { name: '加购', value: 300000 },
    { name: '下单', value: 100000 }
  ],
  
  // 行为分布（玫瑰图）
  eventDistribution: [
    { name: '浏览 (view)', value: 1000000 },
    { name: '加购 (cart)', value: 300000 },
    { name: '下单 (purchase)', value: 100000 },
    { name: '移除 (remove)', value: 50000 }
  ]
}

// ==================== Product 数据 ====================

export const productData = {
  // 品牌销量 TOP10
  brandTop10: {
    brands: ['xiaomi', 'apple', 'samsung', 'huawei', 'oppo', 'vivo', 'lenovo', 'asus', 'dell', 'hp'],
    sales: [50000, 48000, 45000, 42000, 38000, 35000, 32000, 28000, 25000, 22000]
  },
  
  // 品类词云数据
  categoryWordCloud: [
    { name: 'smartphone', value: 1000 },
    { name: 'laptop', value: 800 },
    { name: 'tablet', value: 600 },
    { name: 'headphone', value: 500 },
    { name: 'kitchen', value: 450 },
    { name: 'desktop', value: 400 },
    { name: 'climate', value: 350 },
    { name: 'case', value: 300 }
  ],
  
  // 价格敏感度分析（散点图数据）
  priceSensitivity: Array.from({ length: 100 }, () => [
    Math.random() * 5000 + 100,           // 价格 100-5100
    Math.floor(Math.random() * 10000)     // 销量 0-10000
  ])
}

// ==================== UserInsight 数据 ====================

export const userInsightData = {
  // RFM 用户分层
  userSegmentation: [
    { name: '高价值用户', value: 15000 },
    { name: '潜力用户', value: 50000 },
    { name: '挽留用户', value: 80000 },
    { name: '流失用户', value: 205000 }
  ]
}

// ==================== Prediction 数据 ====================

export const predictionData = {
  // 历史数据（过去30天）
  historical: {
    dates: generateDateLabels(-30, 0),
    pv: generateTrendData(31, 50000, 80000)
  },
  
  // 预测数据（未来7天）
  forecast: {
    dates: generateDateLabels(1, 7),
    pv: generateTrendData(7, 55000, 85000),
    // 95% 置信区间
    confidenceInterval: {
      upper: generateTrendData(7, 60000, 90000),
      lower: generateTrendData(7, 50000, 80000)
    }
  }
}
