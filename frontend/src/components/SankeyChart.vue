<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({ nodes: [], links: [] }) //以此防空
  },
  height: { type: String, default: '400px' }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  // 销毁旧实例防止内存泄漏或渲染异常
  if (chartInstance) {
    chartInstance.dispose()
  }
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', () => chartInstance?.resize())
}

const updateChart = () => {
  // 1. 安全检查：如果没实例或者数据里的 nodes 为空，就不画，防止报错
  if (!chartInstance || !props.data || !props.data.nodes || props.data.nodes.length === 0) {
    // console.warn('桑基图等待数据中...') 
    return
  }

  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: '{b}: {c}'
    },
    // 颜色盘：给桑基图一些好看的默认颜色
    color: ['#E85D3D', '#E8A03D', '#2D9F6E', '#3D8FE8', '#6B6560', '#D14B2E', '#F07A5F'],
    series: [
      {
        type: 'sankey',
        layout: 'none',
        emphasis: { focus: 'adjacency' },
        data: props.data.nodes,
        links: props.data.links,
        top: '5%',    // 留出边距
        bottom: '5%',
        left: '2%',
        right: '15%', // 右边留多点给文字
        nodeWidth: 20,
        nodeGap: 16,  // 节点间距拉大一点，防止重叠
        layoutIterations: 32, // 布局迭代次数，自动优化位置
        itemStyle: {
          borderWidth: 0,
          borderColor: '#fff'
        },
        lineStyle: {
          color: 'gradient', // 线条颜色渐变，更好看
          curveness: 0.5,
          opacity: 0.4
        },
        label: {
          show: true,
          position: 'right',
          color: '#333',
          fontSize: 12,
          fontWeight: 'bold'
        }
      }
    ]
  }
  
  chartInstance.setOption(option, true) // true 表示不合并，强制重绘
}

// 监听数据变化，一旦数据来了立马重绘
watch(() => props.data, async () => {
  await nextTick()
  updateChart()
}, { deep: true })

onMounted(() => {
  nextTick(() => initChart())
})

onUnmounted(() => chartInstance?.dispose())
</script>