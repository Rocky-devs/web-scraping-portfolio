import pandas as pd
import folium
from rapidfuzz import process, fuzz

gmap_df = pd.read_csv("New York_restaurants.csv")
nyc_df = pd.read_csv('nyc_restaurant_inspection.csv')

nyc_df['inspection_date'] = pd.to_datetime(nyc_df['inspection_date'])
nyc_df = nyc_df.sort_values('inspection_date', ascending=False).drop_duplicates(subset='camis')
gmap_df['name'] = gmap_df['name'].str.lower()
nyc_df['dba'] = nyc_df['dba'].str.lower()

nyc_names = nyc_df['dba'].tolist()

def fuzzy_match(name, choices, threshold=85):
    result = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if result and result[1] >= threshold:
        return result[0]
    return None

gmap_df['dba_matched'] = gmap_df['name'].apply(lambda x: fuzzy_match(x, nyc_names))
merged = pd.merge(gmap_df, nyc_df, how='left', left_on='dba_matched', right_on='dba')
matched = merged[merged['grade'].notna()].drop_duplicates(subset='name')

# 地图
m = folium.Map(location=[40.7580, -73.9855], zoom_start=13)

GRADE_COLOR = {"A": "green", "B": "orange", "C": "red"}

for _, row in matched.iterrows():
    if pd.isna(row['location_lat']):
        continue
    color = GRADE_COLOR.get(row['grade'], "gray")
    folium.Marker(
        location=[row['location_lat'], row['location_lng']],
        popup=folium.Popup(f"""
            <b>{row['name'].title()}</b><br>
            ⭐ Google Rating: {row['rating']}<br>
            🏥 Health Grade: <b>{row['grade']}</b><br>
            📊 Inspection Score: {int(row['score'])}<br>
            📍 {row['address']}
        """, max_width=250),
        icon=folium.Icon(color=color, icon="cutlery", prefix="fa")
    ).add_to(m)

legend_html = """
<div style="position:fixed; bottom:30px; left:30px; z-index:1000;
     background:white; padding:12px 16px; border-radius:8px;
     box-shadow:0 2px 8px rgba(0,0,0,0.3); font-family:Arial;">
  <b>NYC Restaurant Health Grade</b><br><br>
  🟢 Grade A<br>
  🟠 Grade B<br>
  🔴 Grade C
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
m.save("restaurant_inspector_map.html")
print("地图已保存")