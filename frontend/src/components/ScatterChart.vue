/**
 * 散点图组件
 * 功能：展示价格与销量的关系分布，用于分析商品定价策略
 * 使用示例：<ScatterChart :data="scatterData" height="400px" />
 */
<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

// ==================== Props 定义 ====================
/**
 * 组件属性
 * @property {Array} data - 散点数据数组，格式：[[价格, 销量], [价格, 销量], ...]
 * @property {String} height - 图表高度，默认 400px
 */
const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  height: {
    type: String,
    default: '400px'
  }
})

// ==================== 响应式数据 ====================
/**
 * 图表容器 DOM 引用
 */
const chartRef = ref(null)

/**
 * ECharts 实例对象
 * 用于管理图表的生命周期和更新
 */
let chartInstance = null

// ==================== 图表初始化 ====================
/**
 * 初始化图表
 * 创建 ECharts 实例并绑定窗口大小变化监听
 */
const initChart = () => {
  if (!chartRef.value) return
  
  // 创建 ECharts 实例
  chartInstance = echarts.init(chartRef.value)
  
  // 渲染图表
  updateChart()
  
  // 监听窗口大小变化，自适应调整图表尺寸
  window.addEventListener('resize', handleResize)
}

// ==================== 图表更新 ====================
/**
 * 更新图表配置和数据
 * 当 props.data 变化时会自动调用此方法
 */
const updateChart = () => {
  // 确保图表实例和数据都存在
  if (!chartInstance || !props.data) return
  
  // 配置图表选项
  const option = {
    // 提示框配置
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: (params) => {
        return `价格: ¥${params.value[0].toFixed(2)}<br/>销量: ${params.value[1]}`
      }
    },
    // 网格配置：控制图表在容器中的位置
    grid: {
      left: '3%',
      right: '7%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    // X 轴配置：价格轴
    xAxis: {
      type: 'value',
      name: '价格 (元)',
      nameTextStyle: {
        color: '#606266'
      },
      axisLine: {
        lineStyle: {
          color: '#e4e7ed'
        }
      },
      axisLabel: {
        color: '#909399'
      },
      splitLine: {
        lineStyle: {
          color: '#e4e7ed',
          type: 'dashed'
        }
      }
    },
    // Y 轴配置：销量轴
    yAxis: {
      type: 'value',
      name: '销量',
      nameTextStyle: {
        color: '#606266'
      },
      axisLine: {
        show: false
      },
      axisLabel: {
        color: '#909399'
      },
      splitLine: {
        lineStyle: {
          color: '#e4e7ed',
          type: 'dashed'
        }
      }
    },
    // 系列配置：散点图数据
    series: [
      {
        type: 'scatter',
        data: props.data,
        symbolSize: 8,
        itemStyle: {
          color: '#E85D3D',
          opacity: 0.6
        },
        // 高亮样式：鼠标悬停时的效果
        emphasis: {
          itemStyle: {
            color: '#F07A5F',
            opacity: 1,
            borderColor: '#E85D3D',
            borderWidth: 2
          }
        }
      }
    ]
  }
  
  // 应用配置到图表实例（true 表示不合并，完全替换）
  chartInstance.setOption(option, true)
}

// ==================== 窗口大小调整 ====================
/**
 * 处理窗口大小变化
 * 自动调整图表尺寸以适应容器
 */
const handleResize = () => {
  chartInstance?.resize()
}

// ==================== 数据监听 ====================
/**
 * 监听数据变化
 * 当 props.data 发生变化时，自动更新图表
 * 注意：本次优化简化了逻辑，直接调用 updateChart()
 */
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// ==================== 生命周期钩子 ====================
/**
 * 组件挂载时初始化图表
 */
onMounted(() => {
  initChart()
})

/**
 * 组件卸载时清理资源
 * 移除事件监听器并销毁图表实例，防止内存泄漏
 */
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>
