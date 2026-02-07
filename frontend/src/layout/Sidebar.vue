<!--
  Sidebar 侧边栏导航组件
  功能：展示系统主导航菜单，支持路由跳转和激活状态高亮
  
  菜单结构（按业务主题重构）：
  - 数仓运营大屏：首页，展示核心业务指标
  - 商品与品牌洞察：商品专题分析
  - 用户与转化全景：用户价值与转化分析
  - 智能预测：流量趋势预测
-->
<template>
  <div class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      background-color="#F5F3EF"
      text-color="#6B6560"
      active-text-color="#E85D3D"
      @select="handleMenuSelect"
    >
      <!-- 数仓运营大屏 -->
      <el-menu-item index="/ops-dashboard">
        <el-icon><Odometer /></el-icon>
        <span>数仓运营大屏</span>
      </el-menu-item>

      <!-- 商品与品牌洞察 -->
      <el-menu-item index="/product-brand">
        <el-icon><Goods /></el-icon>
        <span>商品与品牌洞察</span>
      </el-menu-item>
      
      <!-- 用户与转化全景 -->
      <el-menu-item index="/user-conversion">
        <el-icon><User /></el-icon>
        <span>用户与转化全景</span>
      </el-menu-item>

      <!-- 智能预测 -->
      <el-menu-item index="/smart-prediction">
        <el-icon><MagicStick /></el-icon>
        <span>智能预测</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
// ==================== 依赖导入 ====================
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Odometer,      // 仪表盘图标 - 数仓运营大屏
  Goods,         // 商品图标 - 商品与品牌主题
  User,          // 用户图标 - 用户与转化主题
  MagicStick     // 魔法棒图标 - 智能预测
} from '@element-plus/icons-vue'

// ==================== 路由实例 ====================
/**
 * Vue Router 实例
 * 用于编程式导航和路由跳转
 */
const router = useRouter()

/**
 * 当前路由对象
 * 用于获取当前路由路径，实现菜单激活状态
 */
const route = useRoute()

// ==================== 计算属性 ====================
/**
 * 当前激活的菜单项
 * 根据当前路由路径自动高亮对应菜单
 * 
 * @returns {string} 当前路由路径，如 '/ops-dashboard'
 * 
 * @example
 * // 当用户访问 /ops-dashboard 时，该菜单项会被高亮
 * activeMenu.value // '/ops-dashboard'
 */
const activeMenu = computed(() => route.path)

// ==================== 事件处理 ====================
/**
 * 菜单选择事件处理函数
 * 当用户点击菜单项时，跳转到对应路由
 * 
 * @param {string} index - 菜单项的 index 值（即路由路径）
 * 
 * @example
 * handleMenuSelect('/product-brand') // 跳转到商品与品牌主题页面
 */
const handleMenuSelect = (index) => {
  router.push(index)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

// ============================================
// 侧边栏容器样式
// ============================================
.sidebar {
  width: 240px;
  height: 100%;
  background-color: $bg-sidebar;
  border-right: 1px solid $border-color;
  overflow-y: auto;
  
  // ============================================
  // 菜单样式 - Linear 设计风格
  // ============================================
  .sidebar-menu {
    border-right: none;
    height: 100%;
    
    // 菜单项样式
    :deep(.el-menu-item) {
      height: 56px;
      line-height: 56px;
      padding-left: 24px !important;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      
      // 悬停效果
      &:hover {
        background-color: $hover-bg !important;
      }
      
      // 选中状态 - 使用渐变背景 + 左侧橙色边框
      &.is-active {
        background: linear-gradient(90deg, rgba(232, 93, 61, 0.10) 0%, transparent 100%) !important;
        border-left: 4px solid $primary-color;
        color: $primary-color !important;
        font-weight: 600;
      }
      
      // 图标样式
      .el-icon {
        font-size: 18px;
        margin-right: 12px;
        color: inherit;
      }
      
      // 文字样式
      span {
        font-size: 14px;
      }
    }
  }
}

// ============================================
// 滚动条样式优化
// ============================================
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: $bg-sidebar;
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.12);
  border-radius: 3px;
  
  &:hover {
    background: rgba(0, 0, 0, 0.18);
  }
}
</style>
