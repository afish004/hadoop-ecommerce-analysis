"""
统一响应格式 Schema
"""
from pydantic import BaseModel
from typing import Any, Optional


class ResponseModel(BaseModel):
    """统一API响应格式，与前端格式一致"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
