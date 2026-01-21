<template>
  <div class="conversion-container">
    <div class="page-header">
      <h2 class="page-title">用户行为路径分析</h2>
      <p class="page-desc">基于日志流的转化漏斗与路径追踪</p>
    </div>
    
    <el-row :gutter="20">
      <el-col :xs="24" :lg="8">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">总体转化漏斗</h3>
            <span class="chart-subtitle">宏观转化率概览</span>
          </div>
          <FunnelChart :data="conversionData.funnel" height="500px" />
        </div>
      </el-col>
      
      <el-col :xs="24" :lg="16">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">用户行为流转全景 (Sankey)</h3>
            <span class="chart-subtitle">可视化展示用户在各页面间的跳转与流失路径</span>
          </div>
          <SankeyChart :data="conversionData.sankey" height="500px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchConversionData } from '@/api/service'

// 1. 引入组件
import SankeyChart from '@/components/SankeyChart.vue'
import FunnelChart from '@/components/FunnelChart.vue' // 【修改点】引入漏斗图

const conversionData = ref({
  funnel: [],
  sankey: { nodes: [], links: [] }
})

const loadData = async () => {
  try {
    const res = await fetchConversionData()
    if (res.data) {
      conversionData.value = res.data
    }
  } catch (error) {
    console.error("加载转化数据失败", error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.conversion-container {
  .page-header {
    margin-bottom: 24px;
    .page-title { font-size: 24px; font-weight: 600; color: $text-primary; margin-bottom: 4px; }
    .page-desc { font-size: 14px; color: $text-muted; }
  }

  .chart-card {
    background: $bg-card;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    height: 100%;

    .card-header {
      margin-bottom: 20px;
      .chart-title { font-size: 16px; font-weight: 600; color: $text-primary; margin-bottom: 4px; }
      .chart-subtitle { font-size: 13px; color: $text-muted; }
    }
  }
}
</style>