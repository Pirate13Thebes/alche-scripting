#!/usr/bin/python3
"""Recursively query the Reddit API and count keyword occurrences
in hot post titles."""
import requests


def count_words(subreddit, word_list, instances=None, after=None):
    """Print a sorted count of given keywords found in hot post titles.

    Recursively pages through the Reddit API. Prints nothing if the
    subreddit is invalid or no keywords match.
    """
    if instances is None:
        instances = {}
        normalized = [word.lower() for word in word_list]
        for word in normalized:
            instances.setdefault(word, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alche-scripting:api-advanced:v1.0 (by /u/alche_student)"}
    params = {"limit": 100, "after": after}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    try:
        data = response.json().get("data", {})
    except ValueError:
        return

    children = data.get("children", [])

    for post in children:
        title = post.get("data", {}).get("title", "")
        for token in title.lower().split():
            cleaned = "".join(
                char for char in token if char.isalnum())
            if cleaned in instances:
                instances[cleaned] += 1

    next_after = data.get("after")

    if next_after is not None:
        count_words(subreddit, word_list, instances, next_after)
        return

    results = [(word, count) for word, count in instances.items()
               if count > 0]
    results.sort(key=lambda item: (-item[1], item[0]))

    for word, count in results:
        print("{}: {}".format(word, count))
