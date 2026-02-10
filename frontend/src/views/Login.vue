<!--
  登录页面 (Login) - Clerk.com 风格
  功能：用户身份验证、系统入口
  设计风格：极简、轻盈、专业
  字体：Inter
-->
<template>
  <div class="clerk-container">
    <div class="clerk-card">
      <!-- Logo -->
      <div class="clerk-logo">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 3v18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M7 16l4-4 3 3 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="20" cy="6" r="2" fill="currentColor"/>
        </svg>
      </div>
      
      <!-- 标题 -->
      <div class="clerk-header">
        <h1 class="clerk-title">线上零售数据分析平台</h1>
      </div>
      
      <!-- 登录表单 -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="clerk-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <label class="clerk-label">用户名</label>
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            class="clerk-input"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <label class="clerk-label">密码</label>
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="输入您的密码"
            size="large"
            show-password
            class="clerk-input"
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>
        
        <el-button
          type="primary"
          size="large"
          class="clerk-button"
          :loading="loading"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登录' }}
        </el-button>
      </el-form>
      
      <!-- 底部链接 -->
      <div class="clerk-footer">
        <p class="clerk-footer-text">
          没有账号？
          <router-link to="/register" class="clerk-link">点击注册</router-link>
        </p>
      </div>
      

    </div>
  </div>
</template>

<script setup>
// ==================== 组件导入 ====================
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/service.js'

// ==================== 路由实例 ====================
const router = useRouter()

// ==================== 响应式数据 ====================

/**
 * 登录表单数据
 */
const loginForm = reactive({
  username: '',
  password: ''
})

/**
 * 表单验证规则
 */
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

/**
 * 表单引用
 * 用于调用 Element Plus 表单的验证方法
 */
const loginFormRef = ref(null)

/**
 * 加载状态
 * 控制登录按钮的 loading 状态，防止重复提交
 */
const loading = ref(false)

// ==================== 登录处理函数 ====================

