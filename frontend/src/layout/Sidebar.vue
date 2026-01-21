<!--
  Sidebar 侧边栏导航组件
  功能：展示系统主导航菜单，支持路由跳转和激活状态高亮
  
  菜单结构：
  - 数仓运营大屏：综合数据驾驶舱，展示核心业务指标
  - 多维数据挖掘：
    - 用户行为路径：转化漏斗分析
    - 商品画像洞察：商品与品牌分析
    - 用户价值分层：用户分群与洞察
  - 辅助决策支持：
    - 流量时序预测：基于历史数据的趋势预测
-->
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
      <!-- 综合态势：数据驾驶舱入口 -->
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <span>数仓运营大屏</span>
      </el-menu-item>

      <!-- 核心分析分组：多维度数据挖掘模块 -->
      <el-menu-item-group title="多维数据挖掘">
        <!-- 转化分析：用户行为路径与转化漏斗 -->
        <el-menu-item index="/conversion">
          <el-icon><TrendCharts /></el-icon>
          <span>用户行为路径</span>
        </el-menu-item>
        
        <!-- 商品分析：商品画像与品牌洞察 -->
        <el-menu-item index="/product">
          <el-icon><Goods /></el-icon>
          <span>商品画像洞察</span>
        </el-menu-item>
        
        <!-- 用户洞察：用户价值分层与画像分析 -->
        <el-menu-item index="/user-insight">
          <el-icon><User /></el-icon>
          <span>用户价值分层</span>
        </el-menu-item>
      </el-menu-item-group>

      <!-- 智能决策分组：辅助决策支持模块 -->
      <el-menu-item-group title="辅助决策支持">
        <!-- 趋势预测：基于时序数据的流量预测 -->
        <el-menu-item index="/prediction">
          <el-icon><MagicStick /></el-icon>
          <span>流量时序预测</span>
        </el-menu-item>
      </el-menu-item-group>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Odometer,      // 仪表盘图标
  TrendCharts,   // 趋势图表图标
  Goods,         // 商品图标
  User,          // 用户图标
  MagicStick     // 魔法棒图标（预测）
} from '@element-plus/icons-vue'

// ==================== 路由管理 ====================

/**
 * Vue Router 实例
 * 用于编程式导航
 */
const router = useRouter()

/**
 * 当前路由信息
 * 用于获取当前路径，判断菜单激活状态
 */
const route = useRoute()

// ==================== 计算属性 ====================

/**
 * 当前激活的菜单项
 * 根据当前路由路径自动高亮对应菜单
 * 
 * @returns {string} 当前路由路径，如 '/dashboard'
 * 
 * @example
 * 当用户访问 /dashboard 时，"数仓运营大屏" 菜单项会高亮显示
 */
const activeMenu = computed(() => route.path)

// ==================== 事件处理 ====================

/**
 * 菜单选择处理函数
 * 当用户点击菜单项时，跳转到对应路由
 * 
 * @param {string} index - 菜单项的 index 值（路由路径）
 * 
 * @example
 * handleMenuSelect('/dashboard') // 跳转到 Dashboard 页面
 */
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
