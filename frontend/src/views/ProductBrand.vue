<!--
  主题二：商品与品牌洞察 (ProductBrand)
  功能：品类旭日图、品牌 TOP10、价格敏感度分析
  特点：商品专题页，三图组合展示
-->
<template>
  <div class="product-brand-container">
    <div class="page-header">
      <h2 class="page-title">商品与品牌洞察</h2>
      <p class="page-desc">多维度商品数据分析与品牌竞争力评估</p>
    </div>
    
    <!-- Bento Grid 布局容器：紧凑布局 -->
    <div class="bento-grid">
      <!-- 左上：旭日图 -->
      <div class="chart-card chart-sunburst">
        <h3 class="chart-title-simple">热门品类销售占比</h3>
        <!-- 
          旭日图容器包裹层
          功能说明：
          - 使用 Flexbox 让旭日图在卡片内垂直居中
          - 设置 height="100%" 让图表自适应容器高度
          - 解决旭日图在左侧两行高度下的居中对齐问题
        -->
        <div class="sunburst-wrapper">
          <SunburstChart :data="productData.categorySales" height="100%" />
        </div>
      </div>
      
      <!-- 品牌 TOP10 -->
      <div class="chart-card chart-brand">
        <h3 class="chart-title-simple">品牌销量排行 TOP10</h3>
        <BarChart :data="brandTop10Data" height="460px" />
      </div>
      
      <!-- 下方通栏：价格敏感度分析 -->
      <div class="chart-card chart-price">
        <h3 class="chart-title-simple">价格敏感度散点分析</h3>
        <ScatterChart :data="productData.priceSensitivity" height="380px" />
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, computed, onMounted } from 'vue'
import { fetchProductData, fetchDashboardData } from '@/api/service'
import BarChart from '@/components/BarChart.vue'
import ScatterChart from '@/components/ScatterChart.vue'
import SunburstChart from '@/components/SunburstChart.vue'

// ==================== 响应式状态 ====================

/**
 * 商品分析核心数据
 * 
 * @property {Object} brandTop10 - 品牌销量 TOP10 数据
 * @property {string[]} brandTop10.brands - 品牌名称数组
 * @property {number[]} brandTop10.sales - 对应品牌的销量数组
 * 
 * @property {Array<{name: string, value: number}>} categoryWordCloud - 品类词云数据
 *   格式：[{ name: '手机', value: 1500 }, ...]
 * 
 * @property {Array<[number, number]>} priceSensitivity - 价格敏感度散点数据
 *   格式：[[价格, 销量], [价格, 销量], ...]
 * 
 * @property {Array<{name: string, value: number}>} categorySales - 品类销售旭日图数据
 *   格式：[{ name: 'Electronics.Smartphone', value: 14500000 }, ...]
 *   支持多层级结构（用点号分隔）
 */
const productData = ref({
  brandTop10: {
    brands: [],
    sales: []
  },
  categoryWordCloud: [],
  priceSensitivity: [],
  categorySales: [] // 旭日图数据（从 Dashboard 获取）
})

// ==================== 计算属性 ====================

/**
 * 转换品牌数据为 BarChart 组件所需格式
 * 
 * @returns {Object} BarChart 数据格式
 * @returns {string[]} return.yAxis - Y轴品牌名称数组
 * @returns {number[]} return.data - 对应的销量数据数组
 * 
 * @example
 * // 输入：{ brands: ['Apple', 'Samsung'], sales: [1000, 800] }
 * // 输出：{ yAxis: ['Apple', 'Samsung'], data: [1000, 800] }
 */
const brandTop10Data = computed(() => ({
  yAxis: productData.value.brandTop10.brands,
  data: productData.value.brandTop10.sales
}))

// ==================== 数据加载 ====================

/**
 * 加载商品与品牌分析数据
 * 
 * 功能说明：
 * 1. 调用商品数据 API 获取品牌 TOP10、词云、价格敏感度数据
 * 2. 调用 Dashboard API 获取品类销售旭日图数据
 * 3. 更新响应式状态，触发图表重新渲染
 * 
 * 数据来源：
 * - 商品数据：fetchProductData() - 品牌、词云、价格敏感度
 * - 旭日图数据：fetchDashboardData() - 品类销售层级数据
 * - 当前使用 Mock 数据（frontend/src/api/mockData.js）
 * - 未来可对接真实后端 API
 * 
 * @async
 * @throws {Error} 当 API 请求失败时抛出错误并在控制台输出
 */
