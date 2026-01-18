# 设计文档：基于Hadoop的电商用户行为分析系统（前端工程）

## 概述 (Overview)

本设计文档描述了一个基于 Vue3 的电商用户行为分析可视化系统的前端架构。该系统是本科毕业设计项目的一部分，主题为《基于Hadoop的电商用户行为分析系统设计与实现》。

### 设计目标

1. **高质量可视化展示**：构建专业的数据可视化界面，展示电商用户行为分析结果
2. **Mock 数据驱动**：当前阶段使用模拟数据，但数据结构严格对应真实数据集字段
3. **组件化架构**：每个图表独立封装，便于维护和复用
4. **深色科技风格**：符合大数据看板的视觉体验

### 技术选型

- **前端框架**：Vue 3 + Vite（快速构建）
- **UI 组件库**：Element Plus（布局、表格、侧边栏）
- **可视化库**：ECharts 5.x（所有图表展示）
- **HTTP 客户端**：Axios（数据请求）
- **路由管理**：Vue Router 4
- **状态管理**：Pinia（轻量级状态管理）

## 架构设计 (Architecture)

### 整体架构

系统采用经典的前端 SPA（单页应用）架构，分为以下几层：

```
┌─────────────────────────────────────────┐
│         视图层 (View Layer)              │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Login    │  │Dashboard │  │Product ││
│  │ Page     │  │ Page     │  │ Page   ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│       组件层 (Component Layer)           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Funnel   │  │ LineChart│  │WordCloud│
│  │ Chart    │  │ Component│  │Component││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         API 层 (API Layer)               │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Mock     │  │ Axios    │  │ Request││
│  │ Data     │  │ Instance │  │ Utils  ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

### 目录结构


```
src/
├── assets/              # 静态资源
│   ├── styles/         # 全局样式
│   │   ├── variables.scss   # 深色主题变量
│   │   └── global.scss      # 全局样式
│   └── images/         # 图片资源
├── components/          # 可复用组件
│   ├── charts/         # 图表组件
│   │   ├── FunnelChart.vue      # 漏斗图
│   │   ├── LineChart.vue        # 折线图
│   │   ├── PieChart.vue         # 饼图
│   │   ├── BarChart.vue         # 柱状图
│   │   ├── WordCloud.vue        # 词云图
│   │   ├── ScatterChart.vue     # 散点图
│   │   └── RoseChart.vue        # 玫瑰图
│   ├── layout/         # 布局组件
│   │   ├── MainLayout.vue       # 主布局
│   │   ├── Sidebar.vue          # 侧边栏
│   │   └── Header.vue           # 顶部栏
│   └── common/         # 通用组件
│       ├── MetricCard.vue       # 指标卡片
│       └── ParticleBackground.vue # 粒子背景
├── views/              # 页面视图
│   ├── Login.vue       # 登录页
│   ├── Dashboard.vue   # 综合驾驶舱
│   ├── Conversion.vue  # 流量与转化
│   ├── Product.vue     # 商品与品牌
│   ├── UserInsight.vue # 用户价值分层
│   └── Prediction.vue  # 趋势预测
├── api/                # API 接口
│   ├── mock/           # Mock 数据
│   │   ├── dashboard.js    # 驾驶舱数据
│   │   ├── conversion.js   # 转化数据
│   │   ├── product.js      # 商品数据
│   │   ├── userInsight.js  # 用户洞察数据
│   │   └── prediction.js   # 预测数据
│   └── request.js      # Axios 实例配置
├── router/             # 路由配置
│   └── index.js
├── stores/             # Pinia 状态管理
│   └── user.js         # 用户状态
├── utils/              # 工具函数
│   ├── chartTheme.js   # ECharts 深色主题
│   └── dateFormat.js   # 日期格式化
├── App.vue
└── main.js
```

### 路由设计

系统包含两种布局模式：

1. **独立页面布局**：登录页（无侧边栏和顶部栏）
2. **主布局**：其他所有页面（包含侧边栏和顶部栏）

路由配置：

```javascript
routes: [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'conversion',
        name: 'Conversion',
        component: () => import('@/views/Conversion.vue')
      },
      {
        path: 'product',
        name: 'Product',
        component: () => import('@/views/Product.vue')
      },
      {
        path: 'user-insight',
        name: 'UserInsight',
        component: () => import('@/views/UserInsight.vue')
      },
      {
        path: 'prediction',
        name: 'Prediction',
        component: () => import('@/views/Prediction.vue')
      }
    ]
  }
]
```

## 组件与接口 (Components and Interfaces)

### 核心组件设计

#### 1. 布局组件

**MainLayout.vue**
- **职责**：提供主布局框架，包含侧边栏和顶部栏
- **Props**：无
- **Emits**：无
- **插槽**：default（内容区域）

**Sidebar.vue**
- **职责**：侧边栏导航菜单，支持分组显示
- **Props**：
  - `collapsed: boolean` - 是否折叠
- **Emits**：
  - `update:collapsed` - 折叠状态变化
- **菜单结构**：
  ```javascript
  menuItems: [
    {
      title: '综合态势',
      icon: 'Odometer',
      path: '/dashboard'
    },
    {
      groupTitle: '核心分析',
      children: [
        { title: '流量与转化', icon: 'TrendCharts', path: '/conversion' },
        { title: '商品与品牌', icon: 'Goods', path: '/product' },
        { title: '用户价值分层', icon: 'User', path: '/user-insight' }
      ]
    },
    {
      groupTitle: '智能决策',
      children: [
        { title: '趋势预测', icon: 'MagicStick', path: '/prediction' }
      ]
    }
  ]
  ```

**Header.vue**
- **职责**：顶部栏，显示系统标题、当前时间、用户信息
- **Props**：无
- **Emits**：
  - `logout` - 退出登录
- **功能**：
  - 显示系统标题："Hadoop电商行为分析系统"
  - 实时显示当前时间（每秒更新）
  - 显示管理员头像和退出按钮

#### 2. 图表组件

所有图表组件遵循统一的设计模式：

**通用 Props**：
- `data: Object | Array` - 图表数据
- `height: String` - 图表高度（默认 '400px'）
- `loading: Boolean` - 加载状态

**通用方法**：
- `initChart()` - 初始化 ECharts 实例
- `updateChart()` - 更新图表数据
- `resizeChart()` - 响应式调整图表大小

**FunnelChart.vue（漏斗图）**
- **用途**：展示用户行为转化漏斗
- **数据格式**：
  ```javascript
  {
    data: [
      { name: '浏览', value: 10000 },
      { name: '加购', value: 3000 },
      { name: '下单', value: 1000 }
    ]
  }
  ```

**LineChart.vue（折线图）**
- **用途**：展示时间序列数据（PV/UV 趋势、预测曲线）
- **数据格式**：
  ```javascript
  {
    xAxis: ['00:00', '01:00', ...],
    series: [
      { name: 'PV', data: [100, 200, ...] },
      { name: 'UV', data: [50, 100, ...] }
    ]
  }
  ```
- **特殊功能**：支持预测数据的虚线显示和置信区间阴影

**PieChart.vue（饼图）**
- **用途**：展示分类占比（品类销售、用户分层）
- **数据格式**：
  ```javascript
  {
    data: [
      { name: '电子产品', value: 5000 },
      { name: '服装', value: 3000 }
    ]
  }
  ```

**BarChart.vue（柱状图）**
- **用途**：展示排名数据（品牌 TOP10）
- **数据格式**：
  ```javascript
  {
    yAxis: ['小米', '苹果', '华为', ...],
    data: [5000, 4500, 4000, ...]
  }
  ```

**WordCloud.vue（词云图）**
- **用途**：展示品类关键词热度
- **数据格式**：
  ```javascript
  {
    data: [
      { name: 'smartphone', value: 1000 },
      { name: 'laptop', value: 800 }
    ]
  }
  ```

**ScatterChart.vue（散点图）**
- **用途**：价格敏感度分析
- **数据格式**：
  ```javascript
  {
    data: [
      [price1, sales1],
      [price2, sales2]
    ]
  }
  ```

**RoseChart.vue（玫瑰图）**
- **用途**：行为分布展示
- **数据格式**：
  ```javascript
  {
    data: [
      { name: 'view', value: 10000 },
      { name: 'cart', value: 3000 },
      { name: 'purchase', value: 1000 }
    ]
  }
  ```

#### 3. 通用组件

**MetricCard.vue（指标卡片）**
- **职责**：展示核心指标（GMV、PV、UV）
- **Props**：
  - `title: String` - 指标名称
  - `value: Number | String` - 指标值
  - `unit: String` - 单位
  - `icon: String` - 图标名称
  - `trend: Number` - 趋势百分比（可选）
- **样式**：深色背景，渐变边框，悬停效果

**ParticleBackground.vue（粒子背景）**
- **职责**：登录页科技感粒子动画背景
- **实现**：使用 Canvas 绘制动态粒子效果

### API 接口设计

#### Mock 数据生成器

所有 Mock 数据必须基于 9 个核心字段生成，确保逻辑自洽。

**dashboard.js**
```javascript
export function getDashboardData() {
  return {
    metrics: {
      gmv: 12580000,      // 总销售额
      pv: 1580000,        // 总访问量
      uv: 350000          // 独立访客数
    },
    pvuvTrend: {
      xAxis: generateHourLabels(),  // 24小时标签
      pv: generateTrendData(24, 50000, 80000),
      uv: generateTrendData(24, 10000, 20000)
    },
    categorySales: [
      { name: 'electronics.smartphone', value: 4500000 },
      { name: 'appliances.kitchen', value: 3200000 },
      { name: 'computers.notebook', value: 2800000 }
    ]
  }
}
```

**conversion.js**
```javascript
export function getConversionData() {
  return {
    funnel: [
      { name: '浏览', value: 1000000 },
      { name: '加购', value: 300000 },
      { name: '下单', value: 100000 }
    ],
    eventDistribution: [
      { name: 'view', value: 1000000 },
      { name: 'cart', value: 300000 },
      { name: 'purchase', value: 100000 },
      { name: 'remove_from_cart', value: 50000 }
    ]
  }
}
```

**product.js**
```javascript
export function getProductData() {
  return {
    brandTop10: {
      brands: ['xiaomi', 'apple', 'samsung', 'huawei', ...],
      sales: [50000, 48000, 45000, 42000, ...]
    },
    categoryWordCloud: [
      { name: 'smartphone', value: 1000 },
      { name: 'laptop', value: 800 },
      { name: 'tablet', value: 600 }
    ],
    priceSensitivity: generateScatterData(100)  // 100个数据点
  }
}
```

**userInsight.js**
```javascript
export function getUserInsightData() {
  return {
    userSegmentation: [
      { name: '高价值用户', value: 15000 },
      { name: '潜力用户', value: 50000 },
      { name: '挽留用户', value: 80000 },
      { name: '流失用户', value: 205000 }
    ]
  }
}
```

**prediction.js**
```javascript
export function getPredictionData() {
  return {
    historicalData: {
      dates: generateDateLabels(-30, 0),  // 过去30天
      pv: generateTrendData(30, 50000, 80000)
    },
    forecastData: {
      dates: generateDateLabels(1, 7),    // 未来7天
      pv: generateTrendData(7, 55000, 85000),
      confidenceInterval: {
        upper: generateTrendData(7, 60000, 90000),
        lower: generateTrendData(7, 50000, 80000)
      }
    }
  }
}
```

#### Axios 配置

**request.js**
```javascript
import axios from 'axios'

