<template>
  <div class="chart-wrapper" style="position: relative; width: 100%;" :style="{ height }">
    <div v-if="loading" class="loading-mask">
      <el-icon class="is-loading" :size="24"><Loading /></el-icon>
      <div style="margin-top: 8px">数据计算中...</div>
    </div>

    <el-empty 
      v-else-if="isEmpty" 
      description="该时间段暂无数据" 
      :image-size="80"
      style="height: 100%;" 
    />

    <div 
      v-else 
      ref="chartRef" 
      :style="{ height, width: '100%' }"
    ></div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { Loading } from '@element-plus/icons-vue'

// ==================== Props 定义 ====================
/**
 * 组件属性
 * @property {Object} data - 图表数据对象
 * @property {Array} data.xAxis - X 轴数据（日期、时间等）
 * @property {Array} data.series - 系列数据数组
 * @property {String} data.series[].name - 系列名称（如 "PV"、"UV"）
 * @property {Array} data.series[].data - 系列数值数组
 * @property {String} height - 图表高度（默认 400px）
 * @property {Boolean} loading - 加载状态（默认 false）
 */
const props = defineProps({
  data: Object,
  height: { type: String, default: '400px' },
  loading: { type: Boolean, default: false }
})

// ==================== 响应式数据 ====================
/**
 * 图表 DOM 引用
 * 用于初始化 ECharts 实例
 */
const chartRef = ref(null)

/**
 * ECharts 实例
 * 用于渲染和更新图表
 */
let chartInstance = null

// ==================== 计算属性 ====================
/**
 * 判断数据是否为空
 * @returns {Boolean} 数据为空返回 true，否则返回 false
 * 
 * 检查逻辑：
 * 1. data 对象不存在
 * 2. series 数组为空
 * 3. 所有 series 的 data 都为空
 */
const isEmpty = computed(() => {
  if (!props.data) return true
  if (props.data.series && props.data.series.length === 0) return true
  // 检查所有 series 的 data 是否都有值
  if (props.data.series && props.data.series.every(s => !s.data || s.data.length === 0)) return true
  return false
})

// ==================== 图表初始化 ====================
/**
 * 初始化图表
 * 创建 ECharts 实例并绑定窗口 resize 事件
 */
const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', handleResize)
}

// ==================== 图表更新 ====================
/**
 * 更新图表配置
 * 根据 props.data 动态生成折线图配置
 * 支持智能配色：预测数据场景和普通折线图场景
 */
