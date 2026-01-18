# 毕业论文开发规范系统需求文档

## 项目背景
这是一个本科毕业设计项目，目标是构建一个电商用户行为数据的全链路分析系统。
核心流程：Flume/Kafka采集 -> Hadoop/Hive数仓分层(ODS/DWD/DWS/ADS) -> MySQL结果存储 -> Python后端 -> Vue前端可视化。


## 技术栈约束
- **前端**: Vue3 (使用 Vite 构建)
- **可视化**: ECharts 5.x.
- **后端服务**: Python  (FastAPI),只负责读取MySQL数据给前端.
- **数仓**: Hive (分层结构), MySQL (存储ADS层结果).


## 需求
# Project Spec: 基于Hadoop的电商用户行为分析系统 (前端工程版)

## 1. 项目背景与目标
这是一个本科毕业设计项目，题目为《基于Hadoop的电商用户行为分析系统设计与实现》
**当前阶段目标**：优先搭建高质量的前端可视化系统。
**核心逻辑**：前端暂时不连接真实后端，而是通过 **Mock Data (模拟数据)** 展示未来数仓分析的结果。数据结构必须严格对应我现有的数据集字段。

## 2. 核心数据集定义 (Data Schema)
前端所有的 Mock 数据必须基于以下 9 个字段生成，逻辑要自洽：
- `event_time`: 时间 (用于时间序列分析)
- `event_type`: 行为类型 (枚举值: view, cart, purchase, remove_from_cart)
- `product_id`: 商品ID
- `category_id`: 品类ID
- `category_code`: 品类代码 (例如: electronics.smartphone)
- `brand`: 品牌 (例如: xiaomi, apple)
- `price`: 价格 (用于计算 GMV)
- `user_id`: 用户ID (用于计算 UV 和 RFM 模型)
- `user_session`: 会话ID

## 3. 技术栈要求
- **框架**: Vue 3 + Vite (构建工具)
- [cite_start]**UI 组件库**: Element Plus (用于布局、表格、侧边栏) [cite: 15]
- [cite_start]**可视化库**: ECharts 5.x (核心，用于所有图表展示) [cite: 15]
- **数据请求**: Axios (配合 Mockjs 或简单的 JSON 模拟)
- **样式风格**: "Dark Mode" (深色科技风)，符合大数据看板的视觉体验。

## 4. 功能模块 (Sitemap)
系统需要包含以下 6 个核心页面路由：

### 4.1 登录页 (Login) - `/login`
- **功能**: 展示系统标题。提供模拟登录 (admin/admin)。
- **视觉**: 背景要有科技感粒子效果。

### 4.2 综合数据驾驶舱 (Dashboard) - `/dashboard`
- **定位**: 全局概览，展示数仓 ADS 层最核心的宏观指标。
- **图表要求**:
    - **核心指标卡**: 总销售额 (GMV), 总访问量 (PV), 独立访客数 (UV)。
    - **实时流量趋势**: 24小时 PV/UV 折线图 (基于 `event_time`)。
    - **分类销售占比**: 饼图 (基于 `category_code`)。

### 4.3 流量与转化分析 (Conversion) - `/conversion`
- [cite_start]**定位**: 用户行为路径分析 [cite: 15]。
- **图表要求**:
    - **漏斗图 (Funnel)**: 浏览(view) -> 加购(cart) -> 下单(purchase)。数据必须体现层级递减。
    - **行为分布玫瑰图**: 各类 `event_type` 的数量占比。

### 4.4 商品与品牌洞察 (Product) - `/product`
- **定位**: 基于商品维度的挖掘。
- **图表要求**:
    - **品牌 TOP10**: 横向柱状图 (按 `brand` 统计销量)。
    - **品类词云 (WordCloud)**: 解析 `category_code` 展示热门关键词。
    - **价格敏感度分析**: 散点图 (X轴价格，Y轴销量)。

### 4.5 用户价值分层 (UserInsight) - `/user-insight`
- **定位**: 展示 RFM 模型分析结果（体现深度）。
- **图表要求**:
    - **用户分层占比**: 饼图 (高价值用户、挽留用户、流失用户)。
    - **Mock逻辑**: 基于 `user_id` 和 `price` 模拟分层数据。

### 4.6 趋势预测 (Prediction) - `/prediction`
- [cite_start]**定位**: 展示时间序列算法的预测结果 [cite: 15]。
- **注意**: 这是一个展示页面，算法逻辑暂未联调，使用 Mock 数据展示效果。
- **图表要求**:
    - **未来7天流量预测**: 折线图。**关键点**：历史数据用实线，预测数据用虚线，并带有置信区间阴影。
## 5、页面规划
布局重构要求 (UI/UX)**:
- **Login 页面**: 这是一个完全独立的页面 (Full Page)，不包含侧边栏和顶部栏。
- **主布局 (MainLayout)**: 包含 侧边栏 (Sidebar) 和 顶部栏 (Header)。
    - **顶部栏**: 左侧显示系统标题 "Hadoop电商行为分析系统"，右侧显示当前时间、管理员头像、退出按钮。
    - **侧边栏**: 请使用**分组逻辑**来排列菜单，不要全部堆在一起。

**2. 侧边栏菜单结构 (Menu Structure)**:
请严格按照以下层级生成 `Menu` 组件：
- **(Icon: Odometer) 综合态势**
    -  `/dashboard` -> 驾驶舱 (Dashboard)
- **(Group Title: 核心分析)** <-- 加上分组标题，视觉上分割
    - `/conversion` -> (Icon: Trend) 流量与转化 (Traffic & Conversion)
    - `/product` -> (Icon: Goods) 商品与品牌 (Product Insights)
    - `/user-insight` -> (Icon: User) 用户价值分层 (User Portrait)
- **(Group Title: 智能决策)** <-- 突出你的算法亮点
    - `/prediction` -> (Icon: MagicStick) 趋势预测 (AI Forecast)
**3. 视觉风格**:
- 保持深色模式 (Dark Mode)。
- 侧边栏选中项 (Active State) 需要有明显的高亮背景色（例如电光蓝），体现科技感。
## 6. 开发规范
- **组件化**: 每个 ECharts 图表必须封装成独立的 .vue 组件 (例如 `FunnelChart.vue`).
- **数据模拟**: 在 `src/api/mock` 目录下创建对应的数据生成函数，不要写死在组件里。
