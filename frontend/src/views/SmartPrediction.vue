<!--
  主题四：智能预测 (SmartPrediction)
  功能：时间序列预测、趋势分析
  特点：保留原 Prediction 页面内容
-->
<template>
  <div class="smart-prediction-container">
    <div class="page-header">
      <h2 class="page-title">智能预测分析</h2>
      <p class="page-desc">基于时间序列算法的流量趋势预测与分析</p>
    </div>
    
    <!-- Bento Grid 布局容器 -->
    <div class="bento-grid">
      <!-- 预测折线图：占据整行宽度 -->
      <div class="chart-card chart-prediction">
        <h3 class="chart-title-simple">未来7天流量预测曲线</h3>
        <!-- 示波器效果：背景网格 -->
        <div class="oscilloscope-grid">
          <LineChart :data="predictionChartData" height="520px" />
        </div>
      </div>
      
      <!-- 预测模型说明 -->
      <div class="info-card chart-model">
        <h3 class="info-title">预测模型技术说明</h3>
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
      
      <!-- 预测结果分析 -->
      <div class="info-card chart-result">
        <h3 class="info-title">预测结果数据分析</h3>
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
      
      <!-- AI 插图：温暖渐变风格 -->
      <div class="tech-illustration-card chart-ai">
        <div class="tech-illustration">
          <!-- AI 芯片图标 -->
          <div class="ai-chip-icon">
            <el-icon class="chip-icon"><Cpu /></el-icon>
          </div>
          <!-- 装饰性波浪线 -->
          <div class="wave-decoration"></div>
          <!-- 文字说明 -->
          <div class="tech-text">
            <p class="tech-title">AI 驱动预测</p>
            <p class="tech-desc">基于深度学习的时间序列分析</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, computed, onMounted } from 'vue'
import { fetchPredictionData } from '@/api/service'
import LineChart from '@/components/LineChart.vue'
import { TrendCharts, Cpu } from '@element-plus/icons-vue'

// ==================== 响应式状态 ====================

/**
 * 预测数据核心状态
 * 
 * @property {Object} historical - 历史数据
 * @property {string[]} historical.dates - 历史日期数组
 * @property {number[]} historical.pv - 历史 PV 数据数组
 * 
 * @property {Object} forecast - 预测数据
 * @property {string[]} forecast.dates - 预测日期数组
 * @property {number[]} forecast.pv - 预测 PV 数据数组
 * @property {Object} forecast.confidenceInterval - 置信区间
 * @property {number[]} forecast.confidenceInterval.upper - 置信区间上界
 * @property {number[]} forecast.confidenceInterval.lower - 置信区间下界
 */
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

// ==================== 计算属性 ====================

/**
 * 转换预测数据为 LineChart 组件所需格式
 * 
 * 功能说明：
 * 1. 合并历史日期和预测日期为完整的 X 轴
 * 2. 构建历史数据系列（实线）
 * 3. 构建预测数据系列（虚线）
 * 4. 构建置信区间上下界系列（点线 + 阴影区域）
 * 5. 在历史和预测数据之间添加连接点，确保图表连续
 * 
 * @returns {Object} LineChart 数据格式
 * @returns {string[]} return.xAxis - X 轴日期数组（历史 + 预测）
 * @returns {Array} return.series - 系列数据数组
 * @returns {Object} return.series[0] - 历史数据系列（实线）
 * @returns {Object} return.series[1] - 预测数据系列（虚线）
 * @returns {Object} return.series[2] - 置信区间上界（点线 + 阴影）
 * @returns {Object} return.series[3] - 置信区间下界（点线）
 * 
 * @example
 * // 输入：
 * // historical: { dates: ['2024-01-01', '2024-01-02'], pv: [1000, 1100] }
 * // forecast: { dates: ['2024-01-03', '2024-01-04'], pv: [1200, 1300], confidenceInterval: { upper: [1300, 1400], lower: [1100, 1200] } }
 * 
 * // 输出：
 * // {
 * //   xAxis: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
 * //   series: [
 * //     { name: '历史数据', data: [1000, 1100, null, null], lineStyle: { type: 'solid', width: 3 } },
 * //     { name: '预测数据', data: [null, null, 1100, 1200, 1300], lineStyle: { type: 'dashed', width: 3 } },
 * //     { name: '置信区间上界', data: [null, null, 1100, 1300, 1400], lineStyle: { type: 'dotted', width: 1, opacity: 0.5 }, areaStyle: true },
 * //     { name: '置信区间下界', data: [null, null, 1100, 1100, 1200], lineStyle: { type: 'dotted', width: 1, opacity: 0.5 } }
 * //   ]
 * // }
 */
