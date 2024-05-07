from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import sqlalchemy as sa
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options)

driver.get("https://pantip.com/forum/lumpini")

alist = driver.find_elements(By.XPATH, "//h2/a[contains(@class,'gtm-pantip-trend')]")

links = []
for item in alist:
    links.append(item.get_attribute("href"))

links = list(np.unique(np.array(links)))

title_list = []
username_list = []

for url in links:
    driver.get(url)
    title = driver.find_element(By.CLASS_NAME, "display-post-title").text
    owner = driver.find_element(By.CLASS_NAME, "owner")
    username = owner.text

    title_list.append(title)
    username_list.append(username)

driver.quit()

pantip_trend = pd.DataFrame({
    "วันที่และเวลาที่ข้อมูลถูกดึงมาเก็บไว้": pd.Timestamp.now().strftime('%Y-%m-%d %X'),
    "URL": links,
    "หัวข้อกระทู้": title_list,
    "Username ของผู้ตั้งกระทู้": username_list
    
})

conn_str = f"mysql+pymysql://root:password@localhost:3306/de_inter"
engine = sa.create_engine(conn_str)
conn = engine.connect()
pantip_trend.to_sql("pantip_trend", conn, index=None, if_exists="append")
conn.close()