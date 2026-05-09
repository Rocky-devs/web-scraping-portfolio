# NYC Restaurant Inspector 🍽️

Cross-source restaurant analysis combining NYC Open Data health inspections with Google Maps ratings.

## What This Does
- Fetches **10,000+ NYC restaurant health inspection records** from Socrata Open Data API
- Deduplicates to **8,168 unique restaurants** (latest inspection per restaurant)
- **Fuzzy-matches** inspection records with Google Maps ratings data
- Reveals correlation between health grades and customer ratings

## Key Finding
> All matched high-rated restaurants (4.1+ stars on Google Maps) hold **NYC Grade A** health certifications — suggesting customer ratings and hygiene standards are positively correlated.

## Tech Stack
- Python, Requests, Pandas
- Socrata Open Data API (NYC Department of Health)
- RapidFuzz (fuzzy string matching)

## Data Pipeline

1. Fetch 10,000+ records from Socrata API
2. Deduplicate by `camis` → 8,168 unique restaurants
3. Fuzzy match with Google Maps data (threshold: 85%)
4. Cross-source analysis: health grade vs. customer rating
