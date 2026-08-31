#!/usr/bin/python3
"""Query the Reddit API and print the titles of the first 10 hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a given subreddit.

    If the subreddit is invalid, print None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alche-scripting:api-advanced:v1.0 (by /u/alche_student)"}
    params = {"limit": 10}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        print(None)
        return

    try:
        children = response.json().get("data", {}).get("children", [])
    except ValueError:
        print(None)
        return

    if not children:
        print(None)
        return

    for post in children:
        print(post.get("data", {}).get("title"))
