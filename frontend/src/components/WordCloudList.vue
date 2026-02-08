<template>
  <div class="word-cloud-list">
    <div
      v-for="(item, index) in sortedData"
      :key="index"
      class="word-item"
      :style="getItemStyle(item, index)"
    >
      <span class="word-text">{{ item.name }}</span>
      <span class="word-value">{{ item.value }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

// 按值排序
const sortedData = computed(() => {
  return [...props.data].sort((a, b) => b.value - a.value)
})

// 获取每个词的样式
const getItemStyle = (item, index) => {
  const colors = ['#E85D3D', '#E8A03D', '#2D9F6E', '#3D8FE8', '#6B6560', '#D14B2E', '#F07A5F', '#FA8C16']
  const maxValue = sortedData.value[0]?.value || 1
  const ratio = item.value / maxValue
  
  // 字体大小：14px - 28px
  const fontSize = 14 + ratio * 14
  
  return {
    fontSize: `${fontSize}px`,
    color: colors[index % colors.length],
    opacity: 0.6 + ratio * 0.4
  }
}
</script>

<style lang="scss" scoped>
.word-cloud-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  
  .word-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 16px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
      transform: scale(1.1);
      background: rgba(255, 255, 255, 0.1);
    }
    
    .word-text {
      font-weight: 600;
    }
    
    .word-value {
      font-size: 12px;
      opacity: 0.7;
    }
  }
}
</style>