const predictionChartData = computed(() => {
  const historical = predictionData.value.historical
  const forecast = predictionData.value.forecast
  
  // 合并历史和预测日期为完整的 X 轴
  const allDates = [...historical.dates, ...forecast.dates]
  
  // 历史数据系列：历史部分有值，预测部分为 null
  const historicalData = [...historical.pv, ...new Array(forecast.dates.length).fill(null)]
  
  // 预测数据系列：历史部分为 null，预测部分有值
  // 在历史数据的最后一个点添加连接点，确保图表连续
  const forecastData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1], // 连接点
    ...forecast.pv
  ]
  
  // 置信区间上界系列：历史部分为 null，预测部分有值
  const upperData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1], // 连接点
    ...forecast.confidenceInterval.upper
  ]
  
  // 置信区间下界系列：历史部分为 null，预测部分有值
  const lowerData = [
    ...new Array(historical.dates.length).fill(null),
    historical.pv[historical.pv.length - 1], // 连接点
    ...forecast.confidenceInterval.lower
  ]
  
  return {
    xAxis: allDates,
    series: [
      {
        name: '历史数据',
        data: historicalData,
        lineStyle: { type: 'solid', width: 3 } // 实线，粗线条
      },
      {
        name: '预测数据',
        data: forecastData,
        lineStyle: { type: 'dashed', width: 3 } // 虚线，粗线条
      },
      {
        name: '置信区间上界',
        data: upperData,
        lineStyle: { type: 'dotted', width: 1, opacity: 0.5 }, // 点线，细线条，半透明
        areaStyle: true // 填充阴影区域
      },
      {
        name: '置信区间下界',
        data: lowerData,
        lineStyle: { type: 'dotted', width: 1, opacity: 0.5 } // 点线，细线条，半透明
      }
    ]
  }
})

/**
 * 计算预测期间的平均 PV
 * 
 * 功能说明：
 * 1. 从预测数据中提取 PV 数组
 * 2. 计算平均值并四舍五入
 * 3. 格式化为千分位显示
 * 
 * @returns {string} 格式化后的平均 PV 值，如 '12,345'
 * 
 * @example
 * // 输入：forecast.pv = [1000, 1100, 1200, 1300, 1400, 1500, 1600]
 * // 输出：'1,300'
 */
const avgForecastPV = computed(() => {
  const forecast = predictionData.value.forecast.pv
  if (forecast.length === 0) return 0
  
  // 计算总和
  const sum = forecast.reduce((acc, val) => acc + val, 0)
  // 计算平均值并四舍五入
  const avg = Math.round(sum / forecast.length)
  // 格式化为千分位
  return avg.toLocaleString()
})

// ==================== 数据加载 ====================

/**
 * 加载预测数据
 * 
 * 功能说明：
 * 1. 调用预测数据 API 获取历史数据和预测数据
 * 2. 更新响应式状态，触发图表重新渲染
 * 
 * 数据来源：
 * - 当前使用 Mock 数据（frontend/src/api/mockData.js）
 * - 未来可对接真实预测模型 API（ARIMA / Prophet）
 * 
 * @async
 * @throws {Error} 当 API 请求失败时抛出错误并在控制台输出
 */
const loadData = async () => {
  try {
    const response = await fetchPredictionData()
    predictionData.value = response.data
  } catch (error) {
    console.error('加载预测数据失败:', error)
  }
}

// ==================== 生命周期 ====================

