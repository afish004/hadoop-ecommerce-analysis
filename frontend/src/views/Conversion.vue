<template>
  <div class="conversion-container">
    <div class="page-header">
      <h2 class="page-title">流量与转化分析</h2>
      <p class="page-desc">深入分析用户行为路径与转化效率</p>
    </div>
    
    <el-row :gutter="20">
      <!-- 漏斗图 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">用户转化漏斗</h3>
            <span class="chart-subtitle">浏览 → 加购 → 下单</span>
          </div>
          <FunnelChart :data="conversionData.funnel" height="420px" />
        </div>
      </el-col>
      
      <!-- 玫瑰图 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">行为类型分布</h3>
            <span class="chart-subtitle">各类用户行为占比</span>
          </div>
          <RoseChart :data="conversionData.eventDistribution" height="420px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchConversionData } from '@/api/service'
import FunnelChart from '@/components/FunnelChart.vue'
import RoseChart from '@/components/RoseChart.vue'

const conversionData = ref({
  funnel: [],
  eventDistribution: []
})

const loadData = async () => {
  try {
    const response = await fetchConversionData()
    conversionData.value = response.data
  } catch (error) {
    console.error('加载转化分析数据失败:', error)
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
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: $text-primary;
      margin: 0 0 4px 0;
    }
    
    .page-desc {
      font-size: 14px;
      color: $text-muted;
      margin: 0;
    }
  }
  
  .el-col {
    margin-bottom: 20px;
  }
  
  .chart-card {
    background: $bg-card;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    
    &:hover {
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      transform: translateY(-2px);
    }
    
    .card-header {
      margin-bottom: 20px;
      
      .chart-title {
        font-size: 16px;
        font-weight: 600;
        color: $text-primary;
        margin: 0 0 4px 0;
      }
      
      .chart-subtitle {
        font-size: 13px;
        color: $text-muted;
      }
    }
  }
}
</style>
