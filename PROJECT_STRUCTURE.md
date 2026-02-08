# 📁 项目结构说明

> **项目名称**: Hadoop 电商数据分析系统  
> **技术栈**: Vue 3 + Element Plus + ECharts + SCSS  
> **数据集**: 2019年10月电商数据  
> **设计理念**: 反主流设计（拒绝对称、专业术语、冷冰冰的数据展示）

---

## 🌳 目录树概览

```
hadoop-ecommerce-analysis/
├── 📂 .git/                    # Git 版本控制
├── 📂 .kiro/                   # Kiro AI 配置目录
│   ├── hooks/                  # AI 自动化钩子
│   ├── specs/                  # 功能规格文档
│   └── steering/               # AI 引导规则（UI/UX Pro Max）
├── 📂 backend/                 # 后端目录（当前为空，预留）
├── 📂 docs/                    # 项目文档
│   ├── 功能说明文档            # 各页面功能说明
│   ├── 优化说明文档            # 版本迭代优化记录
│   └── AGENTS.md               # AI Agent 设计理念
├── 📂 frontend/                # 前端项目（主要开发目录）
│   ├── public/                 # 静态资源
│   ├── src/                    # 源代码
│   │   ├── api/                # API 接口和 Mock 数据
│   │   ├── assets/             # 样式资源
│   │   ├── components/         # 可复用组件（图表组件）
│   │   ├── layout/             # 布局组件（MainLayout、Sidebar）
│   │   ├── router/             # 路由配置
│   │   └── views/              # 页面视图（业务页面）
│   ├── package.json            # 依赖配置
│   └── vite.config.js          # Vite 构建配置
└── README.md                   # 项目说明
```

---

## 📂 核心目录详解

### 1️⃣ `.kiro/` - AI 辅助开发配置

```
.kiro/
├── hooks/                              # AI 自动化钩子
│   └── code-comment-doc-generator.kiro.hook  # 代码注释和文档生成钩子
├── specs/                              # 功能规格文档
│   ├── ecommerce-dashboard-october-2019/     # 电商看板规格
│   └── graduation-development-standards/     # 毕业设计开发规范
└── steering/                           # AI 引导规则
    └── ui-ux-pro-max/                  # UI/UX 设计系统（67种样式、96种配色）
```

**用途**：
- 🤖 **hooks**: 自动触发 AI 任务（如文件保存后自动生成注释和文档）
- 📋 **specs**: 功能需求、设计文档、任务清单
- 🎨 **steering**: UI/UX 设计规范，指导 AI 生成符合设计系统的代码

---

### 2️⃣ `docs/` - 项目文档中心

```
docs/
├── 功能说明文档/
│   ├── MainLayout-功能说明.md          # 主布局功能说明
│   ├── Sidebar-功能说明.md             # 侧边栏功能说明
│   ├── OpsDashboard-功能说明.md        # 运营看板功能说明
│   ├── ProductBrand-功能说明.md        # 商品品牌功能说明
│   └── SmartPrediction-功能说明.md     # 智能预测功能说明
│
├── 优化说明文档/
│   ├── OpsDashboard-反主流设计升级说明-v4.0.md
│   ├── OpsDashboard-配色优化说明-v3.0.md
│   ├── ProductBrand-旭日图布局优化说明-v2.4.md
│   └── SmartPrediction-视觉风格优化说明-v1.1.md
│
├── 设计理念文档/
│   ├── AGENTS.md                       # AI Agent 设计理念（反主流设计核心）
│   ├── 反主流设计全面升级说明-v5.0.md
│   └── v5.0-优化总结.md
│
└── 开发记录/
    ├── 代码变更记录.md                 # 代码变更历史
    └── 业务主题重构完成报告.md         # 重构总结报告
```

**文档分类**：
- 📖 **功能说明**: 各模块的功能、数据流、使用方法
- 🔧 **优化说明**: 版本迭代的改动内容、设计原理、效果对比
- 🎨 **设计理念**: 反主流设计原则、AI 协作方法论
- 📝 **开发记录**: 变更历史、重构总结

