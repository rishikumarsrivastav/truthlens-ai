import json
import os
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDIBILITY_PATH = os.path.join(BASE_DIR, "Data", "source_credibility.json")

with open(CREDIBILITY_PATH, "r", encoding="utf-8") as f:
    CREDIBILITY_DB = json.load(f)


def get_host(url):
    parsed = urlparse(url if "://" in url else f"http://{url}")
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def score_domain(url):
    if not url or not url.strip():
        return 50

    try:
        host = get_host(url.strip())
    except ValueError:
        return 50

    parts = host.split(".")
    for i in range(len(parts) - 1):
        domain = ".".join(parts[i:])
        if domain in CREDIBILITY_DB:
            return CREDIBILITY_DB[domain]

    return 50