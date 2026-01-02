#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["folium"]
# ///
import requests
import folium
import time

CALLSIGN = "HA5LA"
OUT_HTML = "map.html"

# Fetch activation data
url = f"https://sotl.as/api/activations/{CALLSIGN}"
data = requests.get(url, timeout=30).json()

# Center map
lats = [a["summit"]["coordinates"]["latitude"] for a in data]
lons = [a["summit"]["coordinates"]["longitude"] for a in data]
center = (sum(lats)/len(lats), sum(lons)/len(lons))

# Create map
m = folium.Map(
    location=center,
    zoom_start=8,
    tiles="OpenStreetMap",
    control_scale=True,
    prefer_canvas=True
)

for a in data:
    folium.Marker(
        location=(a["summit"]["coordinates"]["latitude"], a["summit"]["coordinates"]["longitude"]),
        popup=f'{a["summit"]["code"]} {a["summit"]["name"]} ({a["date"][0:10]})'
    ).add_to(m)

m.save(OUT_HTML)
