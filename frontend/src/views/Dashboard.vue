<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2 class="page-title">综合数据驾驶舱</h2>
      <p class="page-desc">实时监控核心业务指标与数据趋势</p>
    </div>
    
    <!-- 核心指标卡片 -->
    <el-row :gutter="20" class="metrics-row">
      <el-col :xs="24" :sm="8">
        <MetricCard
          title="总销售额 (GMV)"
          :value="dashboardData.metrics.gmv"
          unit="元"
          icon="TrendCharts"
          icon-bg="linear-gradient(135deg, #1890ff 0%, #096dd9 100%)"
        />
      </el-col>
      
      <el-col :xs="24" :sm="8">
        <MetricCard
          title="总访问量 (PV)"
          :value="dashboardData.metrics.pv"
          icon="View"
          icon-bg="linear-gradient(135deg, #52c41a 0%, #389e0d 100%)"
        />
      </el-col>
      
      <el-col :xs="24" :sm="8">
        <MetricCard
          title="独立访客数 (UV)"
          :value="dashboardData.metrics.uv"
          icon="User"
          icon-bg="linear-gradient(135deg, #faad14 0%, #d48806 100%)"
        />
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 24小时 PV/UV 趋势 -->
      <el-col :xs="24" :lg="14">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">24小时流量趋势</h3>
            <span class="chart-subtitle">实时监控访问量变化</span>
          </div>
          <LineChart :data="pvuvTrendData" height="380px" />
        </div>
      </el-col>
      
      <!-- 分类销售占比 -->
      <el-col :xs="24" :lg="10">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="chart-title">品类销售占比</h3>
            <span class="chart-subtitle">各品类销售额分布</span>
          </div>
          <PieChart :data="dashboardData.categorySales" height="380px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchDashboardData } from '@/api/service'
import MetricCard from '@/components/MetricCard.vue'
import LineChart from '@/components/LineChart.vue'
import PieChart from '@/components/PieChart.vue'

// Dashboard 数据
const dashboardData = ref({
  metrics: {
    gmv: 0,
    pv: 0,
    uv: 0
  },
  pvuvTrend: {
    xAxis: [],
    series: []
  },
  categorySales: []
})

// PV/UV 趋势数据（转换为 LineChart 需要的格式）
const pvuvTrendData = ref({
  xAxis: [],
  series: []
})

// 加载数据
const loadData = async () => {
  try {
    const response = await fetchDashboardData()
    dashboardData.value = response.data
    
    // 转换 PV/UV 趋势数据格式
    pvuvTrendData.value = {
      xAxis: response.data.pvuvTrend.xAxis,
      series: response.data.pvuvTrend.series
    }
  } catch (error) {
    console.error('加载 Dashboard 数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.dashboard-container {
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
  
  .metrics-row {
    margin-bottom: 20px;
    
    .el-col {
      margin-bottom: 20px;
    }
  }
  
  .charts-row {
    .el-col {
      margin-bottom: 20px;
    }
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
