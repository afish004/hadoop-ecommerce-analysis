# 后端文件结构说明

> 技术栈: **FastAPI** + **SQLAlchemy 2.0 (异步)** + **MySQL** + **JWT 认证**
> 启动命令: `python -m uvicorn app.main:app --reload --port 8000`

---

## 目录总览

```
backend/
├── .env                  # 环境变量（实际使用的配置，不提交Git）
├── .env.example          # 环境变量模板（供参考）
├── requirements.txt      # Python依赖列表
├── README.md             # 后端说明文档
└── app/                  # 应用主目录
    ├── __init__.py       # 包初始化
    ├── main.py           # FastAPI 应用入口
    ├── config/           # 配置模块
    │   ├── settings.py   # 应用配置（数据库、JWT等）
    │   └── database.py   # 异步数据库连接
    ├── models/           # 数据模型层（ORM）
    │   ├── user.py       # 用户表模型
    │   └── data.py       # 电商数据仓库表模型（8张ads_*表）
    ├── schemas/          # 数据校验层（Pydantic）
    │   ├── response.py   # 统一响应格式
    │   └── user.py       # 用户请求/响应Schema
    ├── crud/             # 数据访问层（CRUD操作）
    │   ├── user.py       # 用户增删改查
    │   └── data.py       # 电商数据查询（核心文件）
    ├── routers/          # 路由层（API接口定义）
    │   ├── auth.py       # 认证路由（登录/注册）
    │   └── data.py       # 数据路由（看板/转化/商品/用户洞察）
    └── utils/            # 工具模块
        └── security.py   # JWT和密码安全工具
```

---

## 各文件详解

### 根目录文件

#### `.env`
运行时的环境变量配置，包含数据库连接信息和JWT密钥等敏感信息。**不应提交到Git。**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=retail_analysis_web
SECRET_KEY=xxx
```

#### `.env.example`
环境变量模板文件。新部署时复制为 `.env` 并填写实际值。

#### `requirements.txt`
Python依赖列表，包含以下核心库：

| 依赖 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.109.0 | Web框架 |
| uvicorn | 0.27.0 | ASGI服务器 |
| sqlalchemy[asyncio] | 2.0.25 | 异步ORM |
| aiomysql | 0.2.0 | MySQL异步驱动 |
| pymysql | 1.1.0 | MySQL同步驱动（建表用） |
| python-jose | 3.3.0 | JWT Token处理 |
| bcrypt | 4.1.2 | 密码哈希加密（替代passlib） |
| pydantic | 2.5.3 | 数据验证 |
| pydantic-settings | 2.1.0 | 配置管理 |
| email-validator | 2.1.0 | 邮箱格式验证 |
| python-dotenv | 1.0.0 | 读取.env文件 |

---

### `app/main.py` — 应用入口

**职责**：FastAPI应用的创建和基础配置

**主要内容**：
- **应用创建**：配置标题、描述、版本号、文档URL（`/docs`、`/redoc`）
- **生命周期管理**：启动时自动创建数据库表（`Base.metadata.create_all`），关闭时释放数据库连接
- **CORS中间件**：允许前端（localhost:5173/3000）跨域访问
- **路由注册**：挂载 `auth`（认证）和 `data`（数据）两个路由模块，统一前缀 `/api`
- **健康检查**：`GET /api/health` 返回服务状态

---

### `app/config/` — 配置模块

#### `settings.py` — 应用配置

**职责**：从 `.env` 文件加载环境变量，提供全局配置

**核心类 `Settings`**：
| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| DB_HOST | localhost | MySQL主机 |
| DB_PORT | 3306 | MySQL端口 |
| DB_USER | root | 数据库用户 |
| DB_PASSWORD | "" | 数据库密码 |
| DB_NAME | ecommerce | 数据库名 |
| SECRET_KEY | (默认值) | JWT加密密钥 |
| ALGORITHM | HS256 | JWT加密算法 |
| ACCESS_TOKEN_EXPIRE_MINUTES | 1440 | Token有效期（24小时） |

**计算属性**：
- `DATABASE_URL`：生成异步连接URL `mysql+aiomysql://...`
- `SYNC_DATABASE_URL`：生成同步连接URL `mysql+pymysql://...`

