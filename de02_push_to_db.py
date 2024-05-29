import pandas as pd
import sqlalchemy as sa
from urllib.parse import quote

data = pd.read_csv("/opt/data/de02/pantip_trend_data.csv")

conn_info = {"dialect":"mysql+pymysql",
                "hostname":"202.44.12.115",
                "port":"3306",
                "username":"testuser",
                "password":"P@ssw0rd",
                "database":"de_inter_workshop"
                }

conn_str = f'{conn_info["dialect"]}://{conn_info["username"]}:{quote(conn_info["password"])}@{conn_info["hostname"]}:{conn_info["port"]}/{conn_info["database"]}'
engine = sa.create_engine(conn_str)
conn = engine.connect()
data.to_sql("de02_pantip_trend", conn, if_exists="append", index=False)
conn.close()