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

  const option = {
    // ==================== 提示框配置 ====================
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: '{b} : {c}'
    },
    
    // ==================== 配色方案 ====================
    // v1.1 大地色系调色板（6 种颜色）
    // 从暖色到冷色，层次分明
    color: [
      '#E85D3D',  // 珊瑚橙（主色）
      '#E8A03D',  // 金黄色（次要色）
      '#2D9F6E',  // 森林绿（成功色）
      '#3D8FE8',  // 天空蓝（信息色）
      '#6B6560',  // 棕灰色（中性色）- v1.1 新增
      '#D14B2E'   // 深橙红（强调色）
    ],
    
    // ==================== 系列配置 ====================
    series: [
      {
        name: '转化漏斗',
        type: 'funnel',
        
        // 布局配置
        left: '15%',                      // 左侧留白 15%
        top: 20,                          // 顶部间距 20px
        bottom: 20,                       // 底部间距 20px
        width: '50%',                     // 漏斗宽度 50%
        
        // 数值范围配置
        min: 0,                           // 最小值
        max: maxValue,                    // 最大值（动态计算）
        minSize: '0%',                    // 最小阶段高度
        maxSize: '100%',                  // 最大阶段高度
        sort: 'descending',               // 排序方式：降序
        gap: 2,                           // 阶段间距 2px
        
        // ==================== 标签配置 ====================
        // 右侧标签显示阶段名称和数值
        label: {
          show: true,                     // 显示标签
          position: 'right',              // 标签位置：右侧
          fontSize: 14,                   // 字号 14px
          color: '#333',                  // 文字颜色：深灰
          formatter: '{b}\n{c}'           // 格式：名称 + 换行 + 数值
        },
        
        // ==================== 引导线配置 ====================
        labelLine: {
          length: 30,                     // 引导线长度 30px
          lineStyle: {
            width: 1,                     // 线宽 1px
            type: 'solid',                // 线型：实线
            color: '#999'                 // 线颜色：浅灰
          }
        },
        
        // ==================== 样式配置 ====================
        itemStyle: {
          borderColor: '#fff',            // 边框颜色：白色
          borderWidth: 1                  // 边框宽度 1px
        },
        
        // ==================== 高亮配置 ====================
        emphasis: {
          label: {
            fontSize: 16,                 // 高亮时字号 16px
            fontWeight: 'bold'            // 高亮时字重：粗体
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
