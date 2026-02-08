<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  height: {
    type: String,
    default: '400px'
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  
  window.addEventListener('resize', handleResize)
}

const updateChart = () => {
  if (!chartInstance || !props.data) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#333' },
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
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
    yAxis: {
      type: 'category',
      data: props.data.yAxis || [],
      axisLine: {
        lineStyle: {
          color: '#e4e7ed'
        }
      },
      axisLabel: {
        color: '#606266'
      }
    },
    series: [
      {
        type: 'bar',
        data: props.data.data || [],
        barWidth: '60%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#E85D3D' },
            { offset: 1, color: '#F07A5F' }
          ]),
          borderRadius: [0, 4, 4, 0]
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#F07A5F' },
              { offset: 1, color: '#E85D3D' }
            ])
          }
        }
      }
    ]
  }
  
  chartInstance.setOption(option, true)
}

const handleResize = () => {
  chartInstance?.resize()
}

watch(() => props.data, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>
