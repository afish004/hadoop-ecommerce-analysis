"""
用户数据模型（SQLAlchemy 2.0 新式声明映射）
使用 Mapped + mapped_column 提供完整类型提示
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from ..config.database import Base


class User(Base):
    """用户表模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="加密后的密码")
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now(), comment="创建时间")
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