const updateChart = () => {
  if (!chartInstance || isEmpty.value) return
  
  /**
   * 获取系列颜色
   * 根据系列名称智能分配颜色，支持两种场景：
   * 1. 预测数据场景：历史数据（蓝色）、预测数据（绿色）、置信区间（金黄色）
   * 2. 普通折线图场景：使用大地色系调色板
   * 
   * @param {String} seriesName - 系列名称（如 "历史数据"、"预测数据"、"PV"、"UV"）
   * @param {Number} index - 系列索引（用于默认配色）
   * @returns {String} 颜色值（HEX 格式）
   * 
   * @example
   * getSeriesColor('历史数据', 0) // 返回 '#3D8FE8'（蓝色）
   * getSeriesColor('预测数据', 1) // 返回 '#2D9F6E'（绿色）
   * getSeriesColor('PV', 0) // 返回 '#E85D3D'（橙色）
   */
  const getSeriesColor = (seriesName, index) => {
    // 预测数据场景的颜色映射
    const colorMap = {
      '历史数据': '#3D8FE8',      // 蓝色 - 表示已发生的真实数据
      '预测数据': '#2D9F6E',      // 绿色 - 表示未来的预测趋势
      '置信区间上界': '#FA8C16',  // 橙色 - 表示预测的上限范围（更鲜艳）
      '置信区间下界': '#FA8C16',  // 橙色 - 表示预测的下限范围（更鲜艳）
      'PV': '#E85D3D',            // 红色 - 页面浏览量（暖色调）
      'PV (浏览量)': '#E85D3D',   // 红色 - 页面浏览量（完整名称）
      'UV': '#2D9F6E',            // 绿色 - 独立访客（冷色调）
      'UV (访客数)': '#2D9F6E'    // 绿色 - 独立访客（完整名称）
    }
    
    // 如果系列名称匹配预测数据场景，使用映射颜色
    if (colorMap[seriesName]) {
      return colorMap[seriesName]
    }
    
    // 默认大地色系调色板（用于普通折线图）
    // 顺序：珊瑚橙 → 金黄色 → 森林绿 → 天空蓝 → 棕灰色 → 深橙红
    const defaultColors = ['#E85D3D', '#E8A03D', '#2D9F6E', '#3D8FE8', '#6B6560', '#D14B2E']
    return defaultColors[index % defaultColors.length]
  }
  
  // ==================== ECharts 配置对象 ====================
  const option = {
    // ==================== 提示框配置 ====================
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: 'rgba(232, 93, 61, 0.3)',
          width: 2
        }
      }
    },
    // 图例配置
    legend: { 
      bottom: 0,                          // 图例位置：底部
      textStyle: { color: '#606266' }     // 图例文字颜色
    },
    // 网格配置（图表绘图区域）
    grid: { left: '3%', right: '4%', bottom: '10%', top: '10%', containLabel: true },
    // X 轴配置
    xAxis: {
      type: 'category',                   // 类目轴（用于日期、时间等）
      boundaryGap: false,                 // 坐标轴两边不留白
      data: props.data.xAxis || [],       // X 轴数据
      axisLine: { lineStyle: { color: '#e4e7ed' } }
    },
    // Y 轴配置
    yAxis: {
      type: 'value',                      // 数值轴
      splitLine: { lineStyle: { type: 'dashed', color: '#e4e7ed' } }
    },
    // 系列配置（折线图数据）
    series: props.data.series.map((item, index) => {
      const seriesColor = getSeriesColor(item.name, index)
      const isConfidenceInterval = item.name && item.name.includes('置信区间')
      
      return {
        ...item,                          // 保留原有配置（如 name、data）
        type: 'line',                     // 图表类型：折线图
        smooth: true,                     // 平滑曲线
        symbol: 'none',                   // 不显示数据点标记
        // 线条样式配置
        lineStyle: {
          ...item.lineStyle,              // 保留原有的 lineStyle（如 type: 'dashed'）
          width: isConfidenceInterval ? 2 : (item.lineStyle?.width || 3),  // 置信区间线条稍细（2px）
          color: seriesColor,             // 线条颜色（智能分配）
          opacity: isConfidenceInterval ? 0.6 : 1  // 置信区间线条透明度提高到 0.6
        },
        // 数据点样式配置
        itemStyle: {
          color: seriesColor              // 数据点颜色与线条一致
        },
        // 区域填充样式配置（可选）
        areaStyle: item.areaStyle ? {
          opacity: isConfidenceInterval ? 0.15 : 0.2,  // 置信区间阴影透明度提高到 0.15
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: seriesColor },           // 顶部颜色
            { offset: 1, color: 'rgba(255,255,255,0)' }  // 底部透明
          ])
        } : undefined
      }
    })
  }
  chartInstance.setOption(option, true)
}

// ==================== 窗口大小调整处理 ====================
/**
 * 处理窗口大小变化
 * 当浏览器窗口大小改变时，自动调整图表尺寸
 */
const handleResize = () => chartInstance?.resize()

// ==================== 生命周期钩子 ====================
/**
 * 监听数据变化
 * 当 props.data 或 props.loading 变化时，重新渲染图表
 */
watch(() => [props.data, props.loading], async () => {
  await nextTick()
  if (!chartInstance && chartRef.value) initChart()
  else updateChart()
}, { deep: true })

/**
 * 组件挂载时初始化图表
 */
onMounted(async () => {
  await nextTick()
  initChart()
})

/**
 * 组件卸载时销毁图表实例
 * 释放内存，避免内存泄漏
 */
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.loading-mask {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  z-index: 10;
  backdrop-filter: blur(2px);
}
</style>