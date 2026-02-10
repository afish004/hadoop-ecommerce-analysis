<!--
  主题三：用户与转化全景 (UserConversion)
  功能：用户价值分层 + 转化漏斗 + 行为路径
  特点：合并原 Conversion 和 UserInsight 页面
-->
<template>
  <div class="user-conversion-container">
    <div class="page-header">
      <h2 class="page-title">用户与转化全景</h2>
      <p class="page-desc">用户价值分层与全链路转化分析</p>
    </div>
    
    <!-- Bento Grid 布局容器：非对称布局 -->
    <div class="bento-grid">
      <!-- 顶部状态栏：RFM 用户分层 -->
      <div class="status-bar">
        <div class="status-header">
          <el-icon class="status-icon"><User /></el-icon>
          <h3 class="status-title">RFM 用户分层占比</h3>
        </div>
        
        <div class="rfm-segments">
          <div 
            v-for="(segment, index) in rfmSegments" 
            :key="segment.name"
            class="rfm-segment"
            :class="getSegmentClass(index)"
          >
            <div class="segment-label">{{ segment.name }}</div>
            <div class="segment-value">{{ segment.percent }}</div>
            <div class="segment-desc">{{ segment.count.toLocaleString() }} 人</div>
          </div>
        </div>
        
        <!-- RFM说明卡片 -->
        <div class="rfm-info-cards">
          <div class="info-card high-value">
            <div class="info-icon">👑</div>
            <div class="info-content">
              <div class="info-title">高价值用户</div>
              <div class="info-desc">近期购买频繁、消费金额高，是核心客户，需重点维护</div>
            </div>
          </div>
          <div class="info-card potential">
            <div class="info-icon">🌱</div>
            <div class="info-content">
              <div class="info-title">潜力用户</div>
              <div class="info-desc">有一定消费能力，购买频次较低，可通过活动提升活跃度</div>
            </div>
          </div>
          <div class="info-card retain">
            <div class="info-icon">🔔</div>
            <div class="info-content">
              <div class="info-title">挽留用户</div>
              <div class="info-desc">曾经活跃但近期消费减少，需通过优惠券等方式挽回</div>
            </div>
          </div>
          <div class="info-card churn">
            <div class="info-icon">💤</div>
            <div class="info-content">
              <div class="info-title">流失用户</div>
              <div class="info-desc">长时间未购买、消费金额低，可考虑放弃或低成本唤醒</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 左侧 40%：转化漏斗 -->
      <div class="chart-card chart-funnel">
        <h3 class="chart-title-simple">总体转化漏斗</h3>
        <FunnelChart :data="conversionData.funnel" height="500px" />
      </div>
      
      <!-- 右侧 60%：桑基图 -->
      <div class="chart-card chart-sankey">
        <h3 class="chart-title-simple">用户行为流转全景</h3>
        <SankeyChart :data="conversionData.sankey" height="500px" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { fetchConversionData, fetchUserInsightData } from '@/api/service'
import { User, Connection, Sort } from '@element-plus/icons-vue'
import FunnelChart from '@/components/FunnelChart.vue'
import SankeyChart from '@/components/SankeyChart.vue'

const userData = ref({
  userSegmentation: []
})

const conversionData = ref({
  funnel: [],
  sankey: { nodes: [], links: [] }
})

// 计算RFM分层数据（带百分比）
const rfmSegments = computed(() => {
  const segmentation = userData.value.userSegmentation || []
  const total = segmentation.reduce((sum, item) => sum + (item.value || 0), 0)
  
  return segmentation.map(item => ({
    name: item.name,
    count: item.value || 0,
    percent: total > 0 ? ((item.value / total) * 100).toFixed(1) + '%' : '0%'
  }))
})

// 获取分层样式类（根据索引循环使用颜色）
const getSegmentClass = (index) => {
  const classes = ['high-value', 'potential', 'retain', 'churn']
  return classes[index % classes.length]
}

