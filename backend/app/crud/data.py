"""
数据CRUD操作（ORM版本）
使用 SQLAlchemy ORM 模型进行数据库查询，替代原生SQL
所有 ads_* 数据仓库表通过 ORM 模型访问
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from ..models.data import (
    TrafficTrendDaily,
    ActivityHeatmap,
    CategorySalesStat,
    BrandSalesTop10,
    ConversionFunnel,
    UserPathSankey,
    UserRfmStat,
    SkuPriceSensitivity,
)


# ==================== 辅助函数 ====================

async def _has_data_in_range(db: AsyncSession, start_date: str, end_date: str) -> bool:
    """
    检查指定日期范围内是否有数据（基于TrafficTrendDaily表）。
    由于数据仅覆盖某一个月（如2019-10），如果用户筛选到其他月份，
    所有图表和数字都应该为空。
    """
    if not start_date or not end_date:
        return True

    result = await db.execute(
        select(func.count()).select_from(TrafficTrendDaily).where(
            TrafficTrendDaily.dt >= start_date,
            TrafficTrendDaily.dt <= end_date
        )
    )
    count = result.scalar()
    return count > 0 if count else False


# ==================== Dashboard数据读取 ====================

async def get_dashboard_metrics(db: AsyncSession, start_date: str = None, end_date: str = None) -> dict:
    """
    获取看板核心指标（GMV/PV/UV）
    支持日期过滤：当日期范围内无数据时返回零值
    """
    empty = {"gmv": 0, "pv": 0, "uv": 0}

    if start_date and end_date:
        has_data = await _has_data_in_range(db, start_date, end_date)
        if not has_data:
            return empty

    try:
        query = select(
            func.sum(TrafficTrendDaily.total_pv).label("pv"),
            func.sum(TrafficTrendDaily.total_uv).label("uv"),
            func.sum(TrafficTrendDaily.total_gmv).label("gmv"),
        )
        if start_date and end_date:
            query = query.where(
                TrafficTrendDaily.dt >= start_date,
                TrafficTrendDaily.dt <= end_date
            )

        result = await db.execute(query)
        row = result.one()
        return {
            "gmv": float(row.gmv) if row.gmv else 0,
            "pv": int(row.pv) if row.pv else 0,
            "uv": int(row.uv) if row.uv else 0,
        }
    except Exception as e:
        print(f"get_dashboard_metrics error: {e}")
        return empty


async def get_activity_heatmap(db: AsyncSession, start_date: str = None, end_date: str = None) -> list:
    """获取活动热力图数据"""
    if start_date and end_date:
        has_data = await _has_data_in_range(db, start_date, end_date)
        if not has_data:
            return []

    try:
        result = await db.execute(
            select(
                ActivityHeatmap.hour_val,
                ActivityHeatmap.week_val,
                ActivityHeatmap.activity_count
            ).order_by(ActivityHeatmap.hour_val, ActivityHeatmap.week_val)
        )
        rows = result.all()
        return [[int(row.hour_val), int(row.week_val), int(row.activity_count)] for row in rows]
    except Exception as e:
        print(f"get_activity_heatmap error: {e}")
        return []


async def get_category_sales(db: AsyncSession, start_date: str = None, end_date: str = None) -> list:
    """获取品类销售数据（旭日图TOP20）"""
    if start_date and end_date:
        has_data = await _has_data_in_range(db, start_date, end_date)
        if not has_data:
            return []

    try:
        result = await db.execute(
            select(
                CategorySalesStat.category_path,
                CategorySalesStat.total_sales
            ).order_by(CategorySalesStat.total_sales.desc()).limit(20)
        )
        rows = result.all()
        return [{"name": str(row.category_path), "value": float(row.total_sales)} for row in rows]
    except Exception as e:
        print(f"get_category_sales error: {e}")
        return []


async def get_traffic_trend(db: AsyncSession, start_date: str = None, end_date: str = None) -> dict:
    """获取流量趋势数据（支持日期过滤）"""
    empty = {
        "xAxis": [],
        "series": [
            {"name": "PV (浏览量)", "data": []},
            {"name": "UV (访客数)", "data": []}
        ]
    }

    try:
        query = select(
            TrafficTrendDaily.dt,
            TrafficTrendDaily.total_pv,
            TrafficTrendDaily.total_uv
        ).order_by(TrafficTrendDaily.dt)

        if start_date and end_date:
            query = query.where(
                TrafficTrendDaily.dt >= start_date,
                TrafficTrendDaily.dt <= end_date
            )

        result = await db.execute(query)
        rows = result.all()

        if rows:
            return {
                "xAxis": [str(row.dt) for row in rows],
                "series": [
                    {"name": "PV (浏览量)", "data": [int(row.total_pv) for row in rows]},
                    {"name": "UV (访客数)", "data": [int(row.total_uv) for row in rows]}
                ]
            }
        return empty
    except Exception as e:
        print(f"get_traffic_trend error: {e}")
        return empty


# ==================== 转化数据读取 ====================

async def get_conversion_funnel(db: AsyncSession) -> list:
    """获取转化漏斗数据"""
    try:
        result = await db.execute(
            select(
                ConversionFunnel.step_name,
                ConversionFunnel.step_value
            ).order_by(ConversionFunnel.step_value.desc())
        )
        rows = result.all()
        return [{"name": str(row.step_name), "value": int(row.step_value)} for row in rows]
    except Exception as e:
        print(f"get_conversion_funnel error: {e}")
        return []


async def get_sankey_data(db: AsyncSession) -> dict:
    """获取桑基图数据"""
    try:
        result = await db.execute(
            select(
                UserPathSankey.source_node,
                UserPathSankey.target_node,
                UserPathSankey.flow_value
            )
        )
        rows = result.all()

        if rows:
            nodes_set = set()
            links = []
            for row in rows:
                source = str(row.source_node)
                target = str(row.target_node)
                value = int(row.flow_value)
                nodes_set.add(source)
                nodes_set.add(target)
                links.append({"source": source, "target": target, "value": value})

            nodes = [{"name": node} for node in nodes_set]
            return {"nodes": nodes, "links": links}
        return {"nodes": [], "links": []}
    except Exception as e:
        print(f"get_sankey_data error: {e}")
        return {"nodes": [], "links": []}


# ==================== 商品数据读取 ====================

async def get_brand_top10(db: AsyncSession) -> dict:
    """获取品牌TOP10"""
    try:
        result = await db.execute(
            select(
                BrandSalesTop10.brand_name,
                BrandSalesTop10.total_sales
            ).order_by(BrandSalesTop10.total_sales.desc()).limit(10)
        )
        rows = result.all()

        if rows:
            return {
                "brands": [str(row.brand_name) for row in rows],
                "sales": [float(row.total_sales) for row in rows]
            }
        return {"brands": [], "sales": []}
    except Exception as e:
        print(f"get_brand_top10 error: {e}")
        return {"brands": [], "sales": []}


async def get_category_wordcloud(db: AsyncSession) -> list:
    """获取品类词云数据"""
    try:
        result = await db.execute(
            select(
                CategorySalesStat.category_path,
                CategorySalesStat.sales_count
            ).order_by(CategorySalesStat.sales_count.desc()).limit(32)
        )
        rows = result.all()
        return [
            {
                "name": str(row.category_path).split('.')[-1] if '.' in str(row.category_path) else str(row.category_path),
                "value": int(row.sales_count)
            }
            for row in rows
        ]
    except Exception as e:
        print(f"get_category_wordcloud error: {e}")
        return []


async def get_price_sensitivity(db: AsyncSession) -> list:
    """获取价格敏感度散点图数据"""
    try:
        result = await db.execute(
            select(
                SkuPriceSensitivity.avg_price,
                SkuPriceSensitivity.total_sales
            ).limit(50)
        )
        rows = result.all()
        return [[float(row.avg_price), int(row.total_sales)] for row in rows]
    except Exception as e:
        print(f"get_price_sensitivity error: {e}")
        return []


# ==================== 用户洞察数据读取 ====================

async def get_user_segmentation(db: AsyncSession) -> list:
    """获取用户分层数据（RFM）"""
    try:
        result = await db.execute(
            select(
                UserRfmStat.rfm_segment,
                UserRfmStat.user_count
            ).order_by(UserRfmStat.user_count.desc())
        )
        rows = result.all()
        return [{"name": str(row.rfm_segment), "value": int(row.user_count)} for row in rows]
    except Exception as e:
        print(f"get_user_segmentation error: {e}")
        return []


# ==================== 智能预测数据（暂用模拟数据） ====================

async def get_prediction_data(db: AsyncSession) -> dict:
    """获取预测数据（暂用模拟数据，表 ads_sku_sales_daily_prediction 预留）"""
    return {
        "historical": {
            "dates": ["10-25", "10-26", "10-27", "10-28", "10-29", "10-30", "10-31"],
            "pv": [180000, 195000, 190000, 185000, 200000, 210000, 205000]
        },
        "forecast": {
            "dates": ["11-01", "11-02", "11-03", "11-04", "11-05", "11-06", "11-07"],
            "pv": [215000, 220000, 218000, 225000, 230000, 240000, 235000],
            "confidenceInterval": {
                "upper": [225000, 230000, 228000, 235000, 245000, 255000, 250000],
                "lower": [205000, 210000, 208000, 215000, 215000, 225000, 220000]
            }
        }
    }
