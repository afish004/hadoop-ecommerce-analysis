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
    // 【修复核心】：解决提示框被遮挡/显示不全的问题
    tooltip: {
      trigger: 'item',
      confine: true,  // <--- 关键！将提示框限制在图表区域内
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      borderWidth: 1,
      textStyle: { color: '#2c3e50' },
      // 提示框内容：显示 名称、数值、百分比
      formatter: '{b}<br/><b>{c}</b> ({d}%)' 
    },
    // 【布局优化】：图例放右边，不和饼图重叠
    legend: {
      type: 'scroll', // 防止图例太多溢出
      orient: 'vertical',
      right: 10,      // 固定在最右侧
      top: 'middle',  // 垂直居中
      itemWidth: 10,
      itemHeight: 10,
      itemGap: 15,
      textStyle: {
        color: '#606266',
        fontSize: 12,
        width: 120,           // 限制文字宽度
        overflow: 'truncate'  // 超出显示省略号
      },
      formatter: function (name) {
        return name.length > 15 ? name.substr(0, 15) + '...' : name;
      }
    },
    series: [
      {
        name: '销售占比',
        type: 'pie',
        // 调整半径，留出呼吸感
        radius: ['40%', '65%'], 
        // 【关键布局】：圆心左移到 30%，给右侧图例让路
        center: ['30%', '50%'], 
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 2
        },
        // 默认隐藏线条标签，保持界面整洁（信息都在图例和提示框里）
        label: {
          show: false, 
          position: 'center'
        },
        // 鼠标悬停时的高亮样式
        emphasis: {
          scale: true,
          scaleSize: 10,
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
            color: '#2c3e50',
            // 悬停时中间只显示百分比，简洁有力
            formatter: '{d}%' 
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.2)'
          }
        },
        labelLine: {
          show: false
        },
        data: props.data,
        color: ['#1890ff', '#13c2c2', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#eb2f96']
      }
    ]
  }
  
  chartInstance.setOption(option, true)
}

const handleResize = () => chartInstance?.resize()

watch(() => props.data, updateChart, { deep: true })

onMounted(() => initChart())

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>