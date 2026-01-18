<template>
  <div class="header">
    <!-- 左侧：系统标题 -->
    <div class="header-left">
      <h1 class="system-title">Hadoop电商行为分析系统</h1>
    </div>

    <!-- 右侧：时间、用户信息、退出 -->
    <div class="header-right">
      <!-- 实时时间 -->
      <div class="current-time">
        <el-icon><Clock /></el-icon>
        <span>{{ currentTime }}</span>
      </div>

      <!-- 管理员信息 -->
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Clock, User, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()

// 当前时间
const currentTime = ref('')
let timer = null

// 头像 URL（可以替换为真实头像）
const avatarUrl = ref('')

// 更新时间
const updateTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  
  currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 下拉菜单命令处理
const handleCommand = (command) => {
  if (command === 'logout') {
    // 清除登录信息
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    
    ElMessage.success('退出登录成功')
    
    // 跳转到登录页
    router.push('/login')
  }
}

onMounted(() => {
  // 初始化时间
  updateTime()
  
  // 每秒更新时间
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  // 清除定时器
  if (timer) {
    clearInterval(timer)
  }
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
    .system-title {
      font-size: 20px;
      font-weight: 600;
      background: $gradient-primary;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 0;
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 24px;
    
    .current-time {
      display: flex;
      align-items: center;
      gap: 8px;
      color: $text-secondary;
      font-size: 14px;
      
      .el-icon {
        font-size: 16px;
      }
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
