"""
用户相关的 Pydantic Schema
用于请求/响应数据验证
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """用户注册请求Schema"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserLogin(BaseModel):
    """用户登录请求Schema"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    """用户信息响应Schema"""
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应Schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token解析后的数据"""
    username: Optional[str] = None
