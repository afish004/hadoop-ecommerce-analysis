# 开发指南

## 📚 目录

1. [项目结构](#项目结构)
2. [代码规范](#代码规范)
3. [组件开发](#组件开发)
4. [路由配置](#路由配置)
5. [样式管理](#样式管理)
6. [常见问题](#常见问题)

---

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   │   ├── service.js    # 接口服务
│   │   └── mockData.js   # 模拟数据
│   ├── assets/           # 静态资源
│   │   └── styles/       # 全局样式
│   │       ├── global.scss     # 全局样式
│   │       └── variables.scss  # 样式变量
│   ├── components/       # 公共组件
│   │   ├── BarChart.vue
│   │   ├── LineChart.vue
│   │   └── ...
│   ├── layout/           # 布局组件
│   │   ├── Header.vue    # 顶部导航
│   │   ├── Sidebar.vue   # 侧边栏
│   │   └── MainLayout.vue
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── views/            # 页面组件
│   │   ├── Dashboard.vue
│   │   ├── Login.vue
│   │   └── ...
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── public/               # 公共资源
├── docs/                 # 项目文档
└── package.json          # 依赖配置
```

---

## 代码规范

### 1. 命名规范

#### 文件命名
- **组件文件**: 使用 PascalCase（大驼峰）
  - ✅ `Header.vue`, `UserProfile.vue`
  - ❌ `header.vue`, `user-profile.vue`

- **工具文件**: 使用 camelCase（小驼峰）
  - ✅ `utils.js`, `formatDate.js`
  - ❌ `Utils.js`, `format-date.js`

#### 变量命名
```javascript
// 常量：全大写 + 下划线
const API_BASE_URL = 'https://api.example.com'

// 普通变量：小驼峰
const userName = 'admin'
const isLoading = false

// 组件名：大驼峰
const MyComponent = defineComponent({...})

// 私有变量：下划线开头
const _privateVar = 'private'
```

### 2. 注释规范

#### 组件注释
```vue
/**
 * 组件名称
 * 功能描述：简要说明组件的作用
 * 使用示例：<ComponentName :prop="value" />
 */
<script setup>
// 组件代码
</script>
```

#### 函数注释
```javascript
/**
 * 函数功能描述
 * @param {string} name - 参数说明
 * @param {number} age - 参数说明
 * @returns {Object} 返回值说明
 * @throws {Error} 可能抛出的错误
 */
function getUserInfo(name, age) {
  // 函数实现
}
```

#### 代码块注释
```javascript
// ==================== 功能模块名称 ====================
// 模块说明

// 单行注释：说明下一行代码的作用
const result = calculate()

/* 
 * 多行注释：
 * 1. 说明复杂逻辑
 * 2. 列举注意事项
 */
```

### 3. Vue 3 Composition API 规范

#### 推荐的代码组织顺序
```vue
<script setup>
// 1. 导入依赖
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 2. 定义 props 和 emits
const props = defineProps({
  title: String
})
const emit = defineEmits(['update'])

// 3. 响应式数据
const count = ref(0)
const doubleCount = computed(() => count.value * 2)

// 4. 方法定义
const increment = () => {
  count.value++
}

// 5. 生命周期钩子
onMounted(() => {
  console.log('Component mounted')
})
</script>
```

---

## 组件开发

### 1. Header 组件使用示例

```vue
<template>
  <MainLayout>
    <template #header>
      <Header />
    </template>
    <template #default>
      <!-- 页面内容 -->
    </template>
  </MainLayout>
</template>

<script setup>
import Header from '@/layout/Header.vue'
import MainLayout from '@/layout/MainLayout.vue'
</script>
```

### 2. 路由配置要求

为了让面包屑导航正常工作，需要在路由中配置 `meta.title`：

```javascript
// router/index.js
const routes = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '数据概览',        // 面包屑显示的标题
      requiresAuth: true,       // 是否需要登录
      icon: 'Dashboard'         // 菜单图标（可选）
    }
  },
  {
    path: '/user-insight',
    name: 'UserInsight',
    component: () => import('@/views/UserInsight.vue'),
    meta: {
      title: '用户画像',
      requiresAuth: true
    }
  }
]
```

### 3. 全屏功能集成

如果需要在其他组件中使用全屏功能：

```vue
<script setup>
import { ref } from 'vue'

const isFullscreen = ref(false)

// 进入全屏
const enterFullscreen = async () => {
  try {
    await document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } catch (err) {
    console.error('无法进入全屏:', err)
  }
}

// 退出全屏
const exitFullscreen = async () => {
  try {
    await document.exitFullscreen()
    isFullscreen.value = false
  } catch (err) {
    console.error('无法退出全屏:', err)
  }
}

// 监听全屏状态变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
}

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})
</script>
```

---

## 路由配置

### 路由守卫示例

```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      // 未登录，跳转到登录页
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})
```

---

## 样式管理

### 1. 使用 SCSS 变量

```scss
// 在组件中使用全局变量
<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;

.my-component {
  color: $primary-color;
  background: $bg-primary;
  border: 1px solid $border-color;
}
</style>
```

### 2. 全局样式变量

```scss
// variables.scss
$primary-color: #1890ff;
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #f5222d;

$text-primary: #333333;
$text-secondary: #666666;
$text-disabled: #999999;

$bg-primary: #ffffff;
$bg-secondary: #f5f5f5;
$border-color: #e8e8e8;
```

### 3. 响应式设计

```scss
// 使用媒体查询
.header {
  padding: 0 24px;
  
  // 平板设备
  @media (max-width: 768px) {
    padding: 0 16px;
  }
  
  // 手机设备
  @media (max-width: 480px) {
    padding: 0 12px;
  }
}
```

---

## 常见问题

### 1. 面包屑不显示当前页面标题

**原因**: 路由配置中缺少 `meta.title` 字段

**解决方案**:
```javascript
{
  path: '/your-page',
  meta: {
    title: '你的页面标题'  // 添加这一行
  }
}
```

### 2. 全屏功能无法使用

**可能原因**:
1. 浏览器不支持 Fullscreen API
2. 没有用户交互触发
3. 页面在 iframe 中且没有权限

**解决方案**:
```javascript
// 检查浏览器支持
if (document.fullscreenEnabled) {
  // 支持全屏
} else {
  console.warn('浏览器不支持全屏功能')
}
```

### 3. 样式不生效

**检查清单**:
- [ ] 是否添加了 `scoped` 属性
- [ ] 是否正确导入了 SCSS 变量
- [ ] 是否有更高优先级的样式覆盖
- [ ] 浏览器缓存是否清除

### 4. 组件卸载后定时器仍在运行

**原因**: 忘记在 `onUnmounted` 中清理定时器

**解决方案**:
```javascript
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    // 定时任务
  }, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)  // 必须清理
  }
})
```

---

## 开发工具推荐

### VS Code 插件
- **Volar**: Vue 3 官方插件
- **ESLint**: 代码检查
- **Prettier**: 代码格式化
- **SCSS IntelliSense**: SCSS 智能提示

### 浏览器插件
- **Vue.js devtools**: Vue 调试工具
- **React Developer Tools**: 如果使用 React

---

## 参考资源

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Vue Router 文档](https://router.vuejs.org/zh/)
- [MDN Web Docs - Fullscreen API](https://developer.mozilla.org/zh-CN/docs/Web/API/Fullscreen_API)

---

**最后更新**: 2026-01-19
