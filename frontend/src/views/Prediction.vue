<template>
  <div class="prediction-container">
    <h2 class="page-title">趋势预测 (AI Forecast)</h2>
    
    <el-row :gutter="24">
      <el-col :xs="24">
        <div class="chart-card">
          <h3 class="chart-title">未来7天流量预测</h3>
          <p class="chart-desc">
            基于历史30天数据，使用时间序列算法预测未来7天的流量趋势
            <el-tag type="info" size="small" style="margin-left: 12px;">实线：历史数据</el-tag>
            <el-tag type="warning" size="small" style="margin-left: 8px;">虚线：预测数据</el-tag>
          </p>
          <LineChart :data="predictionChartData" height="500px" />
        </div>
      </el-col>
    </el-row>
    
    <el-row :gutter="24">
      <el-col :xs="24" :lg="12">
        <div class="info-card">
          <h3 class="info-title">预测模型说明</h3>
          <div class="info-content">
            <p><strong>算法：</strong>时间序列预测（ARIMA / Prophet）</p>
            <p><strong>训练数据：</strong>过去30天的 PV 数据</p>
            <p><strong>预测周期：</strong>未来7天</p>
            <p><strong>置信区间：</strong>95%（阴影区域）</p>
            <p class="note">
              注：当前为 Mock 数据展示，实际部署时将连接真实预测模型。
            </p>
          </div>
        </div>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <div class="info-card">
          <h3 class="info-title">预测结果分析</h3>
          <div class="info-content">
            <div class="prediction-stat">
              <span class="stat-label">预测平均 PV：</span>
              <span class="stat-value">{{ avgForecastPV }}</span>
            </div>
            <div class="prediction-stat">
              <span class="stat-label">预测趋势：</span>
              <span class="stat-value trend-up">
                <el-icon><TrendCharts /></el-icon>
                上升
              </span>
            </div>
            <div class="prediction-stat">
              <span class="stat-label">置信度：</span>
              <span class="stat-value">95%</span>
            </div>
            <p class="analysis-text">
              根据预测模型分析，未来7天流量呈现稳定上升趋势，建议提前准备运营活动和服务器资源。
            </p>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchPredictionData } from '@/api/service'
import LineChart from '@/components/LineChart.vue'
import { TrendCharts } from '@element-plus/icons-vue'

const predictionData = ref({
  historical: {
    dates: [],
    pv: []
  },
  forecast: {
    dates: [],
    pv: [],
    confidenceInterval: {
      upper: [],
      lower: []
    }
  }
})

// 转换为 LineChart 格式
const predictionChartData = computed(() => {
  const historical = predictionData.value.historical
  const forecast = predictionData.value.forecast
  
  // 合并日期
  const allDates = [...historical.dates, ...forecast.dates]
  
  // 历史数据（实线）
  const historicalData = [...historical.pv, ...new Array(forecast.dates.length).fill(null)]
  
  // 预测数据（虚线）
  const forecastData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1], // 连接点
    ...forecast.pv
  ]
  
  // 置信区间上界
  const upperData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1],
    ...forecast.confidenceInterval.upper
  ]
  
  // 置信区间下界
  const lowerData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1],
    ...forecast.confidenceInterval.lower
  ]
  
  return {
    xAxis: allDates,
    series: [
      {
        name: '历史数据',
        data: historicalData,
        lineStyle: { type: 'solid', width: 3 }
      },
      {
        name: '预测数据',
        data: forecastData,
        lineStyle: { type: 'dashed', width: 3 }
      },
      {
        name: '置信区间上界',
        data: upperData,
        lineStyle: { type: 'dotted', width: 1, opacity: 0.5 },
        areaStyle: true
      },
      {
        name: '置信区间下界',
        data: lowerData,
        lineStyle: { type: 'dotted', width: 1, opacity: 0.5 }
      }
    ]
  }
})

// 计算预测平均 PV
const avgForecastPV = computed(() => {
  const forecast = predictionData.value.forecast.pv
  if (forecast.length === 0) return 0
  
  const sum = forecast.reduce((acc, val) => acc + val, 0)
  const avg = Math.round(sum / forecast.length)
  return avg.toLocaleString()
})

const loadData = async () => {
  try {
    const response = await fetchPredictionData()
    predictionData.value = response.data
  } catch (error) {
    console.error('加载预测数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.prediction-container {
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: $text-primary;
    margin: 0 0 24px 0;
  }
  
  .el-col {
    margin-bottom: 24px;
  }
  
  .chart-card {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: 8px;
    padding: 24px;
    transition: all 0.3s ease;
    
    &:hover {
      border-color: $primary-color;
      box-shadow: $shadow-md;
    }
    
    .chart-title {
      font-size: 16px;
      font-weight: 600;
      color: $text-primary;
      margin: 0 0 8px 0;
    }
    
    .chart-desc {
      font-size: 13px;
      color: $text-muted;
      margin: 0 0 20px 0;
      display: flex;
      align-items: center;
    }
  }
  
  .info-card {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: 8px;
    padding: 24px;
    height: 100%;
    
    .info-title {
      font-size: 16px;
      font-weight: 600;
      color: $text-primary;
      margin: 0 0 20px 0;
      padding-bottom: 12px;
      border-bottom: 1px solid $border-color;
    }
    
    .info-content {
      p {
        font-size: 14px;
        color: $text-secondary;
        line-height: 2;
        margin: 0 0 12px 0;
        
        strong {
          color: $text-primary;
        }
        
        &.note {
          margin-top: 16px;
          padding: 12px;
          background: rgba(255, 169, 77, 0.1);
          border-left: 3px solid $warning-color;
          border-radius: 4px;
          font-size: 13px;
          color: $warning-color;
        }
      }
      
      .prediction-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid $divider-color;
        
        &:last-of-type {
          border-bottom: none;
        }
        
        .stat-label {
          font-size: 14px;
          color: $text-secondary;
        }
        
        .stat-value {
          font-size: 16px;
          font-weight: 600;
          color: $primary-color;
          
          &.trend-up {
            color: $success-color;
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }
      
      .analysis-text {
        margin-top: 16px;
        padding: 12px;
        background: rgba(0, 212, 255, 0.05);
        border-left: 3px solid $primary-color;
        border-radius: 4px;
        font-size: 13px;
        line-height: 1.6;
      }
    }
  }
}
</style>
