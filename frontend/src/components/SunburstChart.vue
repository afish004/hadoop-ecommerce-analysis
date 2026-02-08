<!--
  旭日图组件 (SunburstChart)
  
  功能说明：
  - 展示层级数据的旭日图（Sunburst Chart）
  - 支持两层数据结构：一级分类 -> 二级分类
  - 自动将扁平数据（如 "Electronics.Smartphone"）转换为层级结构
  - 为不同一级分类分配固定颜色，二级分类自动继承并变淡
  
  使用场景：
  - 产品品牌分析页面
  - 展示产品类别的销售占比
  - 层级数据可视化
  
  Props:
  - data: 扁平数据数组，格式如 [{ name: 'Electronics.Smartphone', value: 1200 }]
  - height: 图表高度，默认 '400px'
  
  注意事项：
  - Tooltip 使用简单白色背景样式（已从磨砂玻璃效果回退）
  - 数据格式必须为 "一级分类.二级分类" 的点分隔格式
  - 颜色方案与项目整体大地色系保持一致
-->
<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

/**
 * 组件 Props 定义
 * @property {Array} data - 图表数据数组，格式：[{ name: 'Category.SubCategory', value: number }]
 * @property {String} height - 图表容器高度，默认 '400px'
 */
const props = defineProps({
  data: { type: Array, required: true },
  height: { type: String, default: '400px' }
})

// 图表 DOM 引用
const chartRef = ref(null)
// ECharts 实例
let chartInstance = null

/**
 * 数据转换函数：将扁平数据转换为层级结构
 * 
 * 输入格式：[{ name: 'Electronics.Smartphone', value: 1200 }, ...]
 * 输出格式：[{ name: 'Electronics', children: [{ name: 'Smartphone', value: 1200 }] }]
 * 
 * @param {Array} flatData - 扁平数据数组
 * @returns {Array} 层级结构数据数组
 */
const transformData = (flatData) => {
  const root = []
  const groups = {}
  
  // 颜色盘：给四大一级分类分配固定颜色，让层级更明显
  const categoryColors = {
    'Electronics': '#E85D3D', // 珊瑚橙
    'Appliances': '#E8A03D',  // 金黄色
    'Furniture': '#2D9F6E',   // 森林绿
    'Apparel': '#3D8FE8',     // 天空蓝
    'Computers': '#6B6560'    // 棕灰色
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
        itemStyle: { color: categoryColors[category] || '#D14B2E' }, // 分配父级颜色
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

/**
 * 初始化图表
 * - 创建 ECharts 实例
 * - 绑定窗口 resize 事件
 */
const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', () => chartInstance?.resize())
}

/**
 * 更新图表配置
 * - 将扁平数据转换为层级结构
 * - 配置旭日图样式和交互
 * - 应用简单白色背景 Tooltip（已从磨砂玻璃效果回退）
 */
const updateChart = () => {
  if (!chartInstance || !props.data || props.data.length === 0) return

  const sunburstData = transformData(props.data)

  const option = {
    // Tooltip 配置：简单白色背景样式（v1.0 回退版本）
    // 从磨砂玻璃效果回退，提升性能和兼容性
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)', // 白色半透明背景
      borderColor: '#e4e7ed',                       // 浅灰色边框
      textStyle: { color: '#333' },                 // 深灰色文字
      formatter: '{b}: {c}'                         // 显示格式：名称: 数值
    },
    // 旭日图系列配置
    series: {
      type: 'sunburst',
      data: sunburstData,
      radius: [0, '90%'], // 从中心到外围 90% 的半径
      
      // 层级样式配置：定义每一层的视觉效果
      levels: [
        // 第 0 层：中心点（隐形占位）
        {}, 
        
        // 第 1 层：一级分类（Electronics、Appliances 等）
        {
          r0: '15%',  // 内半径：15%
          r: '50%',   // 外半径：50%（较宽的环形）
          label: { 
            rotate: 'tangential', // 文字沿圆弧切线方向排列
            fontWeight: 'bold',   // 粗体文字
            fontSize: 12,
            color: '#fff'         // 白色文字（在深色背景上清晰可见）
          },
          itemStyle: {
            borderRadius: 6,      // 圆角边框
            borderWidth: 2,       // 边框宽度
            borderColor: '#fff'   // 白色边框（分隔各扇区）
          }
        },
        
        // 第 2 层：二级分类（Smartphone、Laptop 等）
        {
          r0: '50%',  // 内半径：50%（紧接第 1 层）
          r: '85%',   // 外半径：85%（最外层环形）
          label: { 
            align: 'right',       // 文字向外对齐
            color: '#666'         // 深灰色文字
          },
          itemStyle: {
            borderRadius: 4,      // 较小的圆角
            borderWidth: 2,
            borderColor: '#fff',
            opacity: 0.8          // 80% 不透明度（视觉层次感）
          }
        }
      ]
    }
  }
  chartInstance.setOption(option, true)
}

// 监听数据变化，自动更新图表
watch(() => props.data, updateChart, { deep: true })

// 生命周期钩子
onMounted(initChart)
onUnmounted(() => chartInstance?.dispose())
</script>