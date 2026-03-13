#!/usr/bin/env -S uv run

import json
import sys
import urllib.parse
import urllib.request

API_KEY = "24c806a4f41eb4cc81c3e716b27d7d1f"

query = sys.argv[1]

if not query:
    print(json.dumps({"items": []}))
    sys.exit(0)

encoded_query = urllib.parse.quote(query)
url = (
    f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={encoded_query}"
)

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

items = []

for movie in data.get("results", [])[:10]:
    title = movie.get("title")
    desc = movie.get("overview")
    year = movie.get("release_date", "")[:4]
    movie_id = movie.get("id")

    items.append(
        {
            "title": f"{title} ({year})",
            "subtitle": f"{desc}",
            "arg": f"https://www.themoviedb.org/movie/{movie_id}",
        }
    )

print(json.dumps({"items": items}))
