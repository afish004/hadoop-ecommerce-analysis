<!--
  运营数据看板 - 反主流设计
  拒绝：专业术语、对称布局、冷冰冰的数据展示
  追求：口语化、不对称、有温度的数据故事
-->
<template>
  <div class="ops-dashboard-container">
    <!-- 页面头部：专业标题 -->
    <div class="page-header">
      <div>
        <h2 class="page-title">运营数据看板</h2>
        <p class="page-desc">实时监控核心业务指标与流量趋势</p>
      </div>
      
      <div class="header-actions">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          size="large"
          :shortcuts="shortcuts"
          @change="handleDateChange"
        />
        <el-button type="primary" :icon="Refresh" circle @click="loadData" style="margin-left: 12px" title="刷新数据" />
      </div>
    </div>
    
    <!-- 不对称 Bento Grid 布局：2fr 3fr (左窄右宽) -->
    <div class="bento-grid">
      <!-- 左侧：指标卡 + 热力图 -->
      <div class="side-area">
        <!-- 大号销售额卡片 - 更有个性的设计 -->
        <div class="metric-card-hero">
          <div class="metric-badge">
            <el-icon><Money /></el-icon>
          </div>
          <div class="metric-content">
            <div class="metric-label">区间总销售额 (GMV)</div>
            <div class="metric-value">{{ formatMoney(dashboardData.metrics.gmv) }}</div>
            <div class="metric-hint">实时数据监控</div>
          </div>
        </div>
        
        <!-- 两个小指标卡：专业表达 -->
        <div class="metrics-row">
          <div class="metric-card-small">
            <div class="metric-icon-small">
              <el-icon><View /></el-icon>
            </div>
            <div class="metric-label-small">区间总浏览量 (PV)</div>
            <div class="metric-value-small">{{ formatNumber(dashboardData.metrics.pv) }}</div>
          </div>
          
          <div class="metric-card-small">
            <div class="metric-icon-small">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="metric-label-small">区间独立访客 (UV)</div>
            <div class="metric-value-small">{{ formatNumber(dashboardData.metrics.uv) }}</div>
          </div>
        </div>
        
        <!-- 热力图 -->
        <div class="chart-card chart-heatmap">
          <div class="card-header-casual">
            <h3 class="chart-title-casual">用户活跃时段分布</h3>
            <span class="chart-subtitle">按小时/星期统计的活跃度热力图</span>
          </div>
          <HeatmapChart :data="dashboardData.activityHeatmap" height="280px" />
        </div>
      </div>
      
      <!-- 右侧：流量趋势图 + 数据统计栏 -->
      <div class="right-area">
        <!-- 流量趋势图 -->
        <div class="chart-card chart-main">
          <div class="card-header-casual">
            <h3 class="chart-title-casual">PV/UV 流量趋势</h3>
            <span class="chart-subtitle">按日期统计的访问量变化</span>
          </div>
          <LineChart :key="chartKey" :data="pvuvTrendData" :loading="loading" height="420px" />
        </div>
        
        <!-- 数据统计栏 -->
        <div class="chart-card chart-summary">
          <div class="summary-item">
            <div class="icon-wrapper peak">
              <el-icon><Top /></el-icon>
            </div>
            <div class="text-group">
              <span class="label">本月流量峰值 (Peak)</span>
              <div class="value-row">
                <span class="value">{{ formatNumber(maxPV) }}</span>
                <span class="sub">于 {{ maxPVDate }}</span>
              </div>
            </div>
          </div>
          
          <div class="divider"></div>
          
          <div class="summary-item">
            <div class="icon-wrapper avg">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="text-group">
              <span class="label">日均访问量 (Avg)</span>
              <div class="value-row">
                <span class="value">{{ formatNumber(avgPV) }}</span>
                <span class="sub">/ 天</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, onMounted, computed } from 'vue'
import { fetchDashboardData } from '@/api/service'
import { Refresh, Money, View, UserFilled, Top, DataLine } from '@element-plus/icons-vue'
import LineChart from '@/components/LineChart.vue'
import HeatmapChart from '@/components/HeatmapChart.vue'