/**
 * 处理用户登录
 */
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      
      try {
        // 调用后端登录API
        const res = await login({
          username: loginForm.username,
          password: loginForm.password
        })
        
        if (res.code === 200) {
          // 登录成功，保存Token和用户信息
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('currentUser', JSON.stringify(res.data.user))
          
          ElMessage.success('登录成功！')
          router.push('/ops-dashboard')
        } else {
          // 登录失败
          ElMessage.error(res.message || '用户名或密码错误！')
        }
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请检查网络连接或后端服务是否启动')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style lang="scss" scoped>
// ==================== 字体导入 ====================
// 导入 Google Fonts - Inter 字体（400/500/600 字重）
// Inter 是一款专为屏幕显示优化的现代无衬线字体，具有优秀的可读性
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

// ==================== 登录容器 ====================
// Clerk.com 风格的极简登录页面容器
.clerk-container {
  min-height: 100vh;                    // 最小高度为视口高度，确保全屏显示
  display: flex;                        // 使用 Flexbox 布局
  align-items: center;                  // 垂直居中
  justify-content: center;              // 水平居中
  background: #F9FAFB;                  // 纯色浅灰背景（Tailwind Gray 50）- v4.2 简化版本
  padding: 48px 20px;                   // 上下 48px，左右 20px 内边距
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;  // 字体栈：Inter → 系统字体
  
  // ==================== 登录卡片 ====================
  // 纯白卡片，包含 Logo、标题、表单和底部链接
  .clerk-card {
    width: 100%;                        // 宽度 100%（受 max-width 限制）
    max-width: 400px;                   // 最大宽度 400px
    background: #FFFFFF;                // 纯白背景
    border: 1px solid #E5E7EB;          // 浅灰边框（Gray 200）
    border-radius: 12px;                // 圆角 12px
    padding: 40px;                      // 内边距 40px
    // 多层阴影效果（Tailwind 风格）
    box-shadow: 
      0 1px 2px 0 rgba(0, 0, 0, 0.03),   // 第一层：细微阴影
      0 4px 8px 0 rgba(0, 0, 0, 0.04),   // 第二层：中等阴影
      0 12px 24px 0 rgba(0, 0, 0, 0.05); // 第三层：深度阴影
    
    // ==================== Logo 区域 ====================
    // 暖橙色渐变 Logo 容器，包含数据分析图标
    .clerk-logo {
      width: 40px;                      // 宽度 40px
      height: 40px;                     // 高度 40px
      margin: 0 auto 16px;              // 水平居中，下边距 16px
      display: flex;                    // Flexbox 布局
      align-items: center;              // 垂直居中
      justify-content: center;          // 水平居中
      background: linear-gradient(135deg, #E85D3D 0%, #F07A5F 100%);  // 橙色渐变
      border-radius: 8px;               // 圆角 8px
      box-shadow: 0 4px 12px rgba(232, 93, 61, 0.2);  // 橙色阴影
      
      svg {
        width: 24px;                    // SVG 图标宽度 24px
        height: 24px;                   // SVG 图标高度 24px
        color: #FFFFFF;                 // 白色图标
      }
    }
    
    // ==================== 标题区域 ====================
    // 包含主标题和副标题
    .clerk-header {
      text-align: center;               // 文本居中
      margin-bottom: 32px;              // 下边距 32px
      
      // 主标题：登录到电商数据分析平台
      .clerk-title {
        font-size: 24px;                // 字号 24px
        font-weight: 600;               // 字重 600（Semibold）
        color: #111827;                 // 深灰色（Gray 900）
        margin: 0 0 8px 0;              // 下边距 8px
        letter-spacing: -0.02em;        // 字间距 -0.02em（紧凑）
        line-height: 1.3;               // 行高 1.3
      }
      
      // 副标题：欢迎回来，请输入您的凭据
      .clerk-subtitle {
        font-size: 14px;                // 字号 14px
        font-weight: 400;               // 字重 400（Regular）
        color: #6B7280;                 // 中灰色（Gray 500）
        margin: 0;                      // 无外边距
        line-height: 1.5;               // 行高 1.5
      }
    }
    
    // ==================== 登录表单 ====================
    // Element Plus 表单组件，包含用户名、密码输入框和登录按钮
    .clerk-form {
      margin-bottom: 24px;              // 下边距 24px
      
      // 表单项间距
      .el-form-item {
        margin-bottom: 20px;            // 每个表单项下边距 20px
      }
      
      // 表单标签（用户名、密码）
      .clerk-label {
        display: block;                 // 块级元素
        font-size: 13px;                // 字号 13px
        font-weight: 500;               // 字重 500（Medium）
        color: #374151;                 // 深灰色（Gray 700）
        margin-bottom: 6px;             // 下边距 6px
      }
      
      // ==================== 输入框样式 ====================
      // 使用 :deep() 穿透 Element Plus 组件样式
      :deep(.clerk-input) {
        // 输入框包装器
        .el-input__wrapper {
          padding: 0 12px;              // 左右内边距 12px
          height: 40px;                 // 高度 40px
          background: #FFFFFF;          // 纯白背景
          border: 1px solid #E5E7EB;    // 浅灰边框（Gray 200）
          border-radius: 6px;           // 圆角 6px
          box-shadow: none;             // 无阴影
          transition: all 0.15s ease;   // 平滑过渡动画（150ms）
          
          // 悬停状态：背景变浅灰，边框变深
          &:hover {
            background: #F9FAFB;        // 浅灰背景（Gray 50）
            border-color: #D1D5DB;      // 中灰边框（Gray 300）
          }
          
          // 聚焦状态：橙色边框 + 橙色阴影
          &.is-focus {
            background: #FFFFFF;        // 纯白背景
            border-color: #E85D3D;      // 橙色边框
            box-shadow: 0 0 0 3px rgba(232, 93, 61, 0.1);  // 橙色发光阴影
          }
        }
        
        // 输入框内部元素
        .el-input__inner {
          color: #111827;               // 深灰色文字（Gray 900）
          font-size: 14px;              // 字号 14px
          
          // 占位符文字
          &::placeholder {
            color: #9CA3AF;             // 浅灰色（Gray 400）
          }
        }
        
        // 输入框前缀图标（用户图标、锁图标）
        .el-input__prefix {
          margin-right: 8px;            // 右边距 8px
          
          svg {
            width: 18px;                // SVG 图标宽度 18px
            height: 18px;               // SVG 图标高度 18px
            color: #6B7280;             // 中灰色（Gray 500）
          }
        }
      }
      
      // ==================== 登录按钮 ====================
      // 暖橙色渐变按钮，带悬停和点击效果
      .clerk-button {
        width: 100%;                    // 宽度 100%
        height: 40px;                   // 高度 40px
        background: linear-gradient(135deg, #E85D3D 0%, #F07A5F 100%);  // 橙色渐变
        border: none;                   // 无边框
        border-radius: 6px;             // 圆角 6px
        color: #FFFFFF;                 // 白色文字
        font-size: 14px;                // 字号 14px
        font-weight: 500;               // 字重 500（Medium）
        cursor: pointer;                // 鼠标指针
        transition: all 0.15s ease;     // 平滑过渡动画（150ms）
        margin-top: 8px;                // 上边距 8px
        box-shadow: 0 2px 8px rgba(232, 93, 61, 0.2);  // 橙色阴影
        
        // 悬停状态：渐变反转 + 阴影加深 + 上浮
        &:hover {
          background: linear-gradient(135deg, #D14B2E 0%, #E85D3D 100%);
          box-shadow: 0 4px 12px rgba(232, 93, 61, 0.3);
          transform: translateY(-1px);  // 上浮 1px
        }
        
        // 点击状态：轻微缩小 + 归位
        &:active {
          transform: scale(0.98) translateY(0);
        }
      }
    }
    
    // ==================== 底部链接区域 ====================
    // 包含"没有账号？点击注册"链接
    .clerk-footer {
      text-align: center;               // 文本居中
      padding-top: 24px;                // 上内边距 24px
      border-top: 1px solid #E5E7EB;    // 顶部边框（Gray 200）
      
      // 底部文字
      .clerk-footer-text {
        font-size: 14px;                // 字号 14px
        color: #6B7280;                 // 中灰色（Gray 500）
        margin: 0;                      // 无外边距
        
        // 注册链接
        .clerk-link {
          color: #E85D3D;               // 橙色
          font-weight: 500;             // 字重 500（Medium）
          text-decoration: none;        // 无下划线
          transition: opacity 0.15s ease;  // 透明度过渡动画（150ms）
          
          // 悬停状态：透明度降低
          &:hover {
            opacity: 0.7;               // 70% 不透明度
          }
        }
      }
    }
    
  }
  
  // ==================== 响应式设计 ====================
  // 移动端适配（屏幕宽度 < 640px）
  @media (max-width: 640px) {
    padding: 20px;                      // 减少容器内边距到 20px
    
    .clerk-card {
      padding: 32px 24px;               // 减少卡片内边距（上下 32px，左右 24px）
    }
  }
}
</style>
