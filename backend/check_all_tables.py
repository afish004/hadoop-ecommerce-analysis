import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='retail_analysis_web', charset='utf8mb4')
c = conn.cursor()

# 1. RFM用户分层
print("=== ads_user_rfm_stat (RFM用户分层) ===")
c.execute("SELECT COUNT(*) FROM ads_user_rfm_stat")
print(f"Total rows: {c.fetchone()[0]}")
c.execute("SHOW COLUMNS FROM ads_user_rfm_stat")
print(f"Columns: {[r[0] for r in c.fetchall()]}")
c.execute("SELECT * FROM ads_user_rfm_stat LIMIT 5")
for row in c.fetchall():
    print(f"  {row}")

# 2. 品牌TOP10 (柱状图)
print("\n=== ads_brand_sales_top10 (品牌TOP10柱状图) ===")
c.execute("SELECT COUNT(*) FROM ads_brand_sales_top10")
print(f"Total rows: {c.fetchone()[0]}")
c.execute("SHOW COLUMNS FROM ads_brand_sales_top10")
print(f"Columns: {[r[0] for r in c.fetchall()]}")
c.execute("SELECT * FROM ads_brand_sales_top10 LIMIT 5")
for row in c.fetchall():
    print(f"  {row}")

# 3. 价格敏感度 (散点图)
print("\n=== ads_sku_price_sensitivity (价格敏感度散点图) ===")
c.execute("SELECT COUNT(*) FROM ads_sku_price_sensitivity")
print(f"Total rows: {c.fetchone()[0]}")
c.execute("SHOW COLUMNS FROM ads_sku_price_sensitivity")
print(f"Columns: {[r[0] for r in c.fetchall()]}")
c.execute("SELECT * FROM ads_sku_price_sensitivity LIMIT 5")
for row in c.fetchall():
    print(f"  {row}")

# 4. 流量趋势 (折线图)
print("\n=== ads_traffic_trend_daily (流量趋势折线图) ===")
c.execute("SELECT COUNT(*) FROM ads_traffic_trend_daily")
print(f"Total rows: {c.fetchone()[0]}")
c.execute("SHOW COLUMNS FROM ads_traffic_trend_daily")
print(f"Columns: {[r[0] for r in c.fetchall()]}")
c.execute("SELECT * FROM ads_traffic_trend_daily LIMIT 5")
for row in c.fetchall():
    print(f"  {row}")

# 5. 转化漏斗
print("\n=== ads_conversion_funnel (转化漏斗) ===")
c.execute("SELECT COUNT(*) FROM ads_conversion_funnel")
print(f"Total rows: {c.fetchone()[0]}")
c.execute("SHOW COLUMNS FROM ads_conversion_funnel")
print(f"Columns: {[r[0] for r in c.fetchall()]}")
c.execute("SELECT * FROM ads_conversion_funnel")
for row in c.fetchall():
    print(f"  {row}")

c.close(); conn.close()
