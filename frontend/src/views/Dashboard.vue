<!--
  Dashboard 数仓运营大屏
  功能：展示电商核心指标、流量趋势、用户活跃度热力图、品类销售占比（旭日图）
  支持日期范围筛选，动态加载数据
  
  本次更新：
  - 页面标题从"电商用户行为分析系统"改为"数仓运营大屏"，突出数据仓库概念
  - 新增副标题"基于 Hadoop 数仓的全域数据监控与分析"
  - 将饼图（PieChart）替换为旭日图（SunburstChart），支持多层级数据展示
  - 优化图表标题，更清晰地说明图表类型和用途
-->
<template>
  <div class="dashboard-container">
    <!-- 页面头部：标题 + 日期筛选 + 刷新按钮 -->
    <div class="page-header">
      <div>
        <h2 class="page-title">数仓运营大屏</h2>
        <p class="page-desc">基于 Hadoop 数仓的全域数据监控与分析</p>
      </div>
      
      <div class="header-actions">
        <!-- 日期范围选择器 -->
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
        <!-- 刷新按钮 -->
        <el-button type="primary" :icon="Refresh" circle @click="loadData" style="margin-left: 12px" title="刷新数据" />
      </div>
    </div>
    
    <!-- 核心指标卡片行：GMV、PV、UV -->
    <el-row :gutter="20" class="metrics-row">
      <el-col :xs="24" :sm="8">
        <MetricCard title="区间总销售额 (GMV)" :value="dashboardData.metrics.gmv" unit="元" icon="TrendCharts" icon-bg="linear-gradient(135deg, #1890ff 0%, #096dd9 100%)" />
      </el-col>
      <el-col :xs="24" :sm="8">
        <MetricCard title="区间总浏览量 (PV)" :value="dashboardData.metrics.pv" unit="次" icon="View" icon-bg="linear-gradient(135deg, #52c41a 0%, #389e0d 100%)" />
      </el-col>
      <el-col :xs="24" :sm="8">
        <MetricCard title="区间独立访客 (UV)" :value="dashboardData.metrics.uv" unit="人" icon="User" icon-bg="linear-gradient(135deg, #faad14 0%, #d48806 100%)" />
      </el-col>
    </el-row>
    
    <!-- 图表行 1：热力图 + 旭日图 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 用户活跃时段热力图 -->
      <el-col :xs="24" :lg="14">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">用户活跃时段分布</h3>
          </div>
          <HeatmapChart :data="dashboardData.activityHeatmap" height="350px" />
        </div>
      </el-col>
      
      <!-- 热门品类旭日图（多层级环形图） -->
      <el-col :xs="24" :lg="10">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">热门品类分布 (旭日图)</h3>
            <span class="chart-subtitle">多层级环形占比分析</span>
          </div>
          
          <!-- 使用旭日图展示层级数据（如 Electronics.Smartphone） -->
          <SunburstChart :data="dashboardData.categorySales" height="350px" />
          
        </div>
      </el-col>
    </el-row>
    
    <!-- 图表行 2：流量趋势折线图 -->
    <el-row class="charts-row" style="margin-top: 20px;">
      <el-col :span="24">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">流量波动趋势</h3>
            <span class="chart-subtitle">
              {{ formatDate(dateRange[0]) }} 至 {{ formatDate(dateRange[1]) }} 流量变化
            </span>
          </div>
          <!-- 使用 key 强制刷新图表，确保日期变化时图表重新渲染 -->
          <LineChart :key="chartKey" :data="pvuvTrendData" :loading="loading" height="380px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchDashboardData } from '@/api/service'
import { Refresh } from '@element-plus/icons-vue'
import MetricCard from '@/components/MetricCard.vue'
import LineChart from '@/components/LineChart.vue'
import HeatmapChart from '@/components/HeatmapChart.vue'

// ==================== 组件导入 ====================
// 【关键】引入旭日图组件，用于展示多层级品类数据
import SunburstChart from '@/components/SunburstChart.vue'
// 注意：已将 PieChart 替换为 SunburstChart，不再使用饼图

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
 * @property {Array<{name: string, value: number}>} categorySales - 品类销售数据
 *   格式：[{ name: 'Electronics.Smartphone', value: 14500000 }, ...]
 *   支持多层级结构（用点号分隔），适配旭日图展示
 * 
 * @property {Array<[number, number, number]>} activityHeatmap - 活跃度热力图数据
 *   格式：[小时, 星期, 活跃度值]
 */
const dashboardData = ref({
  metrics: { gmv: 0, pv: 0, uv: 0 },
  pvuvTrend: {},
  categorySales: [],
  activityHeatmap: []
})

/**
 * 趋势图数据（用于 LineChart 组件）
 * 从 dashboardData.pvuvTrend 中提取并格式化
 */
const pvuvTrendData = ref({}) 

// ==================== 日期筛选配置 ====================

/**
 * 默认日期范围：2019年10月（毕业设计数据集时间范围）
 */
const defaultStartDate = new Date('2019-10-01')
const defaultEndDate = new Date('2019-10-31')
const dateRange = ref([defaultStartDate, defaultEndDate])

/**
 * 日期选择器快捷选项
 * 提供常用时间范围的快速选择
 */
const shortcuts = [
  { text: '2019年10月(全量)', value: [new Date('2019-10-01'), new Date('2019-10-31')] },
  { text: '国庆黄金周', value: [new Date('2019-10-01'), new Date('2019-10-07')] },
  { text: '最近7天(模拟)', value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  }
]

// ==================== 工具函数 ====================

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
 * 2. 更新核心指标、趋势图、热力图、品类销售数据
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

.dashboard-container {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .page-title { font-size: 24px; font-weight: 600; color: $text-primary; margin-bottom: 4px; }
    .page-desc { font-size: 14px; color: $text-muted; }
  }

  .metrics-row { margin-bottom: 20px; }
  .charts-row { margin-bottom: 20px; }
  .el-col { margin-bottom: 20px; }

  .chart-card {
    background: $bg-card;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    height: 100%;
    
    .card-header {
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      div, .card-header {
        .chart-title { font-size: 16px; font-weight: 600; color: $text-primary; margin-bottom: 4px; }
        .chart-subtitle { font-size: 13px; color: $text-muted; }
      }
    }
  }
}
</style>