// ==================== 响应式状态 ====================

/**
 * 加载状态
 * 用于控制图表的 loading 效果
 */
const loading = ref(true)

/**
 * 图表刷新键
 * 每次数据更新时递增，强制 LineChart 组件重新渲染
 * 解决日期范围变化时图表不更新的问题
 */
const chartKey = ref(0)

/**
 * Dashboard 核心数据
 * 
 * @property {Object} metrics - 核心业务指标
 * @property {number} metrics.gmv - 总销售额（Gross Merchandise Volume）
 * @property {number} metrics.pv - 总浏览量（Page View）
 * @property {number} metrics.uv - 独立访客数（Unique Visitor）
 * 
 * @property {Object} pvuvTrend - PV/UV 趋势数据
 * @property {string[]} pvuvTrend.xAxis - 日期数组
 * @property {Array} pvuvTrend.series - 系列数据（PV 和 UV）
 * 
 * @property {Array<[number, number, number]>} activityHeatmap - 活跃度热力图数据
 *   格式：[小时, 星期, 活跃度值]
 */
const dashboardData = ref({
  metrics: { gmv: 0, pv: 0, uv: 0 },
  pvuvTrend: {},
  activityHeatmap: []
})

/**
 * 趋势图数据（用于 LineChart 组件）
 * 从 dashboardData.pvuvTrend 中提取并格式化
 */
const pvuvTrendData = ref({})

// ==================== 数据统计计算 ====================

/**
 * 计算流量峰值（最大 PV 值）
 * 从 pvuvTrendData 的 PV 系列中找出最大值
 */
const maxPV = computed(() => {
  if (!pvuvTrendData.value.series || pvuvTrendData.value.series.length === 0) return 0
  const pvSeries = pvuvTrendData.value.series.find(s => s.name.includes('PV'))
  if (!pvSeries || !pvSeries.data) return 0
  return Math.max(...pvSeries.data)
})

/**
 * 计算峰值出现的日期
 * 找到最大 PV 值对应的日期，格式化为 MM-DD
 */
const maxPVDate = computed(() => {
  if (!pvuvTrendData.value.series || pvuvTrendData.value.series.length === 0) return '-'
  const pvSeries = pvuvTrendData.value.series.find(s => s.name.includes('PV'))
  if (!pvSeries || !pvSeries.data || !pvuvTrendData.value.xAxis) return '-'
  
  const maxValue = Math.max(...pvSeries.data)
  const maxIndex = pvSeries.data.indexOf(maxValue)
  const fullDate = pvuvTrendData.value.xAxis[maxIndex]
  
  // 格式化为 MM-DD（如 "10-15"）
  if (fullDate) {
    const parts = fullDate.split('-')
    return `${parts[1]}-${parts[2]}`
  }
  return '-'
})

/**
 * 计算日均访问量（平均 PV 值）
 * 对 PV 系列数据求平均值
 */
const avgPV = computed(() => {
  if (!pvuvTrendData.value.series || pvuvTrendData.value.series.length === 0) return 0
  const pvSeries = pvuvTrendData.value.series.find(s => s.name.includes('PV'))
  if (!pvSeries || !pvSeries.data || pvSeries.data.length === 0) return 0
  
  const sum = pvSeries.data.reduce((acc, val) => acc + val, 0)
  return Math.floor(sum / pvSeries.data.length)
})

// ==================== 日期筛选配置 ====================

/**
 * 默认日期范围：2019年10月（毕业设计数据集时间范围）
 */
const defaultStartDate = new Date('2019-10-01')
const defaultEndDate = new Date('2019-10-31')
const dateRange = ref([defaultStartDate, defaultEndDate])

