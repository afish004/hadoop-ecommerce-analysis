# 毕设前端极速开发任务清单 (Lite Version)

## 1. 基础环境搭建 (精简版)

- [x] **1.1 初始化项目**
  - 使用 `npm create vite@latest` 创建 Vue3 项目
  - **仅安装必要依赖**: `vue-router`, `element-plus`, `echarts`, `sass`, `axios`, `@element-plus/icons-vue`
  - *移除: Pinia, Vitest, ESLint, Prettier 等非必要工具*

- [x] **1.2 创建核心目录**
  - `src/layout` (存放 MainLayout)
  - `src/views` (存放 6 个页面组件)
  - `src/components` (存放封装的图表组件)
  - `src/api` (存放 Mock 数据和 Service 层)
  - `src/assets/styles` (存放样式文件)

- [x] **1.3 配置深色主题 (Dark Mode)**
  - 在 `src/assets/styles` 中定义深色背景变量 (如 `#0f172a`)
  - 在 `main.js` 中引入 Element Plus 的深色样式

## 2. API 隔离层 (核心策略 - 为后端联调做准备)

- [x] **2.1 编写 Mock 数据源**
  - 创建 `src/api/mockData.js`
  - **数据要求**: 根据数据集字段 (`event_time`, `event_type`, `price`, `user_id` 等) 生成静态 JSON 数据
  - **覆盖范围**: Dashboard 指标, 漏斗图数据, 品牌销量, 预测折线图数据

- [x] **2.2 封装 Service 中介层**
  - 创建 `src/api/service.js`
  - 封装通用请求函数: `fetchDashboardData`, `fetchPredictionData` 等
  - **策略**: 使用 `Promise` + `setTimeout` 返回 mockData，模拟 200ms 网络延迟
  - *目的: 后续联调真实后端时，只需修改此处逻辑为 axios 请求，页面代码无需变动*

## 3. 布局与路由系统

- [x] **3.1 配置路由**
  - 创建 `src/router/index.js`
  - 配置 6 个路由: `/login`, `/dashboard`, `/conversion`, `/product`, `/user-insight`, `/prediction`
  - 设置默认路由重定向到 `/dashboard` (登录后)

- [x] **3.2 开发侧边栏 (Sidebar)**
  - 使用 Element Plus `el-menu` 组件
  - **实现分组逻辑**:
    1.  **综合态势**: Dashboard
    2.  **核心分析**: Conversion, Product, UserInsight
    3.  **智能决策**: Prediction
  - 实现路由跳转与选中高亮 (电光蓝风格)

- [x] **3.3 开发主布局 (MainLayout)**
  - 顶部 Header: 显示系统标题、实时时间、管理员头像
  - 左侧 Sidebar: 集成侧边栏组件
  - 内容区: 使用 `router-view` 渲染子页面

## 4. 核心页面开发 (可视化实现)

- [x] **4.1 开发 Login 登录页**
  - 深色科技感背景
  - 简单登录逻辑: 校验 `admin/123456` -> 存入 localStorage -> 跳转 Dashboard

- [x] **4.2 开发 Dashboard (驾驶舱)**
  - **指标卡**: 展示 GMV, PV, UV (读取 Service 层数据)
  - **趋势图**: 渲染 24小时 PV/UV 折线图

- [x] **4.3 开发 Conversion (转化分析)**
  - **漏斗图**: 展示 浏览 -> 加购 -> 下单 的转化率 (数据需递减)
  - **玫瑰图**: 展示各行为类型的分布占比

- [x] **4.4 开发 Product (商品分析)**
  - **柱状图**: 品牌销量 Top 10
  - **词云图**: 热门品类展示 (使用 echarts-wordcloud 或简单列表)

- [x] **4.5 开发 UserInsight (用户价值)**
  - **饼图**: RFM 用户分层占比 (高价值/挽留/流失)

- [x] **4.6 开发 Prediction (趋势预测 - 毕设亮点)**
  - **预测折线图**:
    - 实线: 历史 30 天流量
    - 虚线: 未来 7 天预测流量
    - 阴影: 95% 置信区间 (Area Style)

## 5. 最终优化

- [x] **5.1 样式微调**
  - 统一图表配色 (青色/蓝色/紫色调)
  - 确保控制台无报错 (No Errors)