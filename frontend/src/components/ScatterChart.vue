<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

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
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      borderWidth: 1,
      textStyle: {
        color: '#2c3e50'
      },
      formatter: (params) => {
        return `价格: ¥${params.value[0].toFixed(2)}<br/>销量: ${params.value[1]}`
      }
    },
    grid: {
      left: '3%',
      right: '7%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
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
    series: [
      {
        type: 'scatter',
        data: props.data,
        symbolSize: 8,
        itemStyle: {
          color: '#1890ff',
          opacity: 0.6
        },
        emphasis: {
          itemStyle: {
            color: '#40a9ff',
            opacity: 1,
            borderColor: '#1890ff',
            borderWidth: 2
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
