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
  
  // 暖色调配色板，橙色和绿色为主
  const colorPalette = [
    '#ff7a45',  // 橙色
    '#52c41a',  // 绿色
    '#faad14',  // 金黄色
    '#fa541c',  // 深橙红
    '#73d13d',  // 浅绿
    '#ffc53d',  // 金色
    '#ff9c6e',  // 浅橙
    '#95de64',  // 浅草绿
    '#ffd666',  // 浅金
    '#d46b08'   // 深橙
  ]
  
  // 给每个节点分配不同颜色
  const nodesWithColor = props.data.nodes.map((node, index) => ({
    ...node,
    itemStyle: {
      color: colorPalette[index % colorPalette.length],
      borderColor: '#fff',
      borderWidth: 1
    }
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: (params) => {
        if (params.dataType === 'edge') {
          return `${params.data.source} → ${params.data.target}<br/>流量: ${params.value.toLocaleString()}`
        }
        return `${params.name}: ${params.value?.toLocaleString() || ''}`
      }
    },
    series: [
      {
        type: 'sankey',
        layout: 'none',
        emphasis: { 
          focus: 'adjacency',
          lineStyle: {
            opacity: 0.8
          }
        },
        data: nodesWithColor,
        links: props.data.links,
        top: '5%',
        bottom: '5%',
        left: '2%',
        right: '18%',
        nodeWidth: 24,            // 增加节点宽度
        nodeGap: 20,              // 增加节点间距
        layoutIterations: 32,
        itemStyle: {
          borderWidth: 1,
          borderColor: '#fff'
        },
        lineStyle: {
          color: 'source',        // 线条颜色跟随源节点
          curveness: 0.5,
          opacity: 0.5            // 增加线条不透明度
        },
        label: {
          show: true,
          position: 'right',
          color: '#333',
          fontSize: 13,
          fontWeight: 'bold',
          formatter: '{b}'
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