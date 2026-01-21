<template>
  <div class="chart-wrapper" style="position: relative; width: 100%;" :style="{ height }">
    <div v-if="loading" class="loading-mask">
      <el-icon class="is-loading" :size="24"><Loading /></el-icon>
      <div style="margin-top: 8px">数据计算中...</div>
    </div>

    <el-empty 
      v-else-if="isEmpty" 
      description="该时间段暂无数据" 
      :image-size="80"
      style="height: 100%;" 
    />

    <div 
      v-else 
      ref="chartRef" 
      :style="{ height, width: '100%' }"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { Loading } from '@element-plus/icons-vue'

const props = defineProps({
  data: Object,
  height: { type: String, default: '400px' },
  loading: { type: Boolean, default: false }
})

const chartRef = ref(null)
let chartInstance = null

// 判断数据是否为空
const isEmpty = computed(() => {
  if (!props.data) return true
  if (props.data.series && props.data.series.length === 0) return true
  // 检查所有 series 的 data 是否都有值
  if (props.data.series && props.data.series.every(s => !s.data || s.data.length === 0)) return true
  return false
})

const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', handleResize)
}

const updateChart = () => {
  if (!chartInstance || isEmpty.value) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      textStyle: { color: '#2c3e50' }
    },
    legend: { bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '10%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: props.data.xAxis || [],
      axisLine: { lineStyle: { color: '#e4e7ed' } }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: '#e4e7ed' } }
    },
    series: props.data.series.map((item, index) => ({
      ...item,
      type: 'line',
      smooth: true,
      symbol: 'none',
      areaStyle: {
        opacity: 0.2,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: index === 0 ? '#1890ff' : '#52c41a' },
          { offset: 1, color: 'rgba(255,255,255,0)' }
        ])
      }
    }))
  }
  chartInstance.setOption(option, true)
}

const handleResize = () => chartInstance?.resize()

watch(() => [props.data, props.loading], async () => {
  await nextTick()
  if (!chartInstance && chartRef.value) initChart()
  else updateChart()
}, { deep: true })

onMounted(async () => {
  await nextTick()
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.loading-mask {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  z-index: 10;
  backdrop-filter: blur(2px);
}
</style>