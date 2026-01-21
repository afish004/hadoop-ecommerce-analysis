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
  window.addEventListener('resize', () => chartInstance?.resize())
}

const updateChart = () => {
  if (!chartInstance || !props.data || props.data.length === 0) return
  
  // 计算最大值，保证漏斗形状正确
  const maxValue = props.data.reduce((max, item) => Math.max(max, item.value), 0)

  const option = {
    // 【修改点】删除了 legend (图例) 配置，防止重叠
    tooltip: {
      trigger: 'item',
      formatter: '{b} : {c}'
    },
    color: ['#1890ff', '#13c2c2', '#faad14', '#f5222d', '#722ed1'],
    series: [
      {
        name: '转化漏斗',
        type: 'funnel',
        left: '15%', 
        top: 20,    // 顶部不需要留给图例了，稍微往上提一点
        bottom: 20,
        width: '50%', 
        
        min: 0,
        max: maxValue,
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 2,
        
        // 既然没有图例，右侧的标签就非常重要了
        label: {
          show: true,
          position: 'right',
          fontSize: 14,
          color: '#333',
          formatter: '{b}\n{c}' // 显示名称和数值
        },
        labelLine: {
          length: 30, // 稍微加长引线，让文字离漏斗远一点，更清晰
          lineStyle: {
            width: 1,
            type: 'solid',
            color: '#999'
          }
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          label: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: props.data
      }
    ]
  }
  
  chartInstance.setOption(option, true)
}

watch(() => props.data, updateChart, { deep: true })
onMounted(initChart)
onUnmounted(() => chartInstance?.dispose())
</script>