---

### 3️⃣ `frontend/src/` - 前端源代码

```
frontend/src/
├── 📂 api/                             # API 层
│   ├── service.js                      # API 接口封装（axios）
│   └── mockData.js                     # Mock 数据（2019年10月电商数据）
│
├── 📂 assets/                          # 样式资源
│   └── styles/
│       ├── variables.scss              # SCSS 变量（颜色、阴影、字体）
│       └── global.scss                 # 全局样式
│
├── 📂 components/                      # 可复用组件（图表组件）
│   ├── BarChart.vue                    # 柱状图（品牌 TOP10）
│   ├── LineChart.vue                   # 折线图（趋势分析）
│   ├── PieChart.vue                    # 饼图（占比分析）
│   ├── SunburstChart.vue               # 旭日图（品类层级）
│   ├── ScatterChart.vue                # 散点图（价格敏感度）
│   ├── HeatmapChart.vue                # 热力图（时间分布）
│   ├── FunnelChart.vue                 # 漏斗图（转化流程）
│   ├── SankeyChart.vue                 # 桑基图（流量流向）
│   ├── WordCloudList.vue               # 词云列表（品类标签）
│   └── MetricCard.vue                  # 指标卡片（核心数据展示）
│
├── 📂 layout/                          # 布局组件
│   ├── MainLayout.vue                  # 主布局（顶栏 + 侧边栏 + 内容区）
│   └── Sidebar.vue                     # 侧边栏（导航菜单）
│
├── 📂 router/                          # 路由配置
│   └── index.js                        # Vue Router 路由表
│
├── 📂 views/                           # 页面视图（业务页面）
│   ├── Login.vue                       # 登录页
│   ├── Dashboard.vue                   # 数据总览（已废弃，被 OpsDashboard 替代）
│   ├── OpsDashboard.vue                # 运营数据看板（主页）
│   ├── ProductBrand.vue                # 商品与品牌洞察
│   ├── UserConversion.vue              # 用户与转化全景
│   ├── SmartPrediction.vue             # 智能预测
│   ├── Product.vue                     # 商品分析（旧版，已废弃）
│   ├── Conversion.vue                  # 转化分析（旧版，已废弃）
│   ├── Prediction.vue                  # 预测分析（旧版，已废弃）
│   ├── UserInsight.vue                 # 用户洞察（旧版，已废弃）
│   └── NotFound.vue                    # 404 页面
│
├── App.vue                             # 根组件
└── main.js                             # 入口文件（Vue 实例、路由、Element Plus）
```

---

## 🎯 核心业务页面说明

### 主要页面（当前使用）

| 页面 | 路由 | 功能 | 布局特点 |
|------|------|------|---------|
| **OpsDashboard** | `/ops-dashboard` | 运营数据看板（主页） | 4图 Bento Grid（不对称布局） |
| **ProductBrand** | `/product-brand` | 商品与品牌洞察 | 3图 Bento Grid（5:3 黄金比例） |
| **UserConversion** | `/user-conversion` | 用户与转化全景 | 4图 Bento Grid（不对称布局） |
| **SmartPrediction** | `/smart-prediction` | 智能预测 | 3图 Bento Grid（不对称布局） |

### 旧版页面（已废弃）

| 页面 | 状态 | 说明 |
|------|------|------|
| Dashboard | ❌ 已废弃 | 被 OpsDashboard 替代 |
| Product | ❌ 已废弃 | 被 ProductBrand 替代 |
| Conversion | ❌ 已废弃 | 被 UserConversion 替代 |
| Prediction | ❌ 已废弃 | 被 SmartPrediction 替代 |
| UserInsight | ❌ 已废弃 | 被 UserConversion 替代 |

---

## 📊 图表组件说明

### ECharts 图表组件

