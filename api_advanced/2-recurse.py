#!/usr/bin/python3
"""Recursively query the Reddit API for all hot article titles."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list of titles of all hot articles for a given subreddit.

    Uses recursion to page through the Reddit API results.
    If the subreddit is invalid, return None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alche-scripting:api-advanced:v1.0 (by /u/alche_student)"}
    params = {"limit": 100, "after": after}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json().get("data", {})
    except ValueError:
        return None

    children = data.get("children", [])

    if not children and not hot_list:
        return None

    for post in children:
        hot_list.append(post.get("data", {}).get("title"))

    next_after = data.get("after")

    if next_after is None:
        return hot_list

    return recurse(subreddit, hot_list, next_after)
