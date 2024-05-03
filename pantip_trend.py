#!/usr/bin/env python
# coding: utf-8

# # HW

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By 
import numpy as np
import pandas as pd
from time import sleep


# In[2]:


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options)

driver.get("https://pantip.com/forum/lumpini")

alist = driver.find_elements(By.XPATH, "//h2/a[contains(@class,'gtm-pantip-trend')]")

links = []
for item in alist:
    links.append(item.get_attribute("href"))

links = list(np.unique(np.array(links)))
print(len(links))
print(links)


# In[5]:


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


# In[6]:


df = pd.DataFrame({
    "วันที่และเวลาที่ข้อมูลถูกดึงมาเก็บไว้": pd.Timestamp.now().strftime('%Y-%m-%d %X'),
    "URL": links,
    "หัวข้อกระทู้": title_list,
    "Username ของผู้ตั้งกระทู้": username_list
    
})
df