**设计**：使用 `@lru_cache` 实现配置单例模式，避免重复读取 `.env` 文件。

#### `database.py` — 数据库连接

**职责**：创建和管理异步数据库连接

**核心组件**：
- `async_engine`：SQLAlchemy异步引擎（配置连接池预检测、自动回收）
- `AsyncSessionLocal`：异步会话工厂（配置为不自动提交/刷新）
- `Base`：ORM模型基类（所有数据模型继承此类）
- `get_db()`：FastAPI依赖注入函数，每次请求提供一个独立的数据库会话

---

### `app/models/` — 数据模型层

#### `user.py` — 用户表模型

**职责**：定义 `users` 表的ORM结构

**表结构**：
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| username | String(50) | 用户名，唯一索引 |
| email | String(100) | 邮箱，唯一索引 |
| hashed_password | String(255) | bcrypt加密后的密码 |
| created_at | DateTime | 创建时间（自动） |
| updated_at | DateTime | 更新时间（自动） |

#### `data.py` — 电商数据仓库表模型

**职责**：定义8张 `ads_*` 数据仓库表的ORM映射，使用 `extend_existing=True` 声明表已存在于数据库中

| ORM模型类 | 对应表 | 字段 |
|-----------|--------|------|
| `TrafficTrendDaily` | ads_traffic_trend_daily | dt, total_gmv, total_pv, total_uv |
| `ActivityHeatmap` | ads_activity_heatmap | hour_val, week_val, activity_count |
| `CategorySalesStat` | ads_category_sales_stat | category_path, total_sales, sales_count |
| `BrandSalesTop10` | ads_brand_sales_top10 | brand_name, total_sales |
| `ConversionFunnel` | ads_conversion_funnel | step_name, step_value |
| `UserPathSankey` | ads_user_path_sankey | source_node, target_node, flow_value |
| `UserRfmStat` | ads_user_rfm_stat | rfm_segment, user_count |
| `SkuPriceSensitivity` | ads_sku_price_sensitivity | product_id, avg_price, total_sales |

---

### `app/schemas/` — 数据校验层

#### `response.py` — 统一响应格式

**职责**：定义所有API的统一返回格式

```python
class ResponseModel(BaseModel):
    code: int = 200          # 状态码
    message: str = "success" # 提示消息
    data: Optional[Any]      # 实际数据
```

所有接口返回格式统一为 `{code, message, data}`，前端统一解析。

#### `user.py` — 用户相关Schema

**职责**：请求参数验证和响应格式化

| Schema | 用途 | 字段 |
|--------|------|------|
| `UserCreate` | 注册请求 | username(2-50字符), email(合法邮箱), password(6-100字符) |
| `UserLogin` | 登录请求 | username, password |
| `UserResponse` | 用户信息响应 | id, username, email, created_at |
| `Token` | Token响应 | access_token, token_type |
| `TokenData` | Token解码数据 | username |

---

### `app/crud/` — 数据访问层

#### `user.py` — 用户CRUD

**职责**：用户数据的增删改查操作

| 函数 | 说明 |
|------|------|
| `get_user_by_username(db, username)` | 根据用户名查询 |
| `get_user_by_email(db, email)` | 根据邮箱查询 |
| `get_user_by_id(db, user_id)` | 根据ID查询 |
| `create_user(db, user_data)` | 创建新用户（密码自动加密） |

#### `data.py` — 线上零售数据查询 ⭐核心文件

**职责**：使用 SQLAlchemy ORM 的 `select()` 语句查询电商分析数据，支持日期过滤

**读取的数据表与对应函数**：