const loadData = async () => {
  try {
    // 加载用户洞察数据
    const userResponse = await fetchUserInsightData()
    userData.value = userResponse.data
    
    // 加载转化数据
    const conversionResponse = await fetchConversionData()
    conversionData.value = conversionResponse.data
  } catch (error) {
    console.error('加载用户与转化数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.user-conversion-container {
  position: relative;
  
  // ============================================
  // 背景装饰：更大的有机光晕（绿色 + 橙色）
  // ============================================
  &::before {
    content: '';
    position: absolute;
    top: -120px;
    right: -120px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(45, 159, 110, 0.12) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(80px);
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: -120px;
    left: -120px;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(232, 93, 61, 0.09) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(90px);
  }
  
  // 确保内容在装饰层之上
  > * {
    position: relative;
    z-index: 1;
  }
  
  .page-header {
    margin-bottom: 28px;
    
    .page-title {
      font-size: 28px;
      font-weight: 700;
      color: $text-primary;
      margin-bottom: 6px;
      letter-spacing: -0.5px;
    }
    
    .page-desc {
      font-size: 15px;
      color: $text-secondary;
      font-weight: 500;
    }
  }
  
  // Bento Grid 布局：非对称布局 2fr 3fr
  .bento-grid {
    display: grid;
    grid-template-columns: 2fr 3fr;
    grid-template-rows: auto auto;
    gap: 20px;
    
    // 顶部状态栏：横跨两列
    .status-bar {
      grid-column: 1 / 3;
      grid-row: 1;
    }
    
    // 左侧 40%：漏斗图
    .chart-funnel {
      grid-column: 1;
      grid-row: 2;
    }
    
    // 右侧 60%：桑基图
    .chart-sankey {
      grid-column: 2;
      grid-row: 2;
    }
    
    // 响应式：平板/移动端
    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
      
      .status-bar,
      .chart-funnel,
      .chart-sankey {
        grid-column: 1;
        grid-row: auto;
      }
    }
  }
  
  // ============================================
  // 状态栏样式：RFM 用户分层（更有个性）
  // ============================================
  .status-bar {
    background: $gradient-card;
    border: 1.5px solid $border-color;
    border-radius: 20px;          // 更圆润
    padding: 28px 32px;           // 更宽松
    box-shadow: $shadow-md;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    
    &:hover {
      box-shadow: $shadow-lg;
      transform: scale(1.008);
    }
    
    .status-header {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 28px;
      padding-bottom: 18px;
      position: relative;
      
      // 手写感的下划线（更粗更明显）
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 50%;
        height: 3px;
        background: linear-gradient(90deg, $primary-color 0%, transparent 100%);
        opacity: 0.4;
        border-radius: 3px;
      }
      
      .status-icon {
        font-size: 24px;
        color: $primary-color;
      }
      
      .status-title {
        font-size: 19px;
        font-weight: 700;
        color: $text-primary;
        margin: 0;
        letter-spacing: -0.4px;
      }
    }
    
    .rfm-segments {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
      
      @media (max-width: 768px) {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    
    .rfm-segment {
      text-align: center;
      padding: 24px 18px;
      border-radius: 16px;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      position: relative;
      overflow: hidden;
      
      // 添加背景装饰
      &::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 100px;
        border-radius: 50%;
        pointer-events: none;
        filter: blur(30px);
        opacity: 0.5;
      }
      
      &:hover {
        transform: translateY(-6px) rotate(1.5deg);
      }
      
      &.high-value {
        background: linear-gradient(135deg, rgba(232, 93, 61, 0.15) 0%, rgba(209, 75, 46, 0.08) 100%);
        border: 2px solid rgba(232, 93, 61, 0.3);
        
        &::before {
          background: radial-gradient(circle, rgba(232, 93, 61, 0.3) 0%, transparent 70%);
        }
        
        .segment-value {
          color: $primary-color;
        }
      }
      
      &.potential {
        background: linear-gradient(135deg, rgba(45, 159, 110, 0.15) 0%, rgba(35, 127, 88, 0.08) 100%);
        border: 2px solid rgba(45, 159, 110, 0.3);
        
        &::before {
          background: radial-gradient(circle, rgba(45, 159, 110, 0.3) 0%, transparent 70%);
        }
        
        .segment-value {
          color: $success-color;
        }
      }
      
      &.retain {
        background: linear-gradient(135deg, rgba(232, 160, 61, 0.15) 0%, rgba(209, 144, 46, 0.08) 100%);
        border: 2px solid rgba(232, 160, 61, 0.3);
        
        &::before {
          background: radial-gradient(circle, rgba(232, 160, 61, 0.3) 0%, transparent 70%);
        }
        
        .segment-value {
          color: $warning-color;
        }
      }
      
      &.churn {
        background: linear-gradient(135deg, rgba(209, 75, 46, 0.15) 0%, rgba(185, 60, 38, 0.08) 100%);
        border: 2px solid rgba(209, 75, 46, 0.3);
        
        &::before {
          background: radial-gradient(circle, rgba(209, 75, 46, 0.3) 0%, transparent 70%);
        }
        
        .segment-value {
          color: $error-color;
        }
      }
      
      .segment-label {
        font-size: 14px;
        color: $text-secondary;
        margin-bottom: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
        position: relative;
        z-index: 1;
      }
      
      .segment-value {
        font-size: 36px;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: -1.2px;
        position: relative;
        z-index: 1;
      }
      
      .segment-desc {
        font-size: 13px;
        color: $text-muted;
        font-weight: 600;
        position: relative;
        z-index: 1;
      }
    }
  }
  
  // RFM说明卡片样式
  .rfm-info-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px dashed rgba(107, 101, 96, 0.2);
    
    @media (max-width: 1024px) {
      grid-template-columns: repeat(2, 1fr);
    }
    
    @media (max-width: 576px) {
      grid-template-columns: 1fr;
    }
    
    .info-card {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 14px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.5);
      border: 1px solid rgba(107, 101, 96, 0.1);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      }
      
      &.high-value {
        border-left: 3px solid $primary-color;
      }
      
      &.potential {
        border-left: 3px solid $success-color;
      }
      
      &.retain {
        border-left: 3px solid $warning-color;
      }
      
      &.churn {
        border-left: 3px solid $error-color;
      }
      
      .info-icon {
        font-size: 20px;
        flex-shrink: 0;
      }
      
      .info-content {
        .info-title {
          font-size: 13px;
          font-weight: 700;
          color: $text-primary;
          margin-bottom: 4px;
        }
        
        .info-desc {
          font-size: 12px;
          color: $text-secondary;
          line-height: 1.5;
        }
      }
    }
  }
  
  .chart-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 20px;
    padding: 28px;
    box-shadow: $shadow-sm;
    height: 100%;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    
    &:hover {
      transform: rotate(-0.5deg) scale(1.008);
      box-shadow: $shadow-lg;
      border-color: rgba(45, 159, 110, 0.25);
    }
  }
  
  // ============================================
  // 图表标题样式（更有个性）
  // ============================================
  .chart-title-simple {
    font-size: 17px;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: 18px;
    letter-spacing: -0.4px;
    position: relative;
    padding-bottom: 14px;
    
    // 手写感的下划线（更粗更明显）
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 60%;
      height: 3px;
      background: linear-gradient(90deg, $success-color 0%, transparent 100%);
      opacity: 0.4;
      border-radius: 3px;
    }
  }
}
</style>