const service = axios.create({
  baseURL: '/api',
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加 token（如果存在）
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 统一错误处理
    if (error.response?.status === 401) {
      // 跳转到登录页
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default service
```

## 数据模型 (Data Models)

### 核心数据字段

系统所有数据基于以下 9 个字段构建：

```typescript
interface UserBehaviorEvent {
  event_time: string        // 时间戳，格式：'2024-01-01 12:00:00'
  event_type: EventType     // 行为类型枚举
  product_id: number        // 商品ID
  category_id: number       // 品类ID
  category_code: string     // 品类代码，如 'electronics.smartphone'
  brand: string             // 品牌名称
  price: number             // 价格（元）
  user_id: number           // 用户ID
  user_session: string      // 会话ID
}

enum EventType {
  VIEW = 'view',                    // 浏览
  CART = 'cart',                    // 加购
  PURCHASE = 'purchase',            // 购买
  REMOVE_FROM_CART = 'remove_from_cart'  // 移除购物车
}
```

### 聚合数据模型

**指标数据**
```typescript
interface MetricsData {
  gmv: number          // 总销售额（Gross Merchandise Volume）
  pv: number           // 页面浏览量（Page View）
  uv: number           // 独立访客数（Unique Visitor）
  conversionRate?: number  // 转化率（可选）
}
```

**时间序列数据**
```typescript
interface TimeSeriesData {
  xAxis: string[]      // 时间标签数组
  series: SeriesItem[]
}

interface SeriesItem {
  name: string         // 系列名称
  data: number[]       // 数据数组
  type?: string        // 图表类型（line/bar）
  lineStyle?: object   // 线条样式（实线/虚线）
}
```

**分类数据**
```typescript
interface CategoryData {
  name: string         // 分类名称
  value: number        // 数值
}
```

**预测数据**
```typescript
interface ForecastData {
  historical: TimeSeriesData    // 历史数据
  forecast: TimeSeriesData      // 预测数据
  confidenceInterval?: {        // 置信区间
    upper: number[]
    lower: number[]
  }
}
```

### 用户状态模型

```typescript
interface UserState {
  isAuthenticated: boolean   // 是否已认证
  username: string          // 用户名
  role: string              // 角色（admin）
  loginTime: string         // 登录时间
}
```

## 正确性属性 (Correctness Properties)

属性是一种特征或行为，应该在系统的所有有效执行中保持为真——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。

### 属性 1：登录凭据验证

**对于任意**输入的用户名和密码组合，当用户名为 "admin" 且密码为 "admin" 时，系统应验证成功并跳转到 `/dashboard` 页面；否则应显示错误提示并保持在登录页面。

**验证需求**：需求 1.2, 1.3

### 属性 2：漏斗数据递减不变量

**对于任意**生成的转化漏斗数据，必须满足：浏览数量 ≥ 加购数量 ≥ 下单数量。这个不变量确保转化路径的逻辑一致性。

**验证需求**：需求 3.1, 8.2

### 属性 3：Mock 数据结构完整性

**对于任意**Mock 数据生成函数的输出，返回的每个用户行为事件对象必须包含且仅包含 9 个核心字段：`event_time`、`event_type`、`product_id`、`category_id`、`category_code`、`brand`、`price`、`user_id`、`user_session`。

**验证需求**：需求 8.1

### 属性 4：图表组件初始化

**对于任意**图表组件（FunnelChart、LineChart、PieChart 等），当组件挂载并接收有效数据时，应成功初始化 ECharts 实例并渲染图表内容。

**验证需求**：需求 2.2, 2.3, 3.1, 3.2, 4.1, 4.2, 4.3, 5.1, 6.1, 9.1

### 属性 5：图表响应式更新

**对于任意**图表组件，当其 `data` prop 发生变化时，图表应自动重新渲染以反映新数据。

**验证需求**：需求 9.2

### 属性 6：图表响应式布局

**对于任意**图表组件，当浏览器窗口大小改变时，图表应自动调整尺寸以适应新的容器大小。

**验证需求**：需求 9.3

### 属性 7：路由导航状态同步

**对于任意**侧边栏菜单项，当用户点击该菜单项时，系统应导航到对应路由，并且该菜单项应处于高亮选中状态。

**验证需求**：需求 7.2

### 属性 8：预测数据线型区分

**对于任意**包含历史数据和预测数据的折线图，历史数据应使用实线渲染，预测数据应使用虚线渲染，且预测数据应包含置信区间阴影。

**验证需求**：需求 6.1, 6.2

### 属性 9：时间显示实时更新

**对于任意**顶部栏组件实例，当组件挂载后，显示的当前时间应每秒更新一次，确保时间显示的实时性。

**验证需求**：需求 7.3

### 属性 10：RFM 分层数据完整性

**对于任意**基于 `user_id` 和 `price` 生成的 RFM 用户分层数据，必须包含至少以下分类：高价值用户、潜力用户、挽留用户、流失用户，且每个分类的用户数量应大于 0。

**验证需求**：需求 5.2

## 错误处理 (Error Handling)

### 1. 网络请求错误

**场景**：API 请求失败或超时

**处理策略**：
- 在 Axios 响应拦截器中统一捕获错误
- 显示用户友好的错误提示（使用 Element Plus 的 Message 组件）
- 对于 401 未授权错误，自动跳转到登录页
- 对于 5xx 服务器错误，提示"服务暂时不可用，请稍后重试"
- 记录错误日志到控制台（开发环境）

**实现示例**：
```javascript
service.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          router.push('/login')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误，请稍后重试')
          break
        default:
          ElMessage.error('请求失败，请检查网络连接')
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)
```

### 2. 图表渲染错误

**场景**：ECharts 初始化失败或数据格式错误

**处理策略**：
- 在图表组件中使用 try-catch 包裹 ECharts 初始化代码
- 验证传入数据的格式和完整性
- 如果数据无效，显示占位符提示"暂无数据"
- 在控制台输出详细错误信息（开发环境）

**实现示例**：
```javascript
const initChart = () => {
  try {
    if (!props.data || !Array.isArray(props.data)) {
      console.warn('Invalid chart data:', props.data)
      return
    }
    
    const chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption(getChartOption())
  } catch (error) {
    console.error('Chart initialization failed:', error)
    ElMessage.error('图表加载失败')
  }
}
```

### 3. 路由守卫错误

**场景**：未登录用户访问受保护页面

**处理策略**：
- 在路由全局前置守卫中检查认证状态
- 未登录用户自动重定向到登录页
- 保存原始目标路由，登录成功后跳转回去

**实现示例**：
```javascript
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})
```

### 4. 数据加载状态

**场景**：数据加载过程中的用户体验

**处理策略**：
- 所有页面和图表组件支持 `loading` 状态
- 使用 Element Plus 的 Loading 指令或骨架屏
- 设置合理的超时时间（5秒）
- 加载失败后提供重试按钮

**实现示例**：
```javascript
const loading = ref(false)
const loadData = async () => {
  loading.value = true
  try {
    const data = await getDashboardData()
    dashboardData.value = data
  } catch (error) {
    ElMessage.error('数据加载失败')
  } finally {
    loading.value = false
  }
}
```

### 5. 边界情况处理

**空数据处理**：
- 当 Mock 数据返回空数组或 null 时，显示"暂无数据"占位符
- 图表组件优雅降级，不显示错误信息

**数据异常值处理**：
- 对于价格、数量等数值字段，过滤掉负数和 NaN
- 对于时间字段，验证格式有效性

**浏览器兼容性**：
- 使用 Vite 的自动 polyfill 功能
- 在不支持 ECharts 的浏览器中显示降级提示

## 测试策略 (Testing Strategy)

### 测试方法论

本项目采用**双重测试方法**：

1. **单元测试**：验证具体示例、边界情况和错误条件
2. **属性测试**：验证跨所有输入的通用属性

两者互补，共同确保全面覆盖：
- 单元测试捕获具体的 bug
- 属性测试验证通用正确性

### 单元测试策略

**测试框架**：Vitest（与 Vite 原生集成）

**测试范围**：
- **组件测试**：使用 Vue Test Utils 测试组件渲染和交互
- **工具函数测试**：测试日期格式化、数据生成等纯函数
- **路由测试**：测试路由守卫和导航逻辑
- **状态管理测试**：测试 Pinia store 的 actions 和 getters

**单元测试重点**：
- 登录页面的表单验证和提交逻辑
- 侧边栏菜单的展开/折叠和路由跳转
- 指标卡片的数据格式化显示
- Mock 数据生成器的边界情况（空数组、异常值）

**示例测试用例**：
```javascript
// 测试登录验证逻辑
describe('Login Component', () => {
  it('should navigate to dashboard with correct credentials', async () => {
    const wrapper = mount(Login)
    await wrapper.find('input[type="text"]').setValue('admin')
    await wrapper.find('input[type="password"]').setValue('admin')
    await wrapper.find('button').trigger('click')
    
    expect(router.currentRoute.value.path).toBe('/dashboard')
  })
  
  it('should show error message with incorrect credentials', async () => {
    const wrapper = mount(Login)
    await wrapper.find('input[type="text"]').setValue('wrong')
    await wrapper.find('input[type="password"]').setValue('wrong')
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.find('.error-message').exists()).toBe(true)
  })
})
```

### 属性测试策略

**测试框架**：fast-check（JavaScript 的属性测试库）

**配置要求**：
- 每个属性测试至少运行 **100 次迭代**（由于随机化）
- 每个测试必须引用其设计文档中的属性编号
- 标签格式：`Feature: graduation-development-standards, Property {number}: {property_text}`

**属性测试重点**：

**属性 2：漏斗数据递减不变量**
```javascript
import fc from 'fast-check'

