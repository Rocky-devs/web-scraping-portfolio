# NYC Business Scraper 🗽

A multi-industry business data pipeline for New York City using Google Maps Places API.

## What This Does
- Scrapes 5 business categories across Manhattan: **Restaurants, Real Estate, Dental Clinics, Gyms, Auto Repair**
- Fetches detailed info: name, address, phone, rating, review count, coordinates
- Visualizes all 300 data points on an interactive map with color-coded categories

## Tech Stack
- Python, Requests
- Google Maps Places API (Nearby Search + Place Details)
- Folium (interactive map)
- Pandas

## Key Features
- Multi-industry pipeline with a single config (`TARGETS` dict)
- Automatic pagination via `next_page_token`
- Retry logic for network resilience
- Interactive HTML map with clickable popups

## Output
- Per-industry CSV files (`New York_restaurants.csv`, etc.)
- Interactive map: `new_york_map.html`

## Map Preview
![NYC Business Map](screenshot.png)

## Data Sample
| Name | Industry | Rating | Reviews |
|------|----------|--------|---------|
| Per Se | Restaurant | 4.5 | 3,421 |
| Equinox | Gym | 4.3 | 891 |
| NYU Dentistry | Dental | 4.2 | 1,204 |

## Usage
```bash
pip install requests pandas folium
python google_map.py
python visualize.py
```
Set your API key in `google_map.py`:
```python
API_KEY = "your_google_maps_api_key"
```
