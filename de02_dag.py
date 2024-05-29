from airflow.models.dag import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime, timedelta

def pantip_trend(links, conn_info):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import requests
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import sqlalchemy as sa
    from urllib.parse import quote
    import ast

    links = ast.literal_eval(links)
    conn_info = ast.literal_eval(conn_info)

    place_list = []
    image_list = []
    for place in links.keys():
        place_list.append(place)
        image_list.append(requests.get(links[place]).content)

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
        "Date Serv": pd.Timestamp.now(tz='Asia/Bangkok').strftime('%Y-%m-%d %X'),
        "URL": links,
        "Topic": title_list,
        "Username Owner": username_list
    
    })

    pantip_trend.to_csv("/opt/data/de02/pantip_trend.csv", index=False)

    data = pd.read_csv("/opt/data/de02/pantip_trend.csv")
    data.to_csv("/opt/data/de02/pantip_trend_data.csv", index=False)

    conn_str = f'{conn_info["dialect"]}://{conn_info["username"]}:{quote(conn_info["password"])}@{conn_info["hostname"]}:{conn_info["port"]}/{conn_info["database"]}'
    engine = sa.create_engine(conn_str)
    conn = engine.connect()
    data.to_sql("de02_pantip_trend", conn, if_exists="append", index=False)
    conn.close()

default_args = {
    "owner": "de02",
    "start_date": datetime(2024, 5, 18),
    "retries": 1,
    "retry_delay": timedelta(seconds=15)
}

with DAG(
    dag_id="de02_pantip_trend",
    schedule_interval="0 * * * *",
    catchup=False,
    tags=["example"],
    default_args=default_args
) as dag:
    
    start = EmptyOperator(task_id="start") 

    prepare = PythonVirtualenvOperator( task_id="prepare",
                                        python_callable=pantip_trend,
                                        requirements=["pandas==2.2", "sqlalchemy==2.0.30", "pymysql", "urllib3", "requests", "selenium"],
                                        system_site_packages=False,
                                        op_kwargs={"links":Variable.get("pantip_link"),
                                                    "conn_info":Variable.get("db_conn_info"),
                            }
    ) 

    # task_1 = BashOperator(task_id="download_data",
    #                       bash_command="python /opt/data/de02/de02_download_data.py"
    # )

    # task_2 = BashOperator(task_id="prep_data",
    #                       bash_command="python /opt/data/de02/de02_prep_data.py"
    # )

    # task_3 = BashOperator(task_id="push_data",
    #                       bash_command="python /opt/data/de02/de02_push_to_db.py"
    # )

    end = EmptyOperator(task_id="end")

start >> prepare >> end
# start >> prepare >> task_1 >> task_2 >> task_3 >> end