// Feature: graduation-development-standards, Property 2: 漏斗数据递减不变量
test('funnel data must be in descending order', () => {
  fc.assert(
    fc.property(
      fc.record({
        view: fc.integer({ min: 1000, max: 1000000 }),
        cart: fc.integer({ min: 100, max: 500000 }),
        purchase: fc.integer({ min: 10, max: 100000 })
      }),
      (data) => {
        const funnel = generateFunnelData(data)
        return funnel[0].value >= funnel[1].value && 
               funnel[1].value >= funnel[2].value
      }
    ),
    { numRuns: 100 }
  )
})
```

**属性 3：Mock 数据结构完整性**
```javascript
// Feature: graduation-development-standards, Property 3: Mock 数据结构完整性
test('all mock events must have 9 required fields', () => {
  fc.assert(
    fc.property(
      fc.integer({ min: 1, max: 100 }),
      (count) => {
        const events = generateMockEvents(count)
        return events.every(event => {
          const requiredFields = [
            'event_time', 'event_type', 'product_id', 
            'category_id', 'category_code', 'brand', 
            'price', 'user_id', 'user_session'
          ]
          return requiredFields.every(field => field in event)
        })
      }
    ),
    { numRuns: 100 }
  )
})
```

**属性 4：图表组件初始化**
```javascript
// Feature: graduation-development-standards, Property 4: 图表组件初始化
test('chart component should initialize with valid data', () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({
        name: fc.string(),
        value: fc.integer({ min: 0, max: 1000000 })
      }), { minLength: 1, maxLength: 20 }),
      (data) => {
        const wrapper = mount(PieChart, {
          props: { data }
        })
        // 验证 ECharts 实例已创建
        return wrapper.vm.chartInstance !== null
      }
    ),
    { numRuns: 100 }
  )
})
```

### 集成测试

**测试场景**：
- 完整的用户流程：登录 → 浏览各页面 → 退出
- 路由导航：验证所有页面路由可访问
- 数据流：Mock 数据 → API 层 → 组件渲染

**工具**：Playwright 或 Cypress（端到端测试）

### 测试覆盖率目标

- **代码覆盖率**：≥ 80%
- **组件覆盖率**：100%（所有组件至少有基本测试）
- **关键路径覆盖率**：100%（登录、路由守卫、数据加载）

### 持续集成

- 在 Git 提交前自动运行单元测试（使用 husky）
- 在 Pull Request 中运行完整测试套件
- 测试失败时阻止合并



## 样式设计 (Styling)

### 深色主题配置

**variables.scss**
```scss
// 主色调
$primary-color: #00d4ff;        // 电光蓝（科技感）
$primary-dark: #0099cc;
$primary-light: #33ddff;

