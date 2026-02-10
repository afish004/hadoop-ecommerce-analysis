<!--
  注册页面 (Register) - Clerk.com 风格
  功能：用户注册、账号创建
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
        <p class="clerk-subtitle">开始使用数据分析平台</p>
      </div>
      
      <!-- 注册表单 -->
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="clerk-form"
        @submit.prevent="handleRegister"
      >
        <el-form-item prop="name">
          <label class="clerk-label">姓名</label>
          <el-input
            v-model="registerForm.name"
            placeholder="张三"
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
        
        <el-form-item prop="email">
          <label class="clerk-label">邮箱</label>
          <el-input
            v-model="registerForm.email"
            type="email"
            placeholder="your@email.com"
            size="large"
            class="clerk-input"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M3 7l9 6 9-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <label class="clerk-label">密码</label>
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="至少6位字符"
            size="large"
            show-password
            class="clerk-input"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <label class="clerk-label">确认密码</label>
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="再次输入密码"
            size="large"
            show-password
            class="clerk-input"
            @keyup.enter="handleRegister"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
          @click="handleRegister"
        >
          {{ loading ? '注册中...' : '创建账号' }}
        </el-button>
      </el-form>
      
      <!-- 底部链接 -->
      <div class="clerk-footer">
        <p class="clerk-footer-text">
          已有账号？
          <router-link to="/login" class="clerk-link">立即登录</router-link>
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
import { register } from '@/api/service.js'

// ==================== 路由实例 ====================
const router = useRouter()

// ==================== 响应式数据 ====================

/**
 * 注册表单数据
 * @property {String} name - 用户姓名（将作为 username 保存）
 * @property {String} email - 用户邮箱
 * @property {String} password - 用户密码
 * @property {String} confirmPassword - 确认密码
 */
const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

/**
 * 自定义验证器：确认密码
 * 验证确认密码是否与密码一致
 * 
 * @param {Object} _rule - 验证规则对象（未使用，但 Element Plus 要求）
 * @param {String} value - 当前输入的确认密码值
 * @param {Function} callback - 验证回调函数
 */
const validateConfirmPassword = (_rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

/**
 * 表单验证规则
 * 定义每个字段的验证规则
 */
const registerRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, message: '姓名至少2个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

/**
 * 表单引用
 * 用于调用 Element Plus 表单的验证方法
 */
const registerFormRef = ref(null)

/**
 * 加载状态
 * 控制注册按钮的 loading 状态，防止重复提交
 */
const loading = ref(false)

// ==================== 注册处理函数 ====================

/**
 * 处理用户注册
 */
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      
      try {
        // 调用后端注册API
        const res = await register({
          username: registerForm.name,
          email: registerForm.email,
          password: registerForm.password
        })
        
        if (res.code === 200) {
          // 注册成功
          ElMessage.success('注册成功！即将跳转到登录页面...')
          
          // 2秒后跳转到登录页
          setTimeout(() => {
            router.push('/login')
          }, 2000)
        } else {
          // 注册失败
          ElMessage.error(res.message || '注册失败')
        }
      } catch (error) {
        console.error('注册失败:', error)
        ElMessage.error('注册失败，请检查网络连接或后端服务是否启动')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style lang="scss" scoped>
// 字体导入
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.clerk-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F9FAFB;
  padding: 48px 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  
  .clerk-card {
    width: 100%;
    max-width: 400px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 40px;
    box-shadow: 
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 4px 8px 0 rgba(0, 0, 0, 0.04),
      0 12px 24px 0 rgba(0, 0, 0, 0.05);
    
    // Logo
    .clerk-logo {
      width: 40px;
      height: 40px;
      margin: 0 auto 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #E85D3D 0%, #F07A5F 100%);
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(232, 93, 61, 0.2);
      
      svg {
        width: 24px;
        height: 24px;
        color: #FFFFFF;
      }
    }
    
    // 标题区域
    .clerk-header {
      text-align: center;
      margin-bottom: 32px;
      
      .clerk-title {
        font-size: 24px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 8px 0;
        letter-spacing: -0.02em;
        line-height: 1.3;
      }
      
      .clerk-subtitle {
        font-size: 14px;
        font-weight: 400;
        color: #6B7280;
        margin: 0;
        line-height: 1.5;
      }
    }
    
    // 表单
    .clerk-form {
      margin-bottom: 24px;
      
      .el-form-item {
        margin-bottom: 20px;
      }
      
      .clerk-label {
        display: block;
        font-size: 13px;
        font-weight: 500;
        color: #374151;
        margin-bottom: 6px;
      }
      
      :deep(.clerk-input) {
        .el-input__wrapper {
          padding: 0 12px;
          height: 40px;
          background: #FFFFFF;
          border: 1px solid #E5E7EB;
          border-radius: 6px;
          box-shadow: none;
          transition: all 0.15s ease;
          
          &:hover {
            background: #F9FAFB;
            border-color: #D1D5DB;
          }
          
          &.is-focus {
            background: #FFFFFF;
            border-color: #E85D3D;
            box-shadow: 0 0 0 3px rgba(232, 93, 61, 0.1);
          }
        }
        
        .el-input__inner {
          color: #111827;
          font-size: 14px;
          
          &::placeholder {
            color: #9CA3AF;
          }
        }
        
        .el-input__prefix {
          margin-right: 8px;
          
          svg {
            width: 18px;
            height: 18px;
            color: #6B7280;
          }
        }
      }
      
      .clerk-button {
        width: 100%;
        height: 40px;
        background: linear-gradient(135deg, #E85D3D 0%, #F07A5F 100%);
        border: none;
        border-radius: 6px;
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
        margin-top: 8px;
        box-shadow: 0 2px 8px rgba(232, 93, 61, 0.2);
        
        &:hover {
          background: linear-gradient(135deg, #D14B2E 0%, #E85D3D 100%);
          box-shadow: 0 4px 12px rgba(232, 93, 61, 0.3);
          transform: translateY(-1px);
        }
        
        &:active {
          transform: scale(0.98) translateY(0);
        }
      }
    }
    
    // 底部链接
    .clerk-footer {
      text-align: center;
      padding-top: 24px;
      border-top: 1px solid #E5E7EB;
      
      .clerk-footer-text {
        font-size: 14px;
        color: #6B7280;
        margin: 0;
        
        .clerk-link {
          color: #E85D3D;
          font-weight: 500;
          text-decoration: none;
          transition: opacity 0.15s ease;
          
          &:hover {
            opacity: 0.7;
          }
        }
      }
    }
  }
  
  // 响应式
  @media (max-width: 640px) {
    padding: 20px;
    
    .clerk-card {
      padding: 32px 24px;
    }
  }
}
</style>
