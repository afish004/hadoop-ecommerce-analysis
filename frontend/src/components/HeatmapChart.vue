<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: Array,
  height: { type: String, default: '350px' }
})

const chartRef = ref(null)
let chartInstance = null

const hours = Array.from({length: 24}, (_, i) => `${i}点`)
const days = ['周日', '周六', '周五', '周四', '周三', '周二', '周一']

const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', () => chartInstance?.resize())
}

const updateChart = () => {
  if (!chartInstance) return
  
  // 数据为空时清空图表（切换到无数据月份时显示空白）
  if (!props.data || props.data.length === 0) {
    chartInstance.clear()
    return
  }

  // 动态计算数据的最小值和最大值，确保热力图颜色有区分度
  const values = props.data.map(item => item[2])
  const dataMin = Math.min(...values)
  const dataMax = Math.max(...values)

  const option = {
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      formatter: (params) => {
        return `${days[params.value[1]]} ${hours[params.value[0]]}<br/>活跃热度: ${params.value[2]}`
      }
    },
    grid: { height: '70%', top: '10%', left: '10%', right: '5%' },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: { show: true },
      axisLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: { show: true },
      axisLine: { show: false }
    },
    visualMap: {
      min: dataMin,
      max: dataMax,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#FFF5E6', '#FFD8A8', '#FA8C16', '#E85D3D'] // 橙色系渐变
      }
    },
    series: [{
      type: 'heatmap',
      data: props.data,
      label: { show: false },
      itemStyle: {
        borderWidth: 2,
        borderColor: '#fff',
        borderRadius: 6
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  chartInstance.setOption(option)
}

watch(() => props.data, updateChart, { deep: true })
onMounted(initChart)
onUnmounted(() => chartInstance?.dispose())
</script>