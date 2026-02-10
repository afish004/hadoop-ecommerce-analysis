"""
安全工具模块
JWT Token 生成与验证、密码加密
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config.settings import settings
from ..config.database import get_db
from ..models.user import User
from ..schemas.user import TokenData

import hashlib
import bcrypt

# OAuth2 Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def _hash_password_pre(password: str) -> str:
    """
    预处理密码：先进行 SHA256 哈希
    1. 解决 bcrypt 限制密码长度不能超过 72 字节的问题
    2. 确保密码长度固定为 64 字符（Hex），符合 bcrypt 处理范围
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: 数据库存储的哈希值（字符串格式）
    """
    # 1. SHA256 预处理
    pre_hash = _hash_password_pre(plain_password)
    # 2. bcrypt 验证 (注意：bcrypt 需要 bytes 类型)
    # hashed_password 从数据库取出是 str，需要转为 bytes
    return bcrypt.checkpw(pre_hash.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    :return: 哈希后的字符串（用于存入数据库）
    """
    # 1. SHA256 预处理
    pre_hash = _hash_password_pre(password)
    # 2. bcrypt 加密 (生成 salt 并 hash)
    # hashpw 返回的是 bytes，需要 decode 为 str 存入数据库
    hashed_bytes = bcrypt.hashpw(pre_hash.encode(), bcrypt.gensalt())
    return hashed_bytes.decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """
    解码JWT令牌
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username)
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户（异步依赖注入）
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.username == token_data.username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    
    return user
