<template>
  <div class="main-layout">
    <!-- 左侧侧边栏 -->
    <Sidebar class="layout-sidebar" />
    
    <!-- 右侧内容区 -->
    <div class="layout-main">
      <!-- 顶部栏 -->
      <Header class="layout-header" />
      
      <!-- 内容区域 -->
      <div class="layout-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.main-layout {
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
  
  .layout-sidebar {
    flex-shrink: 0;
  }
  
  .layout-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .layout-header {
      flex-shrink: 0;
    }
    
    .layout-content {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      background-color: $bg-dark;
    }
  }
}

// 页面切换动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
