<template>
  <div class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      background-color="#ffffff"
      text-color="#606266"
      active-text-color="#1890ff"
      @select="handleMenuSelect"
    >
      <!-- 综合态势 -->
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <span>综合驾驶舱</span>
      </el-menu-item>

      <!-- 核心分析分组 -->
      <el-menu-item-group title="核心分析">
        <el-menu-item index="/conversion">
          <el-icon><TrendCharts /></el-icon>
          <span>流量与转化</span>
        </el-menu-item>
        
        <el-menu-item index="/product">
          <el-icon><Goods /></el-icon>
          <span>商品与品牌</span>
        </el-menu-item>
        
        <el-menu-item index="/user-insight">
          <el-icon><User /></el-icon>
          <span>用户价值分层</span>
        </el-menu-item>
      </el-menu-item-group>

      <!-- 智能决策分组 -->
      <el-menu-item-group title="智能决策">
        <el-menu-item index="/prediction">
          <el-icon><MagicStick /></el-icon>
          <span>趋势预测</span>
        </el-menu-item>
      </el-menu-item-group>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Odometer, 
  TrendCharts, 
  Goods, 
  User, 
  MagicStick 
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 当前激活的菜单项
const activeMenu = computed(() => route.path)

// 菜单选择处理
const handleMenuSelect = (index) => {
  router.push(index)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.sidebar {
  width: 240px;
  height: 100%;
  background-color: $bg-sidebar;
  border-right: 1px solid $border-color;
  overflow-y: auto;
  
  .sidebar-menu {
    border-right: none;
    height: 100%;
    
    // 菜单项样式
    :deep(.el-menu-item) {
      height: 56px;
      line-height: 56px;
      padding-left: 24px !important;
      transition: all 0.3s ease;
      
      &:hover {
        background-color: rgba(24, 144, 255, 0.08) !important;
      }
      
      // 选中状态
      &.is-active {
        background: linear-gradient(90deg, rgba(24, 144, 255, 0.1) 0%, transparent 100%) !important;
        border-left: 4px solid $primary-color;
        color: $primary-color !important;
        font-weight: 600;
      }
      
      .el-icon {
        font-size: 18px;
        margin-right: 12px;
        color: inherit;
      }
      
      span {
        font-size: 14px;
      }
    }
    
    // 分组标题样式
    :deep(.el-menu-item-group__title) {
      padding: 16px 0 8px 24px;
      font-size: 12px;
      color: $text-muted;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 600;
    }
  }
}

// 滚动条样式
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: $bg-sidebar;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #d9d9d9;
  border-radius: 3px;
  
  &:hover {
    background: $primary-color;
  }
}
</style>
