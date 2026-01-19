<!--
  MetricCard 指标卡片组件
  功能：展示关键业务指标，支持数字滚动动画效果
  使用示例：
  <MetricCard 
    title="总用户数" 
    :value="12580" 
    unit="人"
    icon="User"
    iconBg="linear-gradient(135deg, #1890ff 0%, #096dd9 100%)"
  />
-->
<template>
  <div class="metric-card">
    <!-- 图标区域 -->
    <div class="metric-icon" :style="{ background: iconBg }">
      <el-icon :size="32">
        <component :is="icon" />
      </el-icon>
    </div>
    
    <!-- 内容区域 -->
    <div class="metric-content">
      <div class="metric-title">{{ title }}</div>
      <div class="metric-value">
        {{ displayValue }}
        <span v-if="unit" class="metric-unit">{{ unit }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// ==================== Props 定义 ====================
/**
 * 组件属性定义
 * @property {string} title - 指标标题（必填）
 * @property {number|string} value - 指标数值（必填），支持数字或字符串
 * @property {string} unit - 单位（可选），如 "人"、"元"、"%"
 * @property {string} icon - Element Plus 图标名称（必填），如 "User"、"ShoppingCart"
 * @property {string} iconBg - 图标背景渐变色（可选），默认为蓝色渐变
 */
const props = defineProps({
  title: { type: String, required: true },
  value: { type: [Number, String], required: true },
  unit: { type: String, default: '' },
  icon: { type: String, required: true },
  iconBg: { type: String, default: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)' }
})

// ==================== 响应式数据 ====================
/**
 * 显示的数值（用于动画过渡）
 * 初始值为 '0'，会通过动画逐渐变化到目标值
 */
const displayValue = ref('0')

// ==================== 动画函数 ====================
/**
 * 数字滚动动画函数（原生实现，不依赖第三方库）
 * 使用 requestAnimationFrame 实现流畅的数字递增动画
 * 
 * @param {number} start - 起始值
 * @param {number} end - 目标值
 * @param {number} duration - 动画持续时间（毫秒）
 * 
 * @example
 * animateValue(0, 1000, 1500) // 从 0 滚动到 1000，耗时 1.5 秒
 */
const animateValue = (start, end, duration) => {
  let startTimestamp = null;
  
  // 动画步进函数
  const step = (timestamp) => {
    // 记录动画开始时间
    if (!startTimestamp) startTimestamp = timestamp;
    
    // 计算动画进度（0 到 1）
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    
    // 根据进度计算当前值
    const currentVal = Math.floor(progress * (end - start) + start);
    
    // 更新显示值，并添加千分位分隔符
    displayValue.value = currentVal.toLocaleString();
    
    // 如果动画未完成，继续下一帧
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      // 动画完成，确保最终值精确
      displayValue.value = end.toLocaleString();
    }
  };
  
  // 启动动画
  window.requestAnimationFrame(step);
}

// ==================== 数据监听 ====================
/**
 * 监听 value 属性变化，触发动画
 * - 如果是数字类型：执行滚动动画
 * - 如果是字符串类型：直接显示
 * 
 * immediate: true 表示组件挂载时立即执行一次
 */
watch(() => props.value, (newVal) => {
  if (typeof newVal === 'number') {
    // 数字类型：从 0 滚动到目标值，动画时长 1.5 秒
    animateValue(0, newVal, 1500);
  } else {
    // 字符串类型：直接赋值
    displayValue.value = newVal;
  }
}, { immediate: true })
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.metric-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: $bg-card;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
  }
  
  .metric-icon {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .metric-content {
    flex: 1;
    .metric-title {
      font-size: 14px;
      color: $text-secondary;
      margin-bottom: 8px;
    }
    .metric-value {
      font-size: 28px;
      font-weight: 600;
      color: $text-primary;
      font-family: 'DIN Alternate', 'Helvetica Neue', sans-serif; // 使用更适合数字的字体
      
      .metric-unit {
        font-size: 14px;
        font-weight: 400;
        color: $text-muted;
        margin-left: 4px;
      }
    }
  }
}
</style>