const loadData = async () => {
  try {
    // 加载商品数据（品牌 TOP10、词云、价格敏感度）
    const productResponse = await fetchProductData()
    productData.value.brandTop10 = productResponse.data.brandTop10
    productData.value.categoryWordCloud = productResponse.data.categoryWordCloud
    productData.value.priceSensitivity = productResponse.data.priceSensitivity
    
    // 加载旭日图数据（从 Dashboard API 获取品类销售层级数据）
    const dashboardResponse = await fetchDashboardData('2019-10-01', '2019-10-31')
    productData.value.categorySales = dashboardResponse.data.categorySales
  } catch (error) {
    console.error('加载商品分析数据失败:', error)
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

.product-brand-container {
  position: relative;
  
  // ============================================
  // 背景装饰：更大的有机光晕（橙色 + 金黄色）
  // ============================================
  // 设计理念：使用模糊的径向渐变创建有机光晕效果
  // 颜色选择：橙色系（#E8A03D）和橙红色（#E85D3D）呼应商品主题
  // 视觉效果：柔和的弥散光斑，增加页面温度感和层次感
  
  // 右上角橙色光晕（更大更明显）
  &::before {
    content: '';
    position: absolute;
    top: -100px;          // 向上溢出 100px
    right: -100px;        // 向右溢出 100px
    width: 550px;         // 光晕直径 550px（增加 100px）
    height: 550px;
    background: radial-gradient(circle, rgba(232, 160, 61, 0.12) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(70px);   // 70px 模糊
  }
  
  // 左下角橙红色光晕（更大更柔和）
  &::after {
    content: '';
    position: absolute;
    bottom: -100px;       // 向下溢出 100px
    left: -100px;         // 向左溢出 100px
    width: 600px;         // 光晕直径 600px（增加 100px）
    height: 600px;
    background: radial-gradient(circle, rgba(232, 93, 61, 0.09) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    filter: blur(80px);   // 80px 模糊
  }
  
  // 确保内容在装饰层之上
  > * {
    position: relative;
    z-index: 1;
  }
  
  // ============================================
  // 页面头部样式
  // ============================================
  .page-header {
    margin-bottom: 28px;  // 与内容区保持 28px 间距
    
    .page-title {
      font-size: 28px;           // 大标题字号（比 v2.2 的 24px 增加 4px）
      font-weight: 700;          // 粗体（比 v2.2 的 600 更粗）
      color: $text-primary;      // 主文本颜色
      margin-bottom: 6px;        // 与副标题间距 6px
      letter-spacing: -0.5px;    // 负字间距，更紧凑有个性
    }
    
    .page-desc {
      font-size: 15px;           // 副标题字号（比 v2.2 的 14px 增加 1px）
      color: $text-secondary;    // 次要文本颜色（比 v2.2 的 muted 更深）
      font-weight: 500;          // 中等字重（新增）
    }
  }
  
  // ============================================
  // 不对称 Bento Grid 布局：5fr 3fr (左侧适中，右侧稍窄)
  // ============================================
  .bento-grid {
    display: grid;
    grid-template-columns: 5fr 3fr;
    grid-template-rows: auto auto;
    gap: 20px;
    
    // 左上：旭日图（占据左侧两行）
    .chart-sunburst {
      grid-column: 1;
      grid-row: 1 / 3;
    }
    
    // 右上：品牌 TOP10
    .chart-brand {
      grid-column: 2;
      grid-row: 1;
    }
    
    // 右下：价格敏感度
    .chart-price {
      grid-column: 2;
      grid-row: 2;
    }
    
    // 响应式：平板/移动端
    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
      
      .chart-sunburst,
      .chart-brand,
      .chart-price {
        grid-column: 1;
        grid-row: auto;
      }
    }
  }
  
  .chart-card {
    background: $gradient-card;
    border: 1px solid $border-color;
    border-radius: 20px;          // 更圆润
    padding: 28px;                // 更宽松
    box-shadow: $shadow-sm;
    height: 100%;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    display: flex;
    flex-direction: column;
    
    &:hover {
      transform: rotate(-0.5deg) scale(1.008);  // 更明显的悬停效果
      box-shadow: $shadow-lg;
      border-color: rgba(232, 160, 61, 0.25);
    }
  }
  
  // ============================================
  // 旭日图容器：Flexbox 居中布局
  // ============================================
  // 设计理念：让旭日图在左侧两行高度的卡片内垂直居中
  // 技术实现：
  // - flex: 1 让容器占据剩余空间（标题下方的所有空间）
  // - display: flex + align-items: center 实现垂直居中
  // - justify-content: center 实现水平居中
  // - min-height: 0 解决 Flexbox 子元素高度计算问题
  // 
  // 为什么需要这个容器？
  // - 旭日图占据左侧两行（grid-row: 1 / 3），高度较大
  // - 直接使用固定高度（如 460px）会导致图表在大屏幕下显得过小
  // - 使用 height="100%" 让图表自适应容器高度，充分利用空间
  // - Flexbox 居中确保图表在容器内视觉平衡
  .sunburst-wrapper {
    flex: 1;                    // 占据剩余空间
    display: flex;              // Flexbox 布局
    align-items: center;        // 垂直居中
    justify-content: center;    // 水平居中
    min-height: 0;              // 解决 Flexbox 高度计算问题
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
      width: 60%;              // 更宽的下划线
      height: 3px;             // 更粗的下划线
      background: linear-gradient(90deg, $primary-color 0%, transparent 100%);
      opacity: 0.4;
      border-radius: 3px;
    }
  }
}
</style>
