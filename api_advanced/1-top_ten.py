#!/usr/bin/python3
"""Query Reddit API and print the first 10 hot posts."""

import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code != 200:
        print(None)
        return

    data = response.json()

    posts = data.get("data", {}).get("children", [])

    for post in posts[:10]:
        print(post["data"]["title"])
