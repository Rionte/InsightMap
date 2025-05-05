# 🗺️ InsightMap

InsightMap is a smart location-based search assistant powered by Google Maps API. It helps users find places nearby based on specific filters like category, distance, rating, and price — all inside a sleek PySide6 GUI.

## 🚀 Features

- 🔍 Search by address and location type
- ⭐ Filter by minimum star rating (1–5 stars)
- 📏 Limit by distance (1–50 km)
- 💰 Choose minimum and maximum price level
- 📂 Category + subcategory filtering (e.g., Restaurants → BBQ)
- 📍 View results with name, rating, price level, types
- 🗺️ Live map preview using OpenStreetMap
- ✨ Clean dark mode UI with intuitive layout

## 🛠️ Built With

- [PySide6](https://doc.qt.io/qtforpython/) – Python bindings for Qt GUI
- [Google Maps API](https://developers.google.com/maps/documentation/places/web-service/overview)
- [OpenStreetMap](https://www.openstreetmap.org/) for embedded map display
- Python 3.x

## 📦 Installation

```bash
git clone https://github.com/Rionte/SmartAlarm.git
cd SmartAlarm  # or your correct folder
```
pip install -r requirements.txt

## ADD YOUR OWN GOOGLE API KEY

gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')

## To run

python insightmap.py
