import requests
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_KEY = "YOU_API_KEY"
API_SECRET = "YOU_API_SECRET"
TARGETS = {
    "New York": {"location": "40.7580,-73.9855", "industries": ["restaurants", "real estate agency",
                                                                'dental clinic', 'gym', 'auto repair']},
}

TYPE_MAP = {
    "restaurants": "restaurant",
    "real estate agency": "real_estate_agency",
    "dental clinic": "dentist",
    "gym": "gym",
    "auto repair": "car_repair"
}

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def search_places(query, location, radius=5000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    results = []
    params = {
        "query": query,
        "location": location,  # "35.6762,139.6503" 纬度,经度
        "radius": radius,
        "type": TYPE_MAP.get(query, ""),
        "key": API_KEY
    }

    while True:
        res = session.get(url, params=params).json()
        results.extend(res.get("results", []))

        next_token = res.get("next_page_token")
        print(f"next_page_token: {next_token}")
        if not next_token:
            break

        time.sleep(2)  # 必须等，token有延迟
        params = {"pagetoken": next_token, "key": API_KEY}

    return results


def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "geometry,name,formatted_address,formatted_phone_number,rating,user_ratings_total,opening_hours,price_level,website,types",
        "key": API_KEY
    }
    res = session.get(url, params=params).json()
    return res.get("result", {})


def save_to_csv(data, filename):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"已保存 {len(data)} 条 → {filename}")


# 主流程

for city, info in TARGETS.items():
    for industry in info['industries']:
        raw = search_places(industry, info['location'])
        all_data = []
        for i, place in enumerate(raw):
            detail = get_place_details(place.get('place_id'))
            row = {
                'city': city,
                "name": detail.get("name"),
                "address": detail.get("formatted_address"),
                'location_lat': detail.get('geometry', {}).get('location').get('lat'),
                'location_lng': detail.get('geometry', {}).get('location').get('lng'),
                "phone": detail.get("formatted_phone_number"),
                "rating": detail.get("rating"),
                "reviews": detail.get("user_ratings_total"),
                "price_level": detail.get("price_level"),
                "website": detail.get("website"),
                "open_now": detail.get("opening_hours", {}).get("open_now"),
            }
            all_data.append(row)
            print(f"[{i + 1}/{len(raw)}] {row['name']}")
            time.sleep(0.5)

        save_to_csv(all_data, f'{city}_{industry}.csv')
