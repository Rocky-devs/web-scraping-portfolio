import requests
import pandas as pd

APP_TOKEN = "YOUR_APP_TOKEN"



def fetch_restaurant_inspection_data(total=10000, batch=1000):
    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"

    all_data = []
    for offset in range(0, total, batch):
        params = {
            "$limit": batch,
            "$offset": offset,
            "$$app_token": APP_TOKEN
        }
        res = requests.get(url, params=params).json()
        all_data.extend(res)
        print(f"已抓 {len(all_data)} 条")
        if len(res) < batch:  # 不够一批说明到底了
            break
    return all_data


records = fetch_restaurant_inspection_data()

df = pd.DataFrame(records)
df['inspection_date'] = pd.to_datetime(df['inspection_date'])
df_latest = df.sort_values('inspection_date', ascending=False).drop_duplicates(subset='camis')
print(f"去重后：{len(df_latest)} 家餐厅")