/**
 * 日期选择器快捷选项 - 口语化表达
 * 
 * 功能说明：
 * - 提供常用时间范围的快速选择
 * - 使用口语化文案，降低用户理解成本
 * - 支持动态计算（如"最近一周"）
 * 
 * 快捷选项列表：
 * 1. 整个10月：完整数据集时间范围（2019-10-01 至 2019-10-31）
 * 2. 国庆7天：国庆黄金周（2019-10-01 至 2019-10-07）
 * 3. 最近一周：动态计算最近7天（当前日期往前推7天）
 */
const shortcuts = [
  { text: '2019年10月(全量)', value: [new Date('2019-10-01'), new Date('2019-10-31')] },
  { text: '国庆黄金周', value: [new Date('2019-10-01'), new Date('2019-10-07')] },
  { 
    text: '最近7天(模拟)', 
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  }
]

// ==================== 工具函数 ====================

/**
 * 格式化金额：智能显示万/亿（口语化）
 * 
 * 功能说明：
 * - 自动判断数值大小，选择合适的单位
 * - 亿级：保留1位小数 + "亿"
 * - 万级：保留1位小数 + "万"
 * - 其他：千分位格式化
 * 
 * @param {number} num - 原始金额数值
 * @returns {string} 格式化后的金额字符串，如 "12.5万"、"3.2亿"
 * 
 * @example
 * formatMoney(150000000) // "1.5亿"
 * formatMoney(25000) // "2.5万"
 * formatMoney(1234) // "1,234"
 */
const formatMoney = (num) => {
  if (num >= 100000000) {
    return `${(num / 100000000).toFixed(1)}亿`
  } else if (num >= 10000) {
    return `${(num / 10000).toFixed(1)}万`
  }
  return num.toLocaleString()
}

/**
 * 格式化数字：智能显示万/亿（口语化）
 * 
 * 功能说明：
 * - 与 formatMoney 类似，但万级不保留小数
 * - 适用于浏览量、访客数等整数指标
 * 
 * @param {number} num - 原始数值
 * @returns {string} 格式化后的数字字符串，如 "12万"、"3.2亿"
 * 
 * @example
 * formatNumber(150000000) // "1.5亿"
 * formatNumber(25000) // "25万"（不保留小数）
 * formatNumber(1234) // "1,234"
 */
const formatNumber = (num) => {
  if (num >= 100000000) {
    return `${(num / 100000000).toFixed(1)}亿`
  } else if (num >= 10000) {
    return `${(num / 10000).toFixed(0)}万`
  }
  return num.toLocaleString()
}

/**
 * 格式化日期为 YYYY-MM-DD 格式
 * 
 * @param {Date} date - 日期对象
 * @returns {string} 格式化后的日期字符串，如 '2019-10-15'
 * 
 * @example
 * formatDate(new Date('2019-10-15')) // '2019-10-15'
 */
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// ==================== 数据加载 ====================

/**
 * 加载 Dashboard 数据
 * 
 * 功能说明：
 * 1. 根据选中的日期范围调用 API 获取数据
 * 2. 更新核心指标、趋势图、热力图数据
 * 3. 强制刷新 LineChart 组件（通过 chartKey）
 * 
 * 数据来源：
 * - 当前使用 Mock 数据（frontend/src/api/mockData.js）
 * - 支持动态日期范围筛选
 * - 未来可对接真实后端 API
 * 
 * @async
 * @throws {Error} 当 API 请求失败时抛出错误
 */
const loadData = async () => {
  loading.value = true
  try {
    // 格式化日期参数
    const startStr = formatDate(dateRange.value[0])
    const endStr = formatDate(dateRange.value[1])
    
    // 调用 API 获取数据
    const res = await fetchDashboardData(startStr, endStr)
    dashboardData.value = res.data
    
    // 提取趋势图数据（LineChart 组件需要的格式）
    pvuvTrendData.value = {
      xAxis: res.data.pvuvTrend.xAxis,
      series: res.data.pvuvTrend.series
    }
    
    // 强制刷新图表组件
    chartKey.value++
  } catch (error) {
    console.error('Dashboard 数据加载失败:', error)
  } finally {
    // 延迟 500ms 关闭 loading，提升用户体验
    setTimeout(() => { loading.value = false }, 500)
  }
}

