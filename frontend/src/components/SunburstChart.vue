<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: { type: Array, required: true },
  height: { type: String, default: '400px' }
})

const chartRef = ref(null)
let chartInstance = null

// 数据转换：把 "Electronics.Smartphone" 这种扁平数据变成层级数据
const transformData = (flatData) => {
  const root = []
  const groups = {}
  
  // 颜色盘：给四大一级分类分配固定颜色，让层级更明显
  const categoryColors = {
    'Electronics': '#1890ff', // 蓝
    'Appliances': '#13c2c2',  // 青
    'Furniture': '#faad14',   // 橙
    'Apparel': '#f5222d',     // 红
    'Computers': '#52c41a'    // 绿
  }

  flatData.forEach(item => {
    // 兼容大小写，先转统一格式
    const nameParts = item.name.split('.')
    // 首字母大写处理 (electronics -> Electronics)
    const category = nameParts[0].charAt(0).toUpperCase() + nameParts[0].slice(1)
    const subCategory = nameParts[1] ? (nameParts[1].charAt(0).toUpperCase() + nameParts[1].slice(1)) : null
    
    if (!groups[category]) {
      groups[category] = { 
        name: category, 
        itemStyle: { color: categoryColors[category] || '#722ed1' }, // 分配父级颜色
        children: [] 
      }
      root.push(groups[category])
    }
    
    if (subCategory) {
      groups[category].children.push({
        name: subCategory,
        value: item.value,
        // 子级颜色会自动继承父级，但会变淡一点，ECharts自动处理
      })
    } else {
      groups[category].value = (groups[category].value || 0) + item.value
    }
  })
  return root
}

const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', () => chartInstance?.resize())
}

const updateChart = () => {
  if (!chartInstance || !props.data || props.data.length === 0) return

  const sunburstData = transformData(props.data)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}'
    },
    series: {
      type: 'sunburst',
      data: sunburstData,
      radius: [0, '90%'], // 0 表示中心是实心的或者很小的空洞
      
      // 关键：定义每一层的样式
      levels: [
        // 第0层：中心（隐形）
        {}, 
        // 第1层：一级分类 (Electronics 等)
        {
          r0: '15%', // 内半径
          r: '50%',  // 外半径 (这一层做宽一点)
          label: { 
            rotate: 'tangential', // 文字沿圆弧排列
            fontWeight: 'bold',
            fontSize: 12,
            color: '#fff' // 白字
          },
          itemStyle: {
            borderRadius: 6,
            borderWidth: 2,
            borderColor: '#fff'
          }
        },
        // 第2层：二级分类 (Smartphone 等)
        {
          r0: '50%',
          r: '85%', // 最外层
          label: { 
            align: 'right', // 文字向外对齐
            color: '#666'
          },
          itemStyle: {
            borderRadius: 4,
            borderWidth: 2,
            borderColor: '#fff',
            opacity: 0.8 // 稍微透明一点
          }
        }
      ]
    }
  }
  chartInstance.setOption(option, true)
}

watch(() => props.data, updateChart, { deep: true })
onMounted(initChart)
onUnmounted(() => chartInstance?.dispose())
</script>