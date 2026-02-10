import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='retail_analysis_web', charset='utf8mb4')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM ads_user_path_sankey")
print("Total rows:", c.fetchone()[0])
c.execute("SHOW COLUMNS FROM ads_user_path_sankey")
print("Columns:", [r[0] for r in c.fetchall()])
c.execute("SELECT * FROM ads_user_path_sankey LIMIT 10")
print("Sample data:")
for row in c.fetchall():
    print(f"  {row}")
c.close(); conn.close()
