<template>
  <div class="header">
    <div class="header-left">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-for="(item, index) in breadcrumbList" :key="index">
          {{ item.meta.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="header-right">
      <div class="icon-btn" @click="toggleFullScreen" title="全屏模式">
        <el-icon :size="20">
          <FullScreen v-if="!isFullScreen" />
          <Aim v-else />
        </el-icon>
      </div>

      <div class="current-time">
        <el-icon><Clock /></el-icon>
        <span>{{ currentTime }}</span>
      </div>

      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32" :src="avatarUrl">
            <el-icon><User /></el-icon>
          </el-avatar>
          <span class="username">管理员</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Clock, User, SwitchButton, FullScreen, Aim } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// --- 面包屑逻辑 ---
const breadcrumbList = computed(() => {
  return route.matched.filter(item => item.meta && item.meta.title && item.path !== '/dashboard')
})

// --- 全屏逻辑 ---
const isFullScreen = ref(false)
const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullScreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
      isFullScreen.value = false
    }
  }
}

// --- 原有的时间与登出逻辑 ---
const currentTime = ref('')
const avatarUrl = ref('')
let timer = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-')
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    ElMessage.success('退出登录成功')
    router.push('/login')
  }
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.header {
  height: 64px;
  background-color: $bg-header;
  border-bottom: 1px solid $border-color;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  
  .header-left {
    // 调整面包屑样式
    :deep(.el-breadcrumb__inner) {
      color: $text-secondary;
      font-weight: 500;
      
      &.is-link:hover {
        color: $primary-color;
      }
    }
    :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
      color: $text-primary;
      font-weight: 600;
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 24px;
    
    // 全屏按钮样式
    .icon-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      cursor: pointer;
      color: $text-secondary;
      transition: all 0.3s;
      
      &:hover {
        background: rgba(0, 0, 0, 0.05);
        color: $primary-color;
      }
    }
    
    .current-time {
      display: flex;
      align-items: center;
      gap: 8px;
      color: $text-secondary;
      font-size: 14px;
    }
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      padding: 6px 12px;
      border-radius: 6px;
      transition: all 0.3s ease;
      
      &:hover {
        background-color: rgba(24, 144, 255, 0.08);
      }
      
      .username {
        color: $text-primary;
        font-size: 14px;
      }
    }
  }
}
</style>