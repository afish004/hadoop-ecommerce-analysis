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
  if (!chartInstance || !props.data) return

  const option = {
    tooltip: {
      position: 'top',
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
      min: 0,
      max: 100,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#f0f9ff', '#bae6fd', '#0ea5e9', '#0284c7'] // 科技蓝渐变
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