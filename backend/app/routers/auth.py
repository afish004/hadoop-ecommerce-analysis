"""
认证路由模块
处理用户登录和注册
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from ..config.database import get_db
from ..config.settings import settings
from ..schemas.user import UserCreate, UserLogin
from ..schemas.response import ResponseModel
from ..crud import user as user_crud
from ..utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ResponseModel)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    用户注册接口
    """
    # 检查用户名是否已存在
    existing_user = await user_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        return ResponseModel(code=400, message="用户名已存在，请更换！", data=None)
    
    # 检查邮箱是否已存在
    existing_email = await user_crud.get_user_by_email(db, user_data.email)
    if existing_email:
        return ResponseModel(code=400, message="邮箱已被注册，请更换！", data=None)
    
    # 创建新用户
    new_user = await user_crud.create_user(db, user_data)
    
    # 生成Token
    access_token = create_access_token(
        data={"sub": new_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return ResponseModel(
        code=200,
        message="注册成功！",
        data={
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            },
            "token": access_token
        }
    )


@router.post("/login", response_model=ResponseModel)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    """
    # 查找用户
    user = await user_crud.get_user_by_username(db, user_data.username)
    
    if not user:
        return ResponseModel(code=401, message="用户名或密码错误！", data=None)
    
    # 验证密码
    if not verify_password(user_data.password, user.hashed_password):
        return ResponseModel(code=401, message="用户名或密码错误！", data=None)
    
    # 生成Token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return ResponseModel(
        code=200,
        message="登录成功！",
        data={
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "token": access_token
        }
    )