/**
 * 组件挂载时自动加载数据
 */
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.smart-prediction-container {
  position: relative;
  
  // ============================================
  // 背景装饰：有机光晕（紫色 + 橙色）
  // ============================================
  &::before {
    content: '';
    position: absolute;
    top: -80px;
    right: -80px;
    width: 450px;
    height: 450px;
    background: radial-gradient(
      circle, 
      rgba(124, 58, 237, 0.08) 0%,
      transparent 60%
    );
    pointer-events: none;
    z-index: 0;
    filter: blur(60px);
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: -80px;
    left: -80px;
    width: 500px;
    height: 500px;
    background: radial-gradient(
      circle, 
      rgba(232, 93, 61, 0.06) 0%,
      transparent 70%
    );
    pointer-events: none;
    z-index: 0;
    filter: blur(70px);
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
  
  // Bento Grid 布局
  .bento-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: auto auto;
    gap: 20px;
    
    // 预测折线图：占据整行宽度（第 1 行）
    .chart-prediction {
      grid-column: 1 / 4;
      grid-row: 1;
    }
    
    // 模型说明：左下
    .chart-model {
      grid-column: 1 / 2;
      grid-row: 2;
    }
    
    // 预测结果：中下
    .chart-result {
      grid-column: 2 / 3;
      grid-row: 2;
    }
    
    // AI 插图：右下
    .chart-ai {
      grid-column: 3 / 4;
      grid-row: 2;
    }
    
    // 响应式：平板/移动端
    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
      
      .chart-prediction,
      .chart-model,
      .chart-result,
      .chart-ai {
        grid-column: 1;
        grid-row: auto;
      }
    }
  }
  
  .chart-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 16px;
    padding: 24px;
    box-shadow: $shadow-sm;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    
    &:hover {
      transform: rotate(-0.3deg) scale(1.005);
      box-shadow: $shadow-md;
      border-color: rgba(232, 93, 61, 0.15);
    }
  }
  
  // 简洁图表标题样式
  .chart-title-simple {
    font-size: 16px;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: 16px;
    letter-spacing: -0.3px;
    position: relative;
    padding-bottom: 12px;
    
    // 手写感的下划线
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 50%;
      height: 2px;
      background: $primary-color;
      opacity: 0.3;
      border-radius: 2px;
    }
  }
  
  .info-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 16px;
    padding: 24px;
    box-shadow: $shadow-sm;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    
    &:hover {
      transform: rotate(-0.3deg) scale(1.005);
      box-shadow: $shadow-md;
      border-color: rgba(232, 93, 61, 0.15);
    }
    
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
          background: rgba(217, 119, 6, 0.1);
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
        background: rgba(232, 93, 61, 0.08);
        border-left: 3px solid $primary-color;
        border-radius: 4px;
        font-size: 13px;
        line-height: 1.6;
      }
    }
  }
  
  // ============================================
  // 示波器效果背景网格（温暖橙色调）
  // ============================================
  .oscilloscope-grid {
    position: relative;
    background-image: 
      linear-gradient(rgba(232, 93, 61, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232, 93, 61, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    border-radius: 12px;
    padding: 16px;
    
    // 添加内阴影，增加深度感
    box-shadow: inset 0 2px 8px rgba(232, 93, 61, 0.03);
  }
  
  // ============================================
  // AI 插图卡片（温暖渐变 + 更有机的设计）
  // ============================================
  .tech-illustration-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 20px;          // 更圆润
    padding: 0;
    box-shadow: $shadow-sm;
    height: 100%;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    
    // 移除全局卡片的 ::before 和 ::after
    &::before,
    &::after {
      display: none;
    }
    
    &:hover {
      transform: rotate(1deg) scale(1.02);  // 反向旋转
      box-shadow: $shadow-lg;
      border-color: rgba(232, 160, 61, 0.4);
    }
    
    .tech-illustration {
      width: 100%;
      height: 100%;
      min-height: 300px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 28px;
      padding: 36px;
      
      // 温暖渐变背景（橙色系）
      background: linear-gradient(135deg, #FFF5E6 0%, #FFE8CC 100%);
      position: relative;
      overflow: hidden;
      
      // 装饰性网格（更明显）
      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
          linear-gradient(rgba(232, 93, 61, 0.08) 1px, transparent 1px),
          linear-gradient(90deg, rgba(232, 93, 61, 0.08) 1px, transparent 1px);
        background-size: 20px 20px;
        pointer-events: none;
      }
      
      // 添加有机光晕
      &::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(232, 160, 61, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        filter: blur(50px);
      }
      
      .ai-chip-icon {
        width: 90px;              // 更大的图标
        height: 90px;
        border-radius: 20px;      // 更圆润
        background: $gradient-primary;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(232, 93, 61, 0.35);
        position: relative;
        z-index: 1;
        animation: float 3s ease-in-out infinite;  // 添加浮动动画
        
        .chip-icon {
          font-size: 45px;
          color: white;
        }
      }
      
      .wave-decoration {
        width: 140px;             // 更宽的波浪
        height: 50px;             // 更高的波浪
        background: repeating-linear-gradient(
          90deg,
          rgba(232, 93, 61, 0.3) 0px,
          rgba(232, 93, 61, 0.3) 12px,
          transparent 12px,
          transparent 24px
        );
        border-radius: 25px;
        position: relative;
        z-index: 1;
      }
      
      .tech-text {
        text-align: center;
        position: relative;
        z-index: 1;
        
        .tech-title {
          font-size: 19px;
          font-weight: 700;
          color: $text-primary;
          margin-bottom: 10px;
          letter-spacing: -0.3px;
        }
        
        .tech-desc {
          font-size: 14px;
          color: $text-secondary;
          margin: 0;
          font-weight: 500;
        }
      }
    }
  }
  
  // AI 插图卡片
  .ai-illustration-card {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: 12px;
    padding: 0;
    box-shadow: $shadow-sm;
    height: 100%;
    overflow: hidden;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: $shadow-md;
      border-color: rgba(124, 58, 237, 0.3);
      
      .illustration-overlay {
        opacity: 1;
      }
    }
    
    .illustration-wrapper {
      position: relative;
      width: 100%;
      height: 100%;
      min-height: 300px;
      
      .ai-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 12px;
      }
      
      .illustration-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
          135deg,
          rgba(124, 58, 237, 0.9) 0%,
          rgba(94, 106, 210, 0.9) 100%
        );
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 12px;
        
        .ai-icon {
          font-size: 48px;
          color: white;
          margin-bottom: 12px;
        }
        
        .ai-text {
          font-size: 16px;
          font-weight: 600;
          color: white;
          margin: 0;
        }
      }
    }
  }
}
</style>
