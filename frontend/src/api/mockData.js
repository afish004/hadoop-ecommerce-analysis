/**
 * src/api/mockData.js
 * 完整 Mock 数据源
 */

// 辅助函数：生成日期
function getDateRange(start, end) {
  const dates = []
  let dt = new Date(start)
  const endDate = new Date(end)
  while (dt <= endDate) {
    const y = dt.getFullYear()
    const m = String(dt.getMonth() + 1).padStart(2, '0')
    const d = String(dt.getDate()).padStart(2, '0')
    dates.push(`${y}-${m}-${d}`)
    dt.setDate(dt.getDate() + 1)
  }
  return dates
}

// ==================== 数仓运营大屏 ====================
export const dashboardData = {
  metrics: { gmv: 42580000, pv: 8580000, uv: 1250000 },
  
  // 热力图数据
  activityHeatmap: (function() {
    const data = []
    for (let i = 0; i < 24; i++) {
      for (let j = 0; j < 7; j++) {
        let value = Math.floor(Math.random() * 50)
        if (i > 18) value += 50
        if (j >= 5) value += 30
        data.push([i, j, value])
      }
    }
    return data
  })(),

  // 旭日图数据
  categorySales: [
    { name: 'Electronics.Smartphone', value: 14500000 },
    { name: 'Electronics.Laptop', value: 8500000 },
    { name: 'Electronics.Headphone', value: 3000000 },
    { name: 'Appliances.Kitchen', value: 6200000 },
    { name: 'Appliances.Cleaning', value: 2000000 },
    { name: 'Furniture.LivingRoom', value: 4200000 },
    { name: 'Furniture.Bedroom', value: 2100000 },
    { name: 'Apparel.Shoes', value: 1800000 },
    { name: 'Apparel.Clothing', value: 1000000 }
  ]
}
// 平滑面积折线图数据
export function generateDynamicTrend(startDateStr, endDateStr) {
  const dates = getDateRange(startDateStr, endDateStr)
  const pvData = dates.map(date => {
    const dt = new Date(date)
    const isWeekend = dt.getDay() === 0 || dt.getDay() === 6
    const isHoliday = date.includes('-10-0') && parseInt(date.split('-')[2]) <= 7
    let base = 50000 + Math.random() * 20000
    if (isWeekend) base += 15000
    if (isHoliday) base += 40000 
    return Math.floor(base)
  })
  const uvData = pvData.map(pv => Math.floor(pv * (0.2 + Math.random() * 0.1)))
  return {
    xAxis: dates,
    series: [
      { name: 'PV (浏览量)', data: pvData },
      { name: 'UV (访客数)', data: uvData }
    ]
  }
}

// ==================== 2. 用户行为数据 ====================
export const conversionData = {
  // 漏斗图数据
  funnel: [
    { name: '商品浏览 (View)', value: 1580000 },
    { name: '加入购物车 (Cart)', value: 450000 },
    { name: '生成订单 (Order)', value: 120000 },
    { name: '完成支付 (Pay)', value: 95000 }
  ],
  
//桑基图数据
  sankey: {
    nodes: [
      { name: '首页' },
      { name: '商品列表' },
      { name: '商品详情' },
      { name: '购物车' },
      { name: '支付页面' },
      { name: '支付成功' },
      { name: '流失' }
    ],
    links: [
      { source: '首页', target: '商品列表', value: 60000 },
      { source: '首页', target: '商品详情', value: 20000 },
      { source: '首页', target: '流失', value: 20000 },
      { source: '商品列表', target: '商品详情', value: 40000 },
      { source: '商品列表', target: '流失', value: 20000 },
      { source: '商品详情', target: '购物车', value: 30000 },
      { source: '商品详情', target: '流失', value: 30000 },
      { source: '购物车', target: '支付页面', value: 20000 },
      { source: '购物车', target: '流失', value: 10000 },
      { source: '支付页面', target: '支付成功', value: 18000 },
      { source: '支付页面', target: '流失', value: 2000 }
    ]
  }
}

// ==================== 3. 商品画像洞察 ====================
//横向柱状图数据
export const productData = {
  brandTop10: {
    brands: ['Apple', 'Xiaomi', 'Huawei', 'Samsung', 'Oppo', 'Vivo', 'Sony', 'LG', 'Lenovo', 'Asus'],
    sales: [45000, 42000, 38000, 35000, 28000, 25000, 18000, 15000, 12000, 9000]
  },
//词云图数据
  categoryWordCloud: [
    { name: 'Smartphone', value: 1000 },
    { name: 'Laptop', value: 850 },
    { name: 'Headphone', value: 700 },
    { name: 'Watch', value: 600 },
    { name: 'TV', value: 550 }
  ],
//散点图数据
  priceSensitivity: Array.from({ length: 50 }, () => 
    [Math.floor(Math.random() * 5000),
    Math.floor(Math.random() * 8000)])
}

// ==================== 4. 用户价值分层数据 ====================
//环形图数据
export const userInsightData = {
  userSegmentation: [
    { name: '高价值用户', value: 15800 },
    { name: '潜力用户', value: 25400 },
    { name: '重要唤留', value: 45200 },
    { name: '一般价值', value: 80100 },
    { name: '流失用户', value: 120000 }
  ]
}

// ==================== 5. 流量时序预测 ====================
//时序预测面积折线图
export const predictionData = {
  historical: {
    dates: ['10-25', '10-26', '10-27', '10-28', '10-29', '10-30', '10-31'],
    pv: [180000, 195000, 190000, 185000, 200000, 210000, 205000]
  },
  forecast: {
    dates: ['11-01', '11-02', '11-03', '11-04', '11-05', '11-06', '11-07'],
    pv: [215000, 220000, 218000, 225000, 230000, 240000, 235000],
    confidenceInterval: {
      upper: [225000, 230000, 228000, 235000, 245000, 255000, 250000],
      lower: [205000, 210000, 208000, 215000, 215000, 225000, 220000]
    }
  }
}