| 组件 | 用途 | 使用页面 |
|------|------|---------|
| **BarChart** | 柱状图（横向/纵向） | ProductBrand（品牌 TOP10） |
| **LineChart** | 折线图（趋势分析） | OpsDashboard（销售趋势） |
| **PieChart** | 饼图（占比分析） | OpsDashboard（品类占比） |
| **SunburstChart** | 旭日图（层级结构） | ProductBrand（品类层级） |
| **ScatterChart** | 散点图（相关性分析） | ProductBrand（价格敏感度） |
| **HeatmapChart** | 热力图（时间分布） | UserConversion（活跃时段） |
| **FunnelChart** | 漏斗图（转化流程） | UserConversion（转化漏斗） |
| **SankeyChart** | 桑基图（流量流向） | UserConversion（流量来源） |
| **WordCloudList** | 词云列表（标签展示） | ProductBrand（品类标签） |
| **MetricCard** | 指标卡片（核心数据） | OpsDashboard（GMV、订单量等） |

---

## 🎨 设计系统

### SCSS 变量（`assets/styles/variables.scss`）

```scss
// 颜色系统
$primary-color: #6366F1;        // 主色（靛蓝色）
$text-primary: #0F172A;         // 主文本（深灰）
$text-secondary: #475569;       // 次要文本（中灰）
$text-muted: #94A3B8;           // 弱化文本（浅灰）
$border-color: rgba(255, 255, 255, 0.1);  // 边框颜色

// 渐变背景
$gradient-card: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);

// 阴影系统
$shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
$shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.15);
```

### 布局系统

- **Bento Grid**: 不对称网格布局（CSS Grid）
- **黄金比例**: 5:3 ≈ 1.667:1（接近 1.618:1）
- **响应式**: 移动端自动切换为单列布局

---

## 🚀 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问：`http://localhost:5173`

### 构建生产版本

```bash
npm run build
```

---

## 📦 核心依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| **Vue** | 3.x | 前端框架 |
| **Vue Router** | 4.x | 路由管理 |
| **Element Plus** | 最新 | UI 组件库 |
| **ECharts** | 5.x | 数据可视化 |
| **Axios** | 最新 | HTTP 请求 |
| **Sass** | 最新 | CSS 预处理器 |
| **Vite** | 最新 | 构建工具 |

---

## 🎯 设计理念：反主流设计

### 核心原则（来自 `docs/AGENTS.md`）

1. **拒绝对称布局** → 使用 Bento Grid 不对称布局
2. **拒绝专业术语** → 使用口语化、有温度的文案
3. **拒绝冷冰冰的数据** → 使用有机光晕、手写感下划线
4. **追求视觉张力** → 使用黄金比例、不规则间距

### 视觉特点

- 🌈 **有机光晕**: 使用径向渐变创建柔和的背景装饰
- ✍️ **手写感下划线**: 图表标题使用渐变下划线
- 🎨 **不对称布局**: Bento Grid 布局，拒绝对称
- 🌟 **悬停效果**: 卡片悬停时轻微旋转 + 缩放

---

## 📝 开发规范

### 代码注释规范

- ✅ 使用 JSDoc 格式注释函数
- ✅ 使用中文注释（简体中文）
- ✅ 注释包含：功能说明、参数说明、返回值说明、示例代码

### 文档规范

- ✅ 每次代码变更后在 `docs/` 创建或更新文档
- ✅ 文档包含：变更概述、问题分析、详细改动、效果对比
- ✅ 使用 Markdown 格式，包含表格、代码块、Emoji

### Git 提交规范

```
feat: 新功能
fix: 修复 Bug
docs: 文档更新
style: 样式优化
refactor: 代码重构
perf: 性能优化
test: 测试相关
chore: 构建/工具相关
```

---

## 🔗 相关文档

- [AGENTS.md](./docs/AGENTS.md) - AI Agent 设计理念
- [反主流设计全面升级说明-v5.0.md](./docs/反主流设计全面升级说明-v5.0.md) - 设计理念详解
- [代码变更记录.md](./docs/代码变更记录.md) - 代码变更历史

---

**最后更新**: 2026-02-07  
**维护者**: Kiro AI + 开发团队
