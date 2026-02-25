#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["requests"]
# ///

import json
import os
import requests
from datetime import datetime

ZONE_ID = "WLY01"
CACHE_DIR = os.path.expanduser("~/.alfred_prayer_cache")
os.makedirs(CACHE_DIR, exist_ok=True)


# ----------------------------
# Cache Helpers
# ----------------------------

def cache_path(name):
    return os.path.join(CACHE_DIR, name)


def load_cache(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def save_cache(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


# ----------------------------
# Prayer Labels
# ----------------------------

PRAYER_LABELS = {
    "imsak": "Imsak",
    "fajr": "Subuh",
    "syuruk": "Syuruk",
    "dhuhr": "Zohor",
    "asr": "Asar",
    "maghrib": "Maghrib",
    "isha": "Isya",
}


# ----------------------------
# Fetch & Cache Yearly Data
# ----------------------------

def fetch_prayer_data():
    year = datetime.now().year
    cache_file = cache_path(f"{ZONE_ID}-{year}.json")

    cached = load_cache(cache_file)
    if cached:
        return cached

    url = f"https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=year&zone={ZONE_ID}"
    r = requests.get(url)
    data = r.json()

    save_cache(cache_file, data)
    return data


def load_today():
    data = fetch_prayer_data()
    today = datetime.now().strftime("%d-%b-%Y")

    for day in data.get("prayerTime", []):
        if day["date"] == today:
            return day
    return None


# ----------------------------
# Time Helpers
# ----------------------------

def human_diff(target):
    now = datetime.now()
    diff = target - now
    seconds = int(diff.total_seconds())

    if seconds <= 0:
        return "now"

    mins = seconds // 60
    hours = mins // 60
    mins = mins % 60

    if hours > 0:
        return f"in {hours}h {mins}m"
    return f"in {mins}m"


# ----------------------------
# Build Alfred Items
# ----------------------------

def build_items():
    today = load_today()
    if not today:
        return [{"title": "No prayer data available"}]

    now = datetime.now()
    prayer_times = []

    for key in PRAYER_LABELS:
        raw_time = today[key]
        time_obj = datetime.strptime(raw_time, "%H:%M:%S")
        time_obj = time_obj.replace(
            year=now.year, month=now.month, day=now.day
        )

        prayer_times.append({
            "label": PRAYER_LABELS[key],
            "time": time_obj
        })

    # Determine current prayer
    current_index = 0
    for i, p in enumerate(prayer_times):
        if now >= p["time"]:
            current_index = i

    next_index = (current_index + 1) % len(prayer_times)

    items = []
    for i, p in enumerate(prayer_times):
        title = p["label"]
        subtitle = p["time"].strftime("%I:%M %p")

        if i == current_index:
            title += " (Current)"
        elif i == next_index:
            title += f" ({human_diff(p['time'])})"

        items.append({
            "title": title,
            "subtitle": subtitle,
            "icon": {"path": "./mosque.png"}
        })

    return items


# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":
    output = {
        "items": build_items()
    }
    print(json.dumps(output))