| 函数 | 数据表 | 字段 | 说明 |
|------|--------|------|------|
| `get_dashboard_metrics()` | ads_traffic_trend_daily | dt, total_gmv, total_pv, total_uv | 计算GMV/PV/UV汇总指标 |
| `get_activity_heatmap()` | ads_activity_heatmap | hour_val, week_val, activity_count | 用户活跃时段热力图 |
| `get_category_sales()` | ads_category_sales_stat | category_path, total_sales | 品类销售旭日图（TOP20） |
| `get_traffic_trend()` | ads_traffic_trend_daily | dt, total_pv, total_uv | PV/UV日趋势折线图 |
| `get_conversion_funnel()` | ads_conversion_funnel | step_name, step_value | 转化漏斗图 |
| `get_sankey_data()` | ads_user_path_sankey | source_node, target_node, flow_value | 用户路径桑基图 |
| `get_brand_top10()` | ads_brand_sales_top10 | brand_name, total_sales | 品牌销售TOP10柱状图 |
| `get_category_wordcloud()` | ads_category_sales_stat | category_path, sales_count | 品类词云 |
| `get_price_sensitivity()` | ads_sku_price_sensitivity | avg_price, total_sales | 价格敏感度散点图 |
| `get_user_segmentation()` | ads_user_rfm_stat | rfm_segment, user_count | 用户RFM分层环形图 |
| `get_prediction_data()` | (模拟数据) | — | 智能预测（待接入真实模型） |

**日期过滤逻辑**：
- 内部辅助函数 `_has_data_in_range()` 检查 `ads_traffic_trend_daily` 表中指定日期范围是否有数据
- 如果无数据（如用户筛选到非10月），所有图表返回空数组/零值
- 只有 `ads_traffic_trend_daily` 有日期字段 `dt`，其他表为月度汇总表

---

### `app/routers/` — 路由层

#### `auth.py` — 认证路由

**职责**：处理用户登录和注册

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 注册新用户。校验用户名/邮箱唯一性，成功返回Token |
| `/api/auth/login` | POST | 用户登录。验证密码，成功返回Token |

**请求体**：
- 注册：`{ username, email, password }`
- 登录：`{ username, password }`

#### `data.py` — 数据路由

**职责**：提供前端大屏所需的所有数据接口

| 接口 | 方法 | 参数 | 返回数据 |
|------|------|------|----------|
| `/api/data/dashboard` | GET | start_date, end_date (可选) | metrics, activityHeatmap, categorySales, pvuvTrend |
| `/api/data/conversion` | GET | 无 | funnel, sankey |
| `/api/data/product` | GET | 无 | brandTop10, categoryWordCloud, priceSensitivity |
| `/api/data/user-insight` | GET | 无 | userSegmentation |
| `/api/data/prediction` | GET | 无 | historical, forecast |

**日期联动**：
- `/api/data/dashboard` 接收 `start_date` 和 `end_date` 查询参数
- 日期参数传递给 `get_dashboard_metrics`、`get_activity_heatmap`、`get_category_sales`、`get_traffic_trend`
- 当日期范围内无数据时，所有指标返回 0 / 空数组

---

### `app/utils/` — 工具模块

#### `security.py` — 安全工具

**职责**：JWT Token管理和密码安全（使用 bcrypt + SHA256）

**改进说明**：
为了解决 `bcrypt` 算法限制密码长度不能超过 72 字节的问题，我们在加密前增加了 **SHA256 预处理**。流程如下：
`用户密码 (任意长度) -> SHA256 (32字节) -> bcrypt 加密 -> 数据库`

| 函数 | 说明 |
|------|------|
| `verify_password(plain, hashed)` | 验证密码：`bcrypt.checkpw(sha256(plain), hashed)` |
| `get_password_hash(password)` | 生成哈希：`bcrypt.hashpw(sha256(plain), salt)` |
| `create_access_token(data, expires_delta)` | 创建JWT Token（默认24小时过期） |
| `decode_token(token)` | 解码JWT Token，返回用户信息 |
| `get_current_user(token, db)` | FastAPI依赖注入：从Token获取当前用户对象 |

---

## API 调用流程

```
前端请求 → FastAPI路由(routers/) → CRUD函数(crud/) → MySQL数据库
                                       ↓
                              Pydantic校验(schemas/)
                                       ↓
                              统一ResponseModel返回
```

## 数据库连接说明

```
前端 → API请求 → FastAPI → get_db()依赖注入 → AsyncSession → MySQL
                              ↑
                        settings.py (.env)
```

- **异步驱动**：使用 `aiomysql` 实现非阻塞数据库访问
- **连接池**：SQLAlchemy自动管理，配置预检测(`pool_pre_ping`)和自动回收(`pool_recycle=3600`)
- **数据库**：`retail_analysis_web`（Hive数据仓库导出到MySQL的ADS层表）
