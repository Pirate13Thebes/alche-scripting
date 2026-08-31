#!/usr/bin/python3
"""Recursively query the Reddit API for all hot post titles.

Contains a single recursive function, recurse, that collects
the titles of all hot articles for a given subreddit, paging
through results until none remain.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Recursively collect the titles of all hot posts in a subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.
        hot_list (list): Accumulator list of post titles collected
            so far across recursive calls.
        after (str): Pagination token for the next page of results.

    Returns:
        list: All hot post titles for the subreddit, or None if
            the subreddit is invalid or has no results.
    """
    if after is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "python3:recurse.script:v1.0 (by /u/alu_student)"
    }
    params = {"limit": 100, "after": after}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    page_data = data.get("data", {})
    posts = page_data.get("children", [])

    if not posts and not hot_list:
        return None

    for post in posts:
        hot_list.append(post.get("data", {}).get("title"))

    next_after = page_data.get("after")
    if next_after is None:
        return hot_list

    return recurse(subreddit, hot_list, next_after)
