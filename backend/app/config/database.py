"""
异步数据库连接模块
使用 SQLAlchemy 2.0 异步引擎连接 MySQL
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .settings import settings


# SQLAlchemy 2.0 新式基类
class Base(DeclarativeBase):
    """ORM 模型基类（SQLAlchemy 2.0 DeclarativeBase）"""
    pass


# 创建异步数据库引擎
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:
    """
    获取异步数据库会话的依赖注入函数
    用于FastAPI的Depends
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
