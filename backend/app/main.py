"""
FastAPI 应用入口
电商数据分析平台后端服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config.database import async_engine, Base
from .routers import auth, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时清理资源
    await async_engine.dispose()


# 创建FastAPI应用
app = FastAPI(
    title="电商数据分析平台 API",
    description="Hadoop电商数据分析系统后端服务（异步版）",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(data.router, prefix="/api")


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "电商数据分析平台 API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}
