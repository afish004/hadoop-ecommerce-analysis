<template>
  <div class="user-insight-container">
    <h2 class="page-title">用户价值分层</h2>
    
    <el-row :gutter="24">
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <h3 class="chart-title">RFM 用户分层占比</h3>
          <p class="chart-desc">基于 RFM 模型的用户价值分析</p>
          <PieChart :data="userInsightData.userSegmentation" height="500px" />
        </div>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <div class="info-card">
          <h3 class="info-title">RFM 模型说明</h3>
          
          <div class="rfm-item">
            <div class="rfm-label high-value">高价值用户</div>
            <p class="rfm-desc">
              近期购买频繁、消费金额高的用户。这类用户是核心客户，需要重点维护。
            </p>
          </div>
          
          <div class="rfm-item">
            <div class="rfm-label potential">潜力用户</div>
            <p class="rfm-desc">
              有一定消费能力，但购买频次较低。可通过营销活动提升活跃度。
            </p>
          </div>
          
          <div class="rfm-item">
            <div class="rfm-label retain">挽留用户</div>
            <p class="rfm-desc">
              曾经活跃但近期消费减少的用户。需要通过优惠券等方式挽回。
            </p>
          </div>
          
          <div class="rfm-item">
            <div class="rfm-label churn">流失用户</div>
            <p class="rfm-desc">
              长时间未购买、消费金额低的用户。可考虑放弃或低成本唤醒。
            </p>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchUserInsightData } from '@/api/service'
import PieChart from '@/components/PieChart.vue'

const userInsightData = ref({
  userSegmentation: []
})

const loadData = async () => {
  try {
    const response = await fetchUserInsightData()
    userInsightData.value = response.data
  } catch (error) {
    console.error('加载用户洞察数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.user-insight-container {
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
      margin: 0 0 24px 0;
      padding-bottom: 16px;
      border-bottom: 1px solid $border-color;
    }
    
    .rfm-item {
      margin-bottom: 24px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .rfm-label {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
        
        &.high-value {
          background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
          color: white;
        }
        
        &.potential {
          background: linear-gradient(135deg, #8ce99a 0%, #51cf66 100%);
          color: white;
        }
        
        &.retain {
          background: linear-gradient(135deg, #ffa94d 0%, #ff8c1a 100%);
          color: white;
        }
        
        &.churn {
          background: linear-gradient(135deg, #ff6b9d 0%, #ff4d7d 100%);
          color: white;
        }
      }
      
      .rfm-desc {
        font-size: 13px;
        color: $text-secondary;
        line-height: 1.6;
        margin: 0;
      }
    }
  }
}
</style>
