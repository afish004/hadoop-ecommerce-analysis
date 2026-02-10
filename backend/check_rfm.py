import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='retail_analysis_web', charset='utf8mb4')
c = conn.cursor()
c.execute("SELECT * FROM ads_user_rfm_stat")
print("RFM Data:")
for row in c.fetchall():
    print(f"  {row}")
c.close(); conn.close()
