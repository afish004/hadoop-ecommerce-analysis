<!--
  漏斗图组件 (FunnelChart)
  功能：展示转化流程、流失分析
  使用场景：用户转化漏斗、销售漏斗、流程分析
-->
<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

// ==================== Props 定义 ====================
/**
 * 组件属性
 * @property {Array} data - 漏斗图数据数组
 * @property {Object} data[].name - 阶段名称（如 "浏览商品"、"加入购物车"）
 * @property {Number} data[].value - 阶段数值（用户数量）
 * @property {String} height - 图表高度（默认 400px）
 * 
 * @example
 * const funnelData = [
 *   { name: '浏览商品', value: 10000 },
 *   { name: '加入购物车', value: 5000 },
 *   { name: '提交订单', value: 2000 },
 *   { name: '完成支付', value: 1500 }
 * ]
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
 * 图表 DOM 引用
 * 用于初始化 ECharts 实例
 */
const chartRef = ref(null)

/**
 * ECharts 实例
 * 用于渲染和更新图表
 */
let chartInstance = null

// ==================== 图表初始化 ====================
/**
 * 初始化图表
 * 创建 ECharts 实例并绑定窗口 resize 事件
 */
const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', () => chartInstance?.resize())
}

// ==================== 图表更新 ====================
/**
 * 更新图表配置
 * 根据 props.data 动态生成漏斗图配置
 */
const updateChart = () => {
  if (!chartInstance || !props.data || props.data.length === 0) return
  
  // 计算最大值，保证漏斗形状正确
  const maxValue = props.data.reduce((max, item) => Math.max(max, item.value), 0)
  
  // 为每个阶段计算转化率
  const dataWithRate = props.data.map((item, index) => {
    const rate = index === 0 ? '100%' : ((item.value / props.data[0].value) * 100).toFixed(1) + '%'
    return { ...item, rate }
  })

  const option = {
    // ==================== 提示框配置 ====================
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: (params) => {
        const rate = dataWithRate[params.dataIndex]?.rate || ''
        return `${params.name}<br/>数量: ${params.value.toLocaleString()}<br/>转化率: ${rate}`
      }
    },
    
    // ==================== 配色方案 ====================
    // 暖色调配色，橙色和绿色为主
    color: [
      '#ff7a45',  // 橙色
      '#52c41a',  // 绿色
      '#faad14',  // 金黄色
      '#fa541c',  // 深橙红
      '#73d13d',  // 浅绿
      '#ffc53d'   // 金色
    ],
    
    // ==================== 系列配置 ====================
    series: [
      {
        name: '转化漏斗',
        type: 'funnel',
        
        // 布局配置
        left: '15%',
        top: 30,
        bottom: 30,
        width: '50%',
        
        // 倒三角漏斗图配置
        min: 0,
        max: maxValue,
        minSize: '15%',                   // 最小层宽度15%
        maxSize: '100%',
        sort: 'descending',               // 倒序：大值在上，小值在下
        funnelAlign: 'center',            // 居中对齐，形成倒三角
        gap: 4,
        
        // ==================== 标签配置 ====================
        label: {
          show: true,
          position: 'right',
          fontSize: 13,
          color: '#333',
          fontWeight: 'bold',
          formatter: (params) => {
            const rate = dataWithRate[params.dataIndex]?.rate || ''
            return `${params.name}\n${params.value.toLocaleString()}\n(${rate})`
          }
        },
        
        // ==================== 引导线配置 ====================
        labelLine: {
          length: 20,
          lineStyle: {
            width: 1,
            type: 'solid',
            color: '#999'
          }
        },
        
        // ==================== 样式配置 ====================
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: 'rgba(0,0,0,0.1)'
        },
        
        // ==================== 高亮配置 ====================
        emphasis: {
          label: {
            fontSize: 15,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(0,0,0,0.2)'
          }
        },
        
        // 数据源
        data: props.data
      }
    ]
  }
  
  // 应用配置（notMerge: true 表示不合并，完全替换）
  chartInstance.setOption(option, true)
}

// ==================== 生命周期钩子 ====================
/**
 * 监听数据变化
 * 当 props.data 变化时，重新渲染图表
 */
watch(() => props.data, updateChart, { deep: true })

/**
 * 组件挂载时初始化图表
 */
onMounted(initChart)

/**
 * 组件卸载时销毁图表实例
 * 释放内存，避免内存泄漏
 */
onUnmounted(() => chartInstance?.dispose())
</script>
