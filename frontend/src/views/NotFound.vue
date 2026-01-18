<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-icon">
        <el-icon :size="120"><WarningFilled /></el-icon>
      </div>
      <h1 class="error-code">404</h1>
      <h2 class="error-title">页面不存在</h2>
      <p class="error-desc">抱歉，您访问的页面不存在或已被删除</p>
      <el-button type="primary" size="large" @click="goHome">
        <el-icon><HomeFilled /></el-icon>
        返回首页
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { WarningFilled, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style lang="scss" scoped>
.not-found-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .not-found-content {
    text-align: center;
    padding: 60px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    .error-icon {
      color: #faad14;
      margin-bottom: 20px;
    }
    
    .error-code {
      font-size: 72px;
      font-weight: 700;
      background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 0 0 16px 0;
    }
    
    .error-title {
      font-size: 28px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 12px 0;
    }
    
    .error-desc {
      font-size: 16px;
      color: #606266;
      margin: 0 0 32px 0;
    }
    
    .el-button {
      padding: 12px 32px;
      font-size: 16px;
    }
  }
}
</style>
