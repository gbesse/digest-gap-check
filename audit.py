#!/usr/bin/env python3
"""Find selected AIHOT items absent as individual links from a daily report."""

import argparse
import datetime as dt
import json
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TEXT = {
    "en": {"title": "Selected items absent from the daily report", "note": "Candidates for editorial review, not proven ingestion failures.", "demo": "Offline fixture; run uses AIHOT's public API.", "incomplete": "INCOMPLETE: pagination limit reached"},
    "fr": {"title": "Articles sélectionnés absents du bulletin", "note": "Candidats à revoir, pas des omissions techniques prouvées.", "demo": "Exemple hors ligne ; run utilise l'API publique AIHOT.", "incomplete": "INCOMPLET : limite de pagination atteinte"},
    "es": {"title": "Artículos seleccionados ausentes del boletín", "note": "Casos para revisión editorial, no fallos de ingesta demostrados.", "demo": "Ejemplo sin conexión; run usa la API pública de AIHOT.", "incomplete": "INCOMPLETO: se alcanzó el límite de paginación"},
}


def get_json(url):
    req = urllib.request.Request(url, headers={"user-agent": "digest-gap-check/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        if not isinstance(exc.reason, ssl.SSLCertVerificationError):
            raise
        # On some macOS Python builds the keychain roots are absent from urllib.
        # curl still verifies the server with the system trust store.
        result = subprocess.run(["curl", "-fsSL", "--max-time", "20", "--", url], capture_output=True, check=True, timeout=25)
        return json.loads(result.stdout)


def collect_report_ids(report):
    ids = set()
    for section in report.get("sections", []):
        for item in section.get("items", []):
            link = (item.get("links") or {}).get("aihot", "")
            path = urllib.parse.urlsplit(link).path.rstrip("/")
            if "/items/" in path:
                item_id = path.rsplit("/items/", 1)[1]
                if item_id and "/" not in item_id:
                    ids.add(urllib.parse.unquote(item_id))
    return ids


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def candidates(report, items):
    start, end = parse_time(report["windowStart"]), parse_time(report["windowEnd"])
    included = collect_report_ids(report)
    rows = []
    for item in items:
        if not item.get("selected"):
            continue
        stamp = item.get("publishedAt") or item.get("discoveredAt")
        if not stamp or not start <= parse_time(stamp) < end:
            continue
        if item["id"] not in included:
            rows.append({"id": item["id"], "title": item.get("title", ""), "publishedAt": stamp, "url": (item.get("links") or {}).get("aihot", "")})
    return rows


def fetch_live(base, day, max_pages=20):
    root = base.rstrip("/")
    daily = get_json(root + "/api/v1/dailies/" + day)["report"]
    items, cursor = [], None
    for _ in range(max_pages):
        query = {"mode": "selected", "window": "7d", "by": "published", "limit": 100}
        if cursor:
            query["cursor"] = cursor
        body = get_json(root + "/api/v1/items?" + urllib.parse.urlencode(query))
        items.extend(body["items"])
        page = body["page"]
        if not page.get("hasMore"):
            return daily, items, False
        cursor = page.get("nextCursor")
        if not cursor:
            raise ValueError("hasMore without nextCursor")
    return daily, items, True


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare AIHOT's selected items with a daily report.")
    ap.add_argument("command", choices=["demo", "run"])
    ap.add_argument("--lang", choices=TEXT, default="en")
    ap.add_argument("--base-url", default="https://aihot.news")
    ap.add_argument("--date", help="YYYY-MM-DD report date")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.command == "demo":
        fixture = json.loads((Path(__file__).parent / "fixtures" / "digest.json").read_text())
        report, items, incomplete = fixture["report"], fixture["items"], False
    else:
        if not args.date:
            ap.error("run requires --date")
        try:
            dt.date.fromisoformat(args.date)
            report, items, incomplete = fetch_live(args.base_url, args.date)
        except (ValueError, OSError, KeyError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            print(str(exc), file=sys.stderr)
            return 2
    rows = candidates(report, items)
    if args.json:
        print(json.dumps({"simulated": args.command == "demo", "incomplete_page_scan": incomplete, "report_date": report.get("date"), "candidates": rows}, ensure_ascii=False, indent=2))
    else:
        print(TEXT[args.lang]["title"])
        if args.command == "demo":
            print(TEXT[args.lang]["demo"])
        print(TEXT[args.lang]["note"])
        for row in rows:
            print(f"{row['id']}: {row['title']} — {row['url']}")
        if incomplete:
            print(TEXT[args.lang]["incomplete"], file=sys.stderr)
    return 2 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