// 背景色
$bg-dark: #0a0e27;              // 深蓝黑背景
$bg-card: #1a1f3a;              // 卡片背景
$bg-sidebar: #13182e;           // 侧边栏背景
$bg-header: #0f1429;            // 顶部栏背景

// 文字颜色
$text-primary: #ffffff;
$text-secondary: #a0aec0;
$text-muted: #718096;

// 边框和分割线
$border-color: #2d3748;
$divider-color: rgba(255, 255, 255, 0.1);

// 状态颜色
$success-color: #48bb78;
$warning-color: #ed8936;
$error-color: #f56565;
$info-color: #4299e1;

// 阴影
$shadow-sm: 0 2px 8px rgba(0, 212, 255, 0.1);
$shadow-md: 0 4px 16px rgba(0, 212, 255, 0.15);
$shadow-lg: 0 8px 32px rgba(0, 212, 255, 0.2);

// 渐变
$gradient-primary: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
$gradient-card: linear-gradient(135deg, #1a1f3a 0%, #13182e 100%);
```

### 组件样式规范

**卡片样式**
- 背景：`$bg-card`
- 边框：1px solid `$border-color`
- 圆角：8px
- 内边距：24px
- 悬停效果：边框颜色变为 `$primary-color`，添加阴影 `$shadow-md`

**按钮样式**
- 主按钮：背景 `$gradient-primary`，文字白色
- 次按钮：边框 `$primary-color`，背景透明
- 悬停效果：亮度增加 10%，添加阴影

**侧边栏样式**
- 背景：`$bg-sidebar`
- 选中项：背景 `$primary-color`，文字白色，左侧 4px 宽的高亮条
- 未选中项：文字 `$text-secondary`，悬停时背景 `rgba(0, 212, 255, 0.1)`

## ECharts 主题配置 (Chart Theme)

### 深色主题定义

**chartTheme.js**
```javascript
export const darkTheme = {
  color: [
    '#00d4ff', '#ff6b9d', '#ffa94d', '#8ce99a',
    '#74c0fc', '#da77f2', '#ffd43b', '#ff8787'
  ],
  backgroundColor: 'transparent',
  textStyle: {
    color: '#a0aec0',
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
  },
  title: {
    textStyle: {
      color: '#ffffff',
      fontSize: 18,
      fontWeight: 600
    },
    subtextStyle: {
      color: '#718096'
    }
  },
  line: {
    itemStyle: {
      borderWidth: 2
    },
    lineStyle: {
      width: 3
    },
    symbolSize: 8,
    smooth: true
  },
  radar: {
    itemStyle: {
      borderWidth: 2
    },
    lineStyle: {
      width: 3
    },
    symbolSize: 8
  },
  bar: {
    itemStyle: {
      barBorderWidth: 0,
      barBorderColor: '#ccc'
    }
  },
  pie: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  scatter: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  categoryAxis: {
    axisLine: {
      show: true,
      lineStyle: {
        color: '#2d3748'
      }
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      show: true,
      color: '#718096'
    },
    splitLine: {
      show: false
    },
    splitArea: {
      show: false
    }
  },
  valueAxis: {
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      show: true,
      color: '#718096'
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: ['#2d3748'],
        type: 'dashed'
      }
    },
    splitArea: {
      show: false
    }
  },
  tooltip: {
    backgroundColor: 'rgba(26, 31, 58, 0.95)',
    borderColor: '#00d4ff',
    borderWidth: 1,
    textStyle: {
      color: '#ffffff'
    }
  },
  legend: {
    textStyle: {
      color: '#a0aec0'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '10%',
    containLabel: true
  }
}
```

## 实现细节 (Implementation Details)

### 1. 项目初始化

使用 Vite 创建 Vue3 项目：
```bash
npm create vite@latest hadoop-ecommerce-analysis -- --template vue
cd hadoop-ecommerce-analysis
npm install
```

安装依赖：
```bash
npm install vue-router@4 pinia element-plus
npm install echarts echarts-wordcloud
npm install axios
npm install sass -D
```

### 2. 路由守卫实现

在 `router/index.js` 中添加全局前置守卫：

```javascript
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    // 需要认证但未登录，跳转到登录页
    next('/login')
  } else if (to.path === '/login' && userStore.isAuthenticated) {
    // 已登录用户访问登录页，跳转到首页
    next('/dashboard')
  } else {
    next()
  }
})
```

### 3. ECharts 图表封装模式

所有图表组件遵循统一的封装模式：

```vue
<template>
  <div ref="chartRef" :style="{ height, width: '100%' }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { darkTheme } from '@/utils/chartTheme'

