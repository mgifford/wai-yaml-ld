#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def fetch_headers(url: str):
    methods = ["HEAD", "GET"]
    last_error = None
    for method in methods:
        try:
            req = Request(url, method=method)
            if method == "GET":
                req.add_header("Range", "bytes=0-0")
            with urlopen(req, timeout=30) as res:
                headers = {k.lower(): v for k, v in res.headers.items()}
                return {
                    "status": getattr(res, "status", None),
                    "etag": headers.get("etag"),
                    "last_modified": headers.get("last-modified"),
                }
        except (URLError, HTTPError) as exc:
            last_error = str(exc)
    return {"status": None, "etag": None, "last_modified": None, "error": last_error}


def load_watchlist(path: Path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or "resources" not in data:
        raise ValueError("watchlist must be an object containing 'resources'")
    return data


def write_watchlist(path: Path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def build_report(resources, changed):
    lines = []
    lines.append("# W3C Source Monitor Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append(f"Changed resources: {len(changed)}")
    lines.append("")
    lines.append("| ID | URL | Previous ETag | Current ETag | Previous Last-Modified | Current Last-Modified |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in resources:
        lines.append(
            "| {id} | {url} | {prev_etag} | {etag} | {prev_last_modified} | {last_modified} |".format(
                id=row.get("id", ""),
                url=row.get("url", ""),
                prev_etag=row.get("prev_etag") or "",
                etag=row.get("etag") or "",
                prev_last_modified=row.get("prev_last_modified") or "",
                last_modified=row.get("last_modified") or "",
            )
        )
    lines.append("")
    if changed:
        lines.append("## Changed IDs")
        lines.append("")
        for row in changed:
            lines.append(f"- {row.get('id')}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Monitor W3C source headers for changes")
    parser.add_argument("--watchlist", required=True, help="Path to watchlist JSON")
    parser.add_argument("--refresh", action="store_true", help="Refresh stored header values")
    parser.add_argument("--check", action="store_true", help="Check for header changes")
    parser.add_argument("--report", help="Write markdown report to this path")
    args = parser.parse_args()

    if not args.refresh and not args.check:
        parser.error("Specify at least one of --refresh or --check")

    watchlist_path = Path(args.watchlist)
    data = load_watchlist(watchlist_path)
    resources = data.get("resources", [])

    changed = []
    report_rows = []

    for resource in resources:
        prev_etag = resource.get("etag")
        prev_last_modified = resource.get("last_modified")

        current = fetch_headers(resource["url"])
        resource["status"] = current.get("status")
        resource["etag"] = current.get("etag")
        resource["last_modified"] = current.get("last_modified")
        resource["checked_at"] = datetime.now(timezone.utc).isoformat()
        if current.get("error"):
            resource["last_error"] = current["error"]
        else:
            resource.pop("last_error", None)

        row = {
            "id": resource.get("id"),
            "url": resource.get("url"),
            "prev_etag": prev_etag,
            "etag": resource.get("etag"),
            "prev_last_modified": prev_last_modified,
            "last_modified": resource.get("last_modified"),
        }
        report_rows.append(row)

        etag_changed = prev_etag and resource.get("etag") and prev_etag != resource.get("etag")
        lm_changed = prev_last_modified and resource.get("last_modified") and prev_last_modified != resource.get("last_modified")
        if etag_changed or lm_changed:
            changed.append(row)

    data["updated"] = datetime.now(timezone.utc).isoformat()

    if args.refresh:
        write_watchlist(watchlist_path, data)

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(build_report(report_rows, changed))

    print(f"checked={len(resources)} changed={len(changed)}")

    if args.check and changed:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
