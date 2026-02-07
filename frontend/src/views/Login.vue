<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
    
    <!-- 登录表单 -->
    <div class="login-box">
      <div class="login-header">
        <div class="logo-icon">
          <el-icon :size="48"><DataAnalysis /></el-icon>
        </div>
        <h1 class="system-title">Hadoop线上零售数仓用户行为分析系统</h1>
        <p class="system-subtitle">Data Analysis & Visualization Platform</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
        
        <div class="login-tips">
          <el-icon><InfoFilled /></el-icon>
          <span>测试账号：admin / 密码：123456</span>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, DataAnalysis, InfoFilled } from '@element-plus/icons-vue'

const router = useRouter()

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)
const loading = ref(false)

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      
      // 模拟登录延迟
      setTimeout(() => {
        // 验证账号密码
        if (loginForm.username === 'admin' && loginForm.password === '123456') {
          // 登录成功
          localStorage.setItem('token', 'mock-token-' + Date.now())
          localStorage.setItem('username', loginForm.username)
          
          ElMessage.success('登录成功！')
          
          // 跳转到 Dashboard
          router.push('/dashboard')
        } else {
          // 登录失败
          ElMessage.error('用户名或密码错误！')
        }
        
        loading.value = false
      }, 500)
    }
  })
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.login-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  
  // 背景装饰圆圈
  .bg-decoration {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
    
    .circle {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      animation: float 20s infinite ease-in-out;
      
      &.circle-1 {
        width: 300px;
        height: 300px;
        top: -100px;
        left: -100px;
        animation-delay: 0s;
      }
      
      &.circle-2 {
        width: 200px;
        height: 200px;
        bottom: -50px;
        right: 10%;
        animation-delay: 5s;
      }
      
      &.circle-3 {
        width: 150px;
        height: 150px;
        top: 50%;
        right: -50px;
        animation-delay: 10s;
      }
    }
  }
  
  .login-box {
    position: relative;
    z-index: 2;
    width: 420px;
    padding: 48px 40px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    .login-header {
      text-align: center;
      margin-bottom: 40px;
      
      .logo-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        margin-bottom: 20px;
        background: $gradient-primary;
        border-radius: 20px;
        color: white;
        box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
      }
      
      .system-title {
        font-size: 24px;
        font-weight: 600;
        color: $text-primary;
        margin: 0 0 8px 0;
      }
      
      .system-subtitle {
        font-size: 13px;
        color: $text-muted;
        margin: 0;
        letter-spacing: 1px;
      }
    }
    
    .login-form {
      .el-form-item {
        margin-bottom: 24px;
      }
      
      .login-btn {
        width: 100%;
        height: 48px;
        font-size: 16px;
        font-weight: 600;
        background: $gradient-primary;
        border: none;
        
        &:hover {
          filter: brightness(1.1);
        }
      }
    }
    
    .login-tips {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 16px;
      padding: 12px;
      background: rgba(24, 144, 255, 0.08);
      border-radius: 6px;
      font-size: 13px;
      color: #1890ff;
      
      .el-icon {
        font-size: 16px;
      }
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}
</style>
