"""
数据API路由模块
提供看板、转化、商品、用户洞察、预测等数据接口
数据从MySQL数据库异步读取
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..config.database import get_db
from ..schemas.response import ResponseModel
from ..crud import data as data_crud

router = APIRouter(prefix="/data", tags=["数据接口"])


@router.get("/dashboard", response_model=ResponseModel)
async def get_dashboard_data(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取运营看板数据
    包含：指标卡片(GMV/PV/UV)、活动热力图、品类销售、趋势图
    所有数据受日期筛选器控制——日期范围内无数据时全部返回空
    """
    try:
        # 获取核心指标（日期过滤）
        metrics = await data_crud.get_dashboard_metrics(db, start_date, end_date)
        
        # 获取活动热力图（日期过滤）
        activity_heatmap = await data_crud.get_activity_heatmap(db, start_date, end_date)
        
        # 获取品类销售数据（日期过滤）
        category_sales = await data_crud.get_category_sales(db, start_date, end_date)
        
        # 获取流量趋势（日期过滤）
        traffic_trend = await data_crud.get_traffic_trend(db, start_date, end_date)
        
        response_data = {
            "metrics": metrics,
            "activityHeatmap": activity_heatmap,
            "categorySales": category_sales,
            "pvuvTrend": traffic_trend
        }
        
        return ResponseModel(code=200, message="success", data=response_data)
    except Exception as e:
        return ResponseModel(code=500, message=f"获取数据失败: {str(e)}", data=None)


@router.get("/conversion", response_model=ResponseModel)
async def get_conversion_data(db: AsyncSession = Depends(get_db)):
    """
    获取转化数据
    包含：漏斗图、桑基图
    """
    try:
        funnel = await data_crud.get_conversion_funnel(db)
        sankey = await data_crud.get_sankey_data(db)
        
        return ResponseModel(
            code=200,
            message="success",
            data={"funnel": funnel, "sankey": sankey}
        )
    except Exception as e:
        return ResponseModel(code=500, message=f"获取数据失败: {str(e)}", data=None)


@router.get("/product", response_model=ResponseModel)
async def get_product_data(db: AsyncSession = Depends(get_db)):
    """
    获取商品数据
    包含：品牌TOP10、品类词云、价格敏感度散点图
    """
    try:
        brand_top10 = await data_crud.get_brand_top10(db)
        category_wordcloud = await data_crud.get_category_wordcloud(db)
        price_sensitivity = await data_crud.get_price_sensitivity(db)
        
        return ResponseModel(
            code=200,
            message="success",
            data={
                "brandTop10": brand_top10,
                "categoryWordCloud": category_wordcloud,
                "priceSensitivity": price_sensitivity
            }
        )
    except Exception as e:
        return ResponseModel(code=500, message=f"获取数据失败: {str(e)}", data=None)


@router.get("/user-insight", response_model=ResponseModel)
async def get_user_insight_data(db: AsyncSession = Depends(get_db)):
    """
    获取用户洞察数据
    包含：用户分层环形图
    """
    try:
        user_segmentation = await data_crud.get_user_segmentation(db)
        
        return ResponseModel(
            code=200,
            message="success",
            data={"userSegmentation": user_segmentation}
        )
    except Exception as e:
        return ResponseModel(code=500, message=f"获取数据失败: {str(e)}", data=None)


@router.get("/prediction", response_model=ResponseModel)
async def get_prediction_data(db: AsyncSession = Depends(get_db)):
    """
    获取预测数据（暂用模拟数据）
    包含：历史数据、预测数据、置信区间
    """
    try:
        prediction = await data_crud.get_prediction_data(db)
        
        return ResponseModel(code=200, message="success", data=prediction)
    except Exception as e:
        return ResponseModel(code=500, message=f"获取数据失败: {str(e)}", data=None)
