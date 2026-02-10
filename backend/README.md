# 电商数据分析平台 - 后端服务

基于 FastAPI 的后端API服务（异步版本）

## 项目结构

```
backend/
├── app/
│   ├── main.py                 # 应用入口
│   ├── config/                 # 配置模块
│   │   ├── settings.py         # 应用配置
│   │   └── database.py         # 异步数据库连接
│   ├── models/                 # 模型模块
│   │   └── user.py             # 用户模型
│   ├── schemas/                # Schema模块
│   │   ├── user.py             # 用户Schema
│   │   └── response.py         # 响应格式
│   ├── crud/                   # CRUD模块
│   │   ├── user.py             # 用户增删改查
│   │   └── data.py             # 数据读取
│   ├── routers/                # 路由模块
│   │   ├── auth.py             # 认证路由
│   │   └── data.py             # 数据路由
│   └── utils/                  # 工具模块
│       └── security.py         # JWT安全
├── .env                        # 环境配置
└── requirements.txt            # 依赖
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `.env` 文件：

```env
DB_PASSWORD=你的MySQL密码
DB_NAME=你的数据库名
```

### 3. 启动服务

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 4. 访问API文档

`http://localhost:8000/docs`

## API接口

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录

### 数据
- `GET /api/data/dashboard` - 运营看板
- `GET /api/data/conversion` - 转化数据
- `GET /api/data/product` - 商品数据
- `GET /api/data/user-insight` - 用户洞察
- `GET /api/data/prediction` - 预测数据（模拟）
