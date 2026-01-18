<template>
  <div class="metric-card">
    <div class="metric-icon" :style="{ background: iconBg }">
      <el-icon :size="32">
        <component :is="icon" />
      </el-icon>
    </div>
    
    <div class="metric-content">
      <div class="metric-title">{{ title }}</div>
      <div class="metric-value">
        {{ formattedValue }}
        <span v-if="unit" class="metric-unit">{{ unit }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  unit: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    required: true
  },
  iconBg: {
    type: String,
    default: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)'
  }
})

// 格式化数值（添加千分位）
const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString()
  }
  return props.value
})
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
