#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "things-py>=1.0.1",
# ]
# ///

import json
import sys

import things


def show_today():
    tasks = things.today()

    items = []

    for t in tasks:
        items.append(
            {
                "title": t["title"],
                "subtitle": t.get("area_title", ""),
                "arg": t["uuid"],
                "icon": {"path": "./todo.png"},
            }
        )

    output = {"items": items}

    print(json.dumps(output, indent=4))


def main():
    arg = sys.argv[1].lower()

    if arg in {"today", "t"}:
        show_today()
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
