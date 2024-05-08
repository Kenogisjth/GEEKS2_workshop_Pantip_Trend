from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import sqlalchemy as sa
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
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
    "Date Serv": pd.Timestamp.now().strftime('%Y-%m-%d %X'),
    "URL": links,
    "Topic": title_list,
    "Username Owner": username_list
    
})

conn_str = "mysql+pymysql://root:password@host.docker.internal:3306/de_inter"
engine = sa.create_engine(conn_str)
conn = engine.connect()
pantip_trend.to_sql("pantip_trend", conn, index=None, if_exists="append")
conn.close()