/**
 * 日期范围变化处理函数
 * 当用户选择新的日期范围时，重新加载数据
 */
const handleDateChange = () => {
  if (dateRange.value) loadData()
}

// ==================== 生命周期 ====================

/**
 * 组件挂载时自动加载数据
 */
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.ops-dashboard-container {
  position: relative;
  
  // ============================================
  // 背景装饰：有机的光晕（不是规整的点阵）
  // ============================================
  &::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(232, 93, 61, 0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(60px);
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: -100px;
    left: -100px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(45, 159, 110, 0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(80px);
  }
  
  // 确保内容在装饰层之上
  > * {
    position: relative;
    z-index: 1;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    
    .page-title { 
      font-size: 32px; 
      font-weight: 700; 
      color: $text-primary; 
      margin-bottom: 6px;
      letter-spacing: -0.5px; // 紧凑一点，更有个性
    }
    
    .page-desc { 
      font-size: 15px; 
      color: $text-secondary;
      font-weight: 500;
    }
  }

  // ============================================
  // 不对称 Bento Grid 布局：2fr 3fr (左窄右宽)
  // 
  // 布局说明：
  // - 左侧（2fr）：指标卡 + 热力图，占据较窄空间
  // - 右侧（3fr）：流量趋势图 + 数据统计栏，占据较宽空间
  // 
  // 设计理念：
  // - 打破传统对称布局，增强视觉张力
  // - 趋势图需要更宽的空间展示数据变化
  // - 指标卡紧凑排列，快速浏览核心数据
  // 
  // 版本历史：
  // - v4.7：右侧新增数据统计栏
  // - v4.4：从 3fr 2fr 调整为 2fr 3fr（左窄右宽）
  // - v4.0-v4.3：使用 3fr 2fr（左宽右窄）
  // ============================================
  .bento-grid {
    display: grid;
    grid-template-columns: 2fr 3fr;
    gap: 20px; // 稍微大一点的间距
    
    .side-area {
      grid-column: 1;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    
    .right-area {
      grid-column: 2;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    
    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
      
      .side-area,
      .right-area {
        grid-column: 1;
      }
    }
  }
  
  // ============================================
  // 大号销售额卡片 - Hero 风格（更有个性）
  // ============================================
  .metric-card-hero {
    background: $gradient-card;
    border: 1.5px solid $border-color;
    border-radius: 20px;          // 更圆润的边角
    padding: 32px;                // 更宽松的内边距
    box-shadow: $shadow-md;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);  // 弹性动画
    
    // 背景装饰：更大的光晕
    &::before {
      content: '';
      position: absolute;
      top: -60%;
      right: -30%;
      width: 250px;
      height: 250px;
      background: radial-gradient(circle, rgba(232, 93, 61, 0.15) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
      filter: blur(40px);
    }
    
    &:hover {
      transform: rotate(-1.5deg) scale(1.03);  // 更夸张的旋转和缩放
      box-shadow: $shadow-lg;
      border-color: rgba(232, 93, 61, 0.4);
    }
    
    .metric-badge {
      width: 80px;
      height: 80px;
      border-radius: 20px;
      background: rgba(232, 93, 61, 0.1);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 16px;
      animation: float 3s ease-in-out infinite;
      box-shadow: 0 4px 12px rgba(232, 93, 61, 0.15);
      
      .el-icon {
        font-size: 40px;
        color: #E85D3D;
      }
    }
    
    .metric-content {
      position: relative;
      z-index: 1;
      
      .metric-label {
        font-size: 15px;
        color: $text-secondary;
        margin-bottom: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
      }
      
      .metric-value {
        font-size: 40px;          // 更大的数值
        font-weight: 900;         // 更粗的字重
        color: $primary-color;
        margin-bottom: 8px;
        letter-spacing: -1.5px;
        text-shadow: 0 2px 4px rgba(232, 93, 61, 0.1);  // 文字阴影
      }
      
      .metric-hint {
        font-size: 13px;
        color: $text-muted;
        font-style: italic;
        font-weight: 500;
      }
    }
  }
  
  // ============================================
  // 小指标卡：更有个性的设计
  // ============================================
  .metrics-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  .metric-card-small {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 16px;
    padding: 24px;
    box-shadow: $shadow-sm;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    text-align: center;
    position: relative;
    overflow: hidden;
    
    // 背景装饰
    &::before {
      content: '';
      position: absolute;
      top: -50%;
      left: 50%;
      transform: translateX(-50%);
      width: 120px;
      height: 120px;
      background: radial-gradient(circle, rgba(232, 160, 61, 0.08) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
      filter: blur(30px);
    }
    
    &:hover {
      transform: translateY(-6px) rotate(1.5deg);  // 更夸张的悬停效果
      box-shadow: $shadow-md;
      border-color: rgba(232, 93, 61, 0.25);
    }
    
    .metric-icon-small {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: rgba(232, 93, 61, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 12px;
      position: relative;
      z-index: 1;
      
      .el-icon {
        font-size: 24px;
        color: #E85D3D;
      }
    }
    
    .metric-label-small {
      font-size: 13px;
      color: $text-secondary;
      margin-bottom: 10px;
      font-weight: 600;
      letter-spacing: 0.3px;
      position: relative;
      z-index: 1;
    }
    
    .metric-value-small {
      font-size: 26px;            // 更大的数值
      font-weight: 800;
      color: $text-primary;
      letter-spacing: -0.8px;
      position: relative;
      z-index: 1;
    }
  }
  
  // 热力图卡片
  .chart-heatmap {
    flex: 1;
    min-height: 0;
  }
  
  // ============================================
  // 数据统计栏 - 极简设计
  // ============================================
  .chart-summary {
    height: 100px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    background: #F8FAFC !important;
    border: 1px solid rgba(0, 0, 0, 0.04) !important;
    box-shadow: none !important;
    
    &:hover {
      transform: none;
      box-shadow: none !important;
      border-color: rgba(0, 0, 0, 0.04) !important;
    }
    
    .summary-item {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
    }
    
    .divider {
      width: 1px;
      height: 40px;
      background: rgba(0, 0, 0, 0.06);
    }
    
    .icon-wrapper {
      width: 42px;
      height: 42px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
      
      &.peak {
        background: rgba(232, 93, 61, 0.08);
        color: #E85D3D;
      }
      
      &.avg {
        background: rgba(37, 99, 235, 0.08);
        color: #2563EB;
      }
    }
    
    .text-group {
      display: flex;
      flex-direction: column;
      gap: 2px;
      
      .label {
        font-size: 15px;
        color: $text-secondary;
        margin-bottom: 2px;
        font-weight: 600;
      }
      
      .value-row {
        display: flex;
        align-items: baseline;
        gap: 6px;
        
        .value {
          font-family: 'DIN Alternate', -apple-system, BlinkMacSystemFont, sans-serif;
          font-size: 22px;
          font-weight: 700;
          color: #1E293B;
          letter-spacing: -0.5px;
        }
        
        .sub {
          font-size: 12px;
          color: #CBD5E1;
          font-weight: 500;
        }
      }
    }
  }

  // ============================================
  // 卡片样式 - 反主流设计
  // ============================================
  .chart-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 16px;
    padding: 24px;
    box-shadow: $shadow-sm;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    
    &:hover {
      transform: rotate(-0.3deg) scale(1.005);
      box-shadow: $shadow-md;
      border-color: rgba(232, 93, 61, 0.15);
    }
  }
  
  // ============================================
  // 口语化的卡片标题
  // ============================================
  .card-header-casual {
    margin-bottom: 20px;
    
    .chart-title-casual {
      font-size: 18px;
      font-weight: 700;
      color: $text-primary;
      margin-bottom: 4px;
      letter-spacing: -0.3px;
    }
    
    .chart-subtitle {
      font-size: 13px;
      color: $text-muted;
      font-weight: 500;
    }
  }
}

// ============================================
// 浮动动画
// ============================================
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}
</style>
