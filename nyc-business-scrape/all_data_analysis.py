import pandas as pd
import folium
import glob
import os

# 读取所有New York的CSV
all_dfs = []
for file in glob.glob("New York_*.csv"):
    industry = file.replace("New York_", "").replace(".csv", "")
    df = pd.read_csv(file)
    df["industry"] = industry
    all_dfs.append(df)

df = pd.concat(all_dfs, ignore_index=True)

# 去掉没有坐标的行
df = df.dropna(subset=["location_lat", "location_lng"])
print(f"有效数据：{len(df)} 条")

# 行业颜色映射
COLOR_MAP = {
    "restaurants": "red",
    "real estate agency": "blue",
    "dental clinic": "green",
    "gym": "orange",
    "auto repair": "purple"
}

# 创建地图，中心定在曼哈顿
m = folium.Map(location=[40.7282, -73.9942], zoom_start=13)

# 每条数据加一个圆点
for _, row in df.iterrows():
    color = COLOR_MAP.get(row["industry"], "gray")
    folium.CircleMarker(
        location=[row["location_lat"], row["location_lng"]],
        radius=6,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(
            f"""
            <b>{row['name']}</b><br>
            {row['address']}<br>
            ⭐ {row['rating']} ({row['reviews']} reviews)<br>
            📞 {row['phone']}<br>
            🏷️ {row['industry']}
            """,
            max_width=250
        )
    ).add_to(m)

# 加图例（手写HTML）
legend_html = """
<div style="position:fixed; bottom:30px; left:30px; z-index:1000;
     background:white; padding:12px 16px; border-radius:8px;
     box-shadow:0 2px 8px rgba(0,0,0,0.3); font-family:Arial;">
  <b>New York Business Data</b><br><br>
  🔴 Restaurants<br>
  🔵 Real Estate Agency<br>
  🟢 Dental Clinic<br>
  🟠 Gym<br>
  🟣 Auto Repair
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

m.save("new_york_map.html")
print("地图已保存 → new_york_map.html")
