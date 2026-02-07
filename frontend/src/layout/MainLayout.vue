<!--
  MainLayout 主布局组件
  
  功能说明：
  - 应用的主布局框架，采用左侧边栏 + 右侧内容区的经典布局
  - 左侧：固定宽度的侧边栏导航（Sidebar）
  - 右侧：顶部栏（Header）+ 可滚动的内容区域（router-view）
  - 支持页面切换的淡入淡出动画效果
  
  布局结构：
  ┌─────────────────────────────────────┐
  │ Sidebar │ Header                    │
  │         ├───────────────────────────┤
  │         │ Content (router-view)     │
  │         │                           │
  │         │                           │
  └─────────────────────────────────────┘
  
  视觉特点：
  - 内容区域背景：反主流有机纹理（温暖的弥散光斑 + 细腻噪点）
  - 设计理念：拒绝冷冰冰的科技感，追求有温度的视觉体验
  - 页面切换：300ms 淡入淡出动画
  - 响应式布局：自适应不同屏幕尺寸
-->
<template>
  <div class="main-layout">
    <!-- 左侧侧边栏：固定宽度，包含主导航菜单 -->
    <Sidebar class="layout-sidebar" />
    
    <!-- 右侧内容区：弹性布局，包含顶部栏和内容区域 -->
    <div class="layout-main">
      <!-- 顶部栏：固定高度，包含用户信息、通知等 -->
      <Header class="layout-header" />
      
      <!-- 内容区域：可滚动，展示路由页面内容 -->
      <div class="layout-content">
        <!-- 路由视图：使用 v-slot 获取当前组件 -->
        <router-view v-slot="{ Component }">
          <!-- 页面切换动画：淡入淡出效果 -->
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================

/**
 * 侧边栏导航组件
 * 提供主导航菜单，包含数仓运营大屏、商品与品牌洞察、用户与转化全景、智能预测等入口
 */
import Sidebar from './Sidebar.vue'

/**
 * 顶部栏组件
 * 提供用户信息、通知、设置等功能入口
 */
import Header from './Header.vue'
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

// ============================================
// 主布局容器
// ============================================
// 采用 Flexbox 横向布局：左侧边栏 + 右侧内容区
.main-layout {
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden; // 防止整体滚动，仅内容区可滚动
  
  // 左侧侧边栏：固定宽度，不随内容区缩放
  .layout-sidebar {
    flex-shrink: 0;
  }
  
  // ============================================
  // 右侧主内容区
  // ============================================
  // 采用 Flexbox 纵向布局：顶部栏 + 内容区域
  .layout-main {
    flex: 1; // 占据剩余空间
    display: flex;
    flex-direction: column;
    overflow: hidden; // 防止整体滚动
    
    // 顶部栏：固定高度，不随内容区缩放
    .layout-header {
      flex-shrink: 0;
    }
    
    // ============================================
    // 内容区域：可滚动的路由视图容器
    // ============================================
    .layout-content {
      flex: 1; // 占据剩余空间
      overflow-y: auto; // 仅垂直方向可滚动
      padding: 24px; // 内容区域内边距
      background-color: $bg-dark; // 温暖的米白色背景
      
      // ============================================
      // 反主流视觉：有机的点阵纹理 + 噪点
      // ============================================
      // 效果：温暖、有呼吸感的背景（不是冷冰冰的网格）
      background-image: 
        radial-gradient(circle at 20% 30%, rgba(232, 93, 61, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(45, 159, 110, 0.03) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
    }
  }
}

// ============================================
// 页面切换动画：淡入淡出效果
// ============================================
// 用途：在路由切换时提供平滑的视觉过渡
// 时长：300ms
// 缓动函数：ease（先快后慢）

// 进入和离开动画的过渡效果
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

// 进入动画的起始状态 & 离开动画的结束状态
.fade-enter-from,
.fade-leave-to {
  opacity: 0; // 完全透明
}
</style>
