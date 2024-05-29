import pandas as pd

data = pd.read_csv("/opt/data/de02/pantip_trend.csv")
data.to_csv("/opt/data/de02/pantip_trend_data.csv", index=False)