const props = defineProps({
  data: {
    type: [Object, Array],
    required: true
  },
  height: {
    type: String,
    default: '400px'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value, darkTheme)
  updateChart()
  
  // 响应式调整
  window.addEventListener('resize', handleResize)
}

const updateChart = () => {
  if (!chartInstance) return
  
  const option = {
    // 根据具体图表类型配置
  }
  
  chartInstance.setOption(option, true)
}

const handleResize = () => {
  chartInstance?.resize()
}

watch(() => props.data, () => {
  updateChart()
}, { deep: true })

watch(() => props.loading, (val) => {
  if (val) {
    chartInstance?.showLoading()
  } else {
    chartInstance?.hideLoading()
  }
})

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>
```

### 4. Mock 数据工具函数

**utils/mockHelper.js**
```javascript
// 生成时间标签（小时）
export function generateHourLabels() {
  return Array.from({ length: 24 }, (_, i) => 
    `${String(i).padStart(2, '0')}:00`
  )
}

// 生成日期标签
export function generateDateLabels(startOffset, endOffset) {
  const dates = []
  const today = new Date()
  
  for (let i = startOffset; i <= endOffset; i++) {
    const date = new Date(today)
    date.setDate(date.getDate() + i)
    dates.push(date.toISOString().split('T')[0])
  }
  
  return dates
}

// 生成趋势数据（带随机波动）
export function generateTrendData(count, min, max) {
  return Array.from({ length: count }, () => 
    Math.floor(Math.random() * (max - min + 1)) + min
  )
}

// 生成散点数据
export function generateScatterData(count) {
  return Array.from({ length: count }, () => [
    Math.random() * 5000 + 100,  // 价格 100-5100
    Math.floor(Math.random() * 10000)  // 销量 0-10000
  ])
}

// 模拟品牌数据
export const MOCK_BRANDS = [
  'xiaomi', 'apple', 'samsung', 'huawei', 'oppo', 
  'vivo', 'lenovo', 'asus', 'dell', 'hp'
]

// 模拟品类代码
export const MOCK_CATEGORIES = [
  'electronics.smartphone',
  'electronics.tablet',
  'computers.notebook',
  'computers.desktop',
  'appliances.kitchen',
  'appliances.climate',
  'accessories.headphone',
  'accessories.case'
]
```

### 5. 粒子背景实现

**ParticleBackground.vue** 使用 Canvas API 实现：

```javascript
class Particle {
  constructor(canvas) {
    this.canvas = canvas
    this.x = Math.random() * canvas.width
    this.y = Math.random() * canvas.height
    this.vx = (Math.random() - 0.5) * 0.5
    this.vy = (Math.random() - 0.5) * 0.5
    this.radius = Math.random() * 2 + 1
  }
  
  update() {
    this.x += this.vx
    this.y += this.vy
    
    if (this.x < 0 || this.x > this.canvas.width) this.vx *= -1
    if (this.y < 0 || this.y > this.canvas.height) this.vy *= -1
  }
  
  draw(ctx) {
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
    ctx.fillStyle = 'rgba(0, 212, 255, 0.6)'
    ctx.fill()
  }
}
```

### 6. 响应式布局

使用 Element Plus 的栅格系统和媒体查询：

```scss
// 响应式断点
$breakpoint-sm: 768px;
$breakpoint-md: 992px;
$breakpoint-lg: 1200px;
$breakpoint-xl: 1920px;

// 移动端适配
@media (max-width: $breakpoint-sm) {
  .sidebar {
    position: fixed;
    left: -250px;
    transition: left 0.3s;
    
    &.open {
      left: 0;
    }
  }
  
  .metric-card {
    margin-bottom: 16px;
  }
}
```

## 正确性属性 (Correctness Properties)

### 1. 数据一致性属性

**属性 1.1：Mock 数据字段完整性**
- **描述**：所有 Mock 数据必须包含 9 个核心字段
- **验证方法**：单元测试检查每个 Mock 函数返回的数据结构
- **测试示例**：
```javascript
test('Dashboard mock data should contain all required fields', () => {
  const data = getDashboardData()
  expect(data).toHaveProperty('metrics.gmv')
  expect(data).toHaveProperty('metrics.pv')
  expect(data).toHaveProperty('metrics.uv')
  expect(data.pvuvTrend).toHaveProperty('xAxis')
  expect(data.pvuvTrend).toHaveProperty('pv')
  expect(data.pvuvTrend).toHaveProperty('uv')
})
```

**属性 1.2：漏斗数据递减性**
- **描述**：转化漏斗的数据必须呈现递减趋势（浏览 > 加购 > 下单）
- **验证方法**：属性测试验证漏斗数据的单调递减性
- **测试示例**：
```javascript
test('Funnel data should be monotonically decreasing', () => {
  const data = getConversionData()
  const values = data.funnel.map(item => item.value)
  
  for (let i = 1; i < values.length; i++) {
    expect(values[i]).toBeLessThanOrEqual(values[i - 1])
  }
})
```

### 2. UI 渲染属性

**属性 2.1：路由守卫正确性**
- **描述**：未登录用户无法访问需要认证的页面
- **验证方法**：集成测试模拟路由跳转
- **测试示例**：
```javascript
test('Unauthenticated user should be redirected to login', async () => {
  const userStore = useUserStore()
  userStore.isAuthenticated = false
  
  await router.push('/dashboard')
  expect(router.currentRoute.value.path).toBe('/login')
})
```

**属性 2.2：图表响应式调整**
- **描述**：窗口大小变化时，图表应自动调整尺寸
- **验证方法**：组件测试模拟窗口 resize 事件
- **测试示例**：
```javascript
test('Chart should resize on window resize', async () => {
  const wrapper = mount(LineChart, {
    props: { data: mockData }
  })
  
  const resizeSpy = vi.spyOn(wrapper.vm.chartInstance, 'resize')
  window.dispatchEvent(new Event('resize'))
  
  expect(resizeSpy).toHaveBeenCalled()
})
```

### 3. 组件交互属性

**属性 3.1：侧边栏导航正确性**
- **描述**：点击侧边栏菜单项应正确跳转到对应页面
- **验证方法**：组件测试模拟点击事件
- **测试示例**：
```javascript
test('Sidebar menu item click should navigate to correct route', async () => {
  const wrapper = mount(Sidebar, {
    global: {
      plugins: [router]
    }
  })
  
  await wrapper.find('[data-path="/dashboard"]').trigger('click')
  expect(router.currentRoute.value.path).toBe('/dashboard')
})
```

**属性 3.2：登录表单验证**
- **描述**：用户名和密码必须匹配 admin/admin 才能登录成功
- **验证方法**：组件测试验证登录逻辑
- **测试示例**：
```javascript
test('Login should succeed with correct credentials', async () => {
  const wrapper = mount(Login)
  
  await wrapper.find('input[type="text"]').setValue('admin')
  await wrapper.find('input[type="password"]').setValue('admin')
  await wrapper.find('button[type="submit"]').trigger('click')
  
  const userStore = useUserStore()
  expect(userStore.isAuthenticated).toBe(true)
})
```

### 4. 数据可视化属性

**属性 4.1：图表数据绑定正确性**
- **描述**：传入图表组件的数据应正确渲染到图表中
- **验证方法**：快照测试验证图表配置
- **测试示例**：
```javascript
test('PieChart should render correct data', () => {
  const mockData = [
    { name: '电子产品', value: 5000 },
    { name: '服装', value: 3000 }
  ]
  
  const wrapper = mount(PieChart, {
    props: { data: mockData }
  })
  
  const option = wrapper.vm.chartInstance.getOption()
  expect(option.series[0].data).toEqual(mockData)
})
```

**属性 4.2：预测数据样式区分**
- **描述**：预测折线图中，历史数据用实线，预测数据用虚线
- **验证方法**：单元测试检查 ECharts 配置
- **测试示例**：
```javascript
test('Prediction chart should use dashed line for forecast', () => {
  const wrapper = mount(LineChart, {
    props: { 
      data: mockPredictionData,
      showForecast: true 
    }
  })
  
  const option = wrapper.vm.chartInstance.getOption()
  const forecastSeries = option.series.find(s => s.name === '预测')
  
  expect(forecastSeries.lineStyle.type).toBe('dashed')
})
```

## 测试策略 (Testing Strategy)

### 测试框架选择

- **单元测试**：Vitest（与 Vite 无缝集成）
- **组件测试**：@vue/test-utils
- **E2E 测试**：Playwright（可选，用于关键流程验证）

### 测试覆盖目标

1. **Mock 数据生成器**：100% 覆盖
2. **工具函数**：100% 覆盖
3. **图表组件**：核心逻辑 80% 覆盖
4. **页面组件**：关键交互 60% 覆盖
5. **路由守卫**：100% 覆盖

### 测试组织结构

```
tests/
├── unit/                    # 单元测试
│   ├── utils/
│   │   ├── mockHelper.test.js
│   │   ├── chartTheme.test.js
│   │   └── dateFormat.test.js
│   └── api/
│       ├── dashboard.test.js
│       ├── conversion.test.js
│       └── product.test.js
├── component/               # 组件测试
│   ├── charts/
│   │   ├── LineChart.test.js
│   │   ├── PieChart.test.js
│   │   └── FunnelChart.test.js
│   ├── layout/
│   │   ├── Sidebar.test.js
│   │   └── Header.test.js
│   └── common/
│       └── MetricCard.test.js
└── e2e/                     # E2E 测试（可选）
    ├── login.spec.js
    └── dashboard.spec.js
```

### 测试配置

**vitest.config.js**
```javascript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.js'
      ]
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
```

## 性能优化 (Performance Optimization)

### 1. 路由懒加载

所有页面组件使用动态导入：
```javascript
const Dashboard = () => import('@/views/Dashboard.vue')
```

### 2. 图表按需加载

只导入使用的 ECharts 组件：
```javascript
import * as echarts from 'echarts/core'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  LineChart, PieChart, BarChart,
  GridComponent, TooltipComponent,
  CanvasRenderer
])
```

### 3. 组件缓存

使用 `<keep-alive>` 缓存页面组件：
```vue
<router-view v-slot="{ Component }">
  <keep-alive :include="['Dashboard', 'Conversion']">
    <component :is="Component" />
  </keep-alive>
</router-view>
```

### 4. 防抖和节流

对频繁触发的事件（如窗口 resize）使用防抖：
```javascript
import { debounce } from 'lodash-es'

const handleResize = debounce(() => {
  chartInstance?.resize()
}, 200)
```

## 部署配置 (Deployment)

### 构建配置

**vite.config.js**
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          'echarts': ['echarts'],
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia']
        }
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
})
```

### 环境变量

**.env.development**
```
VITE_APP_TITLE=Hadoop电商行为分析系统
VITE_API_BASE_URL=/api
```

**.env.production**
```
VITE_APP_TITLE=Hadoop电商行为分析系统
VITE_API_BASE_URL=https://api.example.com
```

## 总结 (Summary)

本设计文档详细描述了基于 Vue3 的电商用户行为分析可视化系统的前端架构。系统采用组件化设计，使用 Mock 数据驱动，遵循深色科技风格，包含 6 个核心页面和多个可复用的图表组件。

**核心特点**：
1. 清晰的分层架构（视图层、组件层、API 层）
2. 统一的图表组件封装模式
3. 完善的 Mock 数据生成机制
4. 深色主题的视觉设计
5. 全面的测试策略和正确性属性验证

**下一步**：根据本设计文档创建详细的实现任务列表（tasks.md），按模块逐步实现系统功能。
