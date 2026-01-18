<template>
  <div class="product-container">
    <h2 class="page-title">商品与品牌洞察</h2>
    
    <el-row :gutter="24">
      <!-- 品牌 TOP10 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <h3 class="chart-title">品牌销量 TOP10</h3>
          <p class="chart-desc">各品牌商品销量排行</p>
          <BarChart :data="brandTop10Data" height="450px" />
        </div>
      </el-col>
      
      <!-- 品类词云 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <h3 class="chart-title">热门品类分布</h3>
          <p class="chart-desc">品类关键词热度展示</p>
          <WordCloudList :data="productData.categoryWordCloud" />
        </div>
      </el-col>
    </el-row>
    
    <el-row :gutter="24">
      <!-- 价格敏感度分析 -->
      <el-col :xs="24">
        <div class="chart-card">
          <h3 class="chart-title">价格敏感度分析</h3>
          <p class="chart-desc">商品价格与销量的关系散点图</p>
          <ScatterChart :data="productData.priceSensitivity" height="400px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchProductData } from '@/api/service'
import BarChart from '@/components/BarChart.vue'
import WordCloudList from '@/components/WordCloudList.vue'
import ScatterChart from '@/components/ScatterChart.vue'

const productData = ref({
  brandTop10: {
    brands: [],
    sales: []
  },
  categoryWordCloud: [],
  priceSensitivity: []
})

// 转换品牌数据为 BarChart 格式
const brandTop10Data = computed(() => ({
  yAxis: productData.value.brandTop10.brands,
  data: productData.value.brandTop10.sales
}))

const loadData = async () => {
  try {
    const response = await fetchProductData()
    productData.value = response.data
  } catch (error) {
    console.error('加载商品分析数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.product-container {
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
}
</style>
