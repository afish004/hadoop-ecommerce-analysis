"""
电商数据仓库 ADS 层表 ORM 模型（SQLAlchemy 2.0 新式声明映射）
使用 Mapped + mapped_column 提供完整类型提示
这些表由 Hive 数据仓库导出到 MySQL，后端只读不写
"""
from datetime import date
from decimal import Decimal
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..config.database import Base


class TrafficTrendDaily(Base):
    """每日流量趋势表"""
    __tablename__ = "ads_traffic_trend_daily"
    __table_args__ = {'extend_existing': True}

    dt: Mapped[date] = mapped_column(primary_key=True, comment="日期")
    total_gmv: Mapped[Decimal] = mapped_column(comment="当日总销售额")
    total_pv: Mapped[int] = mapped_column(comment="当日总浏览量")
    total_uv: Mapped[int] = mapped_column(comment="当日独立访客数")

    def __repr__(self):
        return f"<TrafficTrendDaily(dt={self.dt}, pv={self.total_pv}, uv={self.total_uv})>"


class ActivityHeatmap(Base):
    """用户活跃时段热力图表"""
    __tablename__ = "ads_activity_heatmap"
    __table_args__ = {'extend_existing': True}

    hour_val: Mapped[int] = mapped_column(primary_key=True, comment="小时(0-23)")
    week_val: Mapped[int] = mapped_column(primary_key=True, comment="星期(0-6)")
    activity_count: Mapped[int] = mapped_column(comment="活跃次数")

    def __repr__(self):
        return f"<ActivityHeatmap(hour={self.hour_val}, week={self.week_val}, count={self.activity_count})>"


class CategorySalesStat(Base):
    """品类销售统计表"""
    __tablename__ = "ads_category_sales_stat"
    __table_args__ = {'extend_existing': True}

    category_path: Mapped[str] = mapped_column(String(255), primary_key=True, comment="品类路径")
    total_sales: Mapped[Decimal] = mapped_column(comment="总销售额")
    sales_count: Mapped[int] = mapped_column(comment="销售笔数")

    def __repr__(self):
        return f"<CategorySalesStat(path={self.category_path}, sales={self.total_sales})>"


class BrandSalesTop10(Base):
    """品牌销售TOP10表"""
    __tablename__ = "ads_brand_sales_top10"
    __table_args__ = {'extend_existing': True}

    brand_name: Mapped[str] = mapped_column(String(255), primary_key=True, comment="品牌名称")
    total_sales: Mapped[Decimal] = mapped_column(comment="总销售额")

    def __repr__(self):
        return f"<BrandSalesTop10(brand={self.brand_name}, sales={self.total_sales})>"


class ConversionFunnel(Base):
    """转化漏斗表"""
    __tablename__ = "ads_conversion_funnel"
    __table_args__ = {'extend_existing': True}

    step_name: Mapped[str] = mapped_column(String(100), primary_key=True, comment="漏斗步骤名称")
    step_value: Mapped[int] = mapped_column(comment="步骤数值")

    def __repr__(self):
        return f"<ConversionFunnel(step={self.step_name}, value={self.step_value})>"


class UserPathSankey(Base):
    """用户路径桑基图表"""
    __tablename__ = "ads_user_path_sankey"
    __table_args__ = {'extend_existing': True}

    source_node: Mapped[str] = mapped_column(String(100), primary_key=True, comment="来源节点")
    target_node: Mapped[str] = mapped_column(String(100), primary_key=True, comment="目标节点")
    flow_value: Mapped[int] = mapped_column(comment="流量值")

    def __repr__(self):
        return f"<UserPathSankey(source={self.source_node}, target={self.target_node}, flow={self.flow_value})>"


class UserRfmStat(Base):
    """用户RFM分层统计表"""
    __tablename__ = "ads_user_rfm_stat"
    __table_args__ = {'extend_existing': True}

    rfm_segment: Mapped[str] = mapped_column(String(100), primary_key=True, comment="RFM分层名称")
    user_count: Mapped[int] = mapped_column(comment="用户数量")

    def __repr__(self):
        return f"<UserRfmStat(segment={self.rfm_segment}, count={self.user_count})>"


class SkuPriceSensitivity(Base):
    """SKU价格敏感度表"""
    __tablename__ = "ads_sku_price_sensitivity"
    __table_args__ = {'extend_existing': True}

    product_id: Mapped[str] = mapped_column(String(100), primary_key=True, comment="商品ID")
    avg_price: Mapped[Decimal] = mapped_column(comment="平均价格")
    total_sales: Mapped[int] = mapped_column(comment="总销量")

    def __repr__(self):
        return f"<SkuPriceSensitivity(id={self.product_id}, price={self.avg_price}, sales={self.total_sales})>"
