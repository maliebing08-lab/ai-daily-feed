#!/usr/bin/env python3
"""Validate a daily post JSON before pushing.  Usage: python3 tools/validate.py posts/YYYY-MM-DD.json"""
import json, re, sys, pathlib, datetime

def fail(msg):
    print("INVALID:", msg); sys.exit(1)

p = pathlib.Path(sys.argv[1])
m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\.json", p.name)
if not m: fail("file name must be YYYY-MM-DD.json")
try:
    d = json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
    fail(f"not valid JSON: {e}")
if d.get("date") != m.group(1): fail("'date' must equal the file name date")
datetime.date.fromisoformat(d["date"])
for k, lo, hi in (("headline", 8, 26), ("intro", 40, 260), ("excerpt", 50, 80)):
    v = str(d.get(k, "")).strip()
    if not (lo <= len(v) <= hi): fail(f"'{k}' length {len(v)} not in {lo}-{hi}")
tags = d.get("tags")
if not (isinstance(tags, list) and 3 <= len(tags) <= 6 and all(isinstance(t, str) and 1 <= len(t) <= 20 for t in tags)):
    fail("'tags' must be 3-6 short strings")
items = d.get("items")
if not (isinstance(items, list) and 5 <= len(items) <= 8): fail("'items' must have 5-8 entries")
urls = set()
for i, it in enumerate(items, 1):
    for k, lo, hi in (("title", 4, 30), ("summary", 30, 260), ("insight", 15, 160), ("source", 2, 40), ("source_title", 4, 300)):
        v = str(it.get(k, "")).strip()
        if not (lo <= len(v) <= hi): fail(f"item {i} '{k}' length {len(v)} not in {lo}-{hi}")
    u = str(it.get("url", ""))
    if not re.match(r"https?://[^\s]+$", u): fail(f"item {i} bad url")
    if u in urls: fail(f"item {i} duplicate url")
    urls.add(u)
print(f"OK {p.name}: {len(items)} items, headline: {d['headline']}")
