<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
/**
 * WordCloudChart 词云图组件
 * 
 * 功能说明：
 * - 使用 echarts-wordcloud 插件实现词云效果
 * - 支持暖色系随机配色（珊瑚橙、金黄、森林绿等）
 * - 支持响应式布局，自动适配容器大小
 * - 支持悬停高亮效果
 * 
 * @component WordCloudChart
 * @example
 * <WordCloudChart 
 *   :data="[{ name: '手机', value: 1500 }, { name: '电脑', value: 1200 }]" 
 *   height="300px" 
 * />
 */

import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'

/**
 * 组件属性定义
 */
const props = defineProps({
  /**
   * 词云数据
   * @type {Array<{name: string, value: number}>}
   * @example [{ name: '手机', value: 1500 }, { name: '电脑', value: 1200 }]
   */
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  /**
   * 图表高度
   * @type {string}
   * @default '300px'
   */
  height: {
    type: String,
    default: '300px'
  }
})

// 图表容器引用
const chartRef = ref(null)
// ECharts 实例
let chartInstance = null

/**
 * 初始化图表
 * 创建 ECharts 实例并渲染词云
 */
const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  
  // 监听窗口大小变化，自动调整图表大小
  window.addEventListener('resize', handleResize)
}

/**
 * 更新图表配置
 * 根据传入的数据更新词云显示
 */
const updateChart = () => {
  if (!chartInstance || !props.data) return
  
  const option = {
    // Tooltip 配置
    tooltip: {
      show: true,
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' }
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',  // 词云形状：圆形
      left: 'center',
      top: 'center',
      width: '95%',
      height: '95%',
      right: null,
      bottom: null,
      sizeRange: [14, 40],  // 字体大小范围：14px - 40px
      rotationRange: [-30, 30],  // 旋转角度范围：-30° - 30°
      rotationStep: 15,  // 旋转步长：15°
      gridSize: 12,  // 网格大小：控制词语之间的间距
      drawOutOfBound: false,  // 不绘制超出边界的词语
      textStyle: {
        fontFamily: 'Inter, sans-serif',
        fontWeight: 'bold',
        // 核心：使用 Warm Linear 暖色系随机配色
        color: function () {
          const colors = [
            '#E85D3D', // 珊瑚橙
            '#E8A03D', // 金黄
            '#2D9F6E', // 森林绿
            '#D14B2E', // 砖红
            '#32325D', // 深蓝灰
            '#6B6560'  // 暖灰
          ];
          return colors[Math.floor(Math.random() * colors.length)];
        }
      },
      // 悬停高亮效果
      emphasis: {
        focus: 'self',
        textStyle: {
          textShadowBlur: 10,
          textShadowColor: 'rgba(232, 93, 61, 0.3)'
        }
      },
      data: props.data
    }]
  }
  
  chartInstance.setOption(option)
}

/**
 * 处理窗口大小变化
 * 自动调整图表大小以适应容器
 */
const handleResize = () => chartInstance?.resize()

/**
 * 监听数据变化
 * 当数据更新时，重新渲染图表
 */
watch(() => props.data, updateChart, { deep: true })

/**
 * 组件挂载时初始化图表
 */
onMounted(initChart)

/**
 * 组件卸载时清理资源
 * 移除事件监听器并销毁图表实例
 */
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
/* 词云图容器样式 */
div {
  width: 100%;
}
</style>
