#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from urllib import error, request

URL_RE = re.compile(r"https?://[^\s<>'\")\]]+")
DATED_TR_RE = re.compile(r"^https?://www\.w3\.org/TR/\d{4}/")


def expand_inputs(includes: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in includes:
        matches = sorted(Path().glob(pattern))
        for match in matches:
            if match.is_file() and match not in seen:
                files.append(match)
                seen.add(match)
    return files


def extract_urls(text: str) -> set[str]:
    found: set[str] = set()
    for raw in URL_RE.findall(text):
        cleaned = raw.rstrip('.,;:`')
        found.add(cleaned)
    return found


def should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return host in {"localhost", "127.0.0.1"}


def check_url(url: str, timeout: int) -> tuple[bool, str]:
    headers = {"User-Agent": "wai-yaml-ld-link-check/1.0 (+https://github.com/mgifford/wai-yaml-ld)"}
    req_head = request.Request(url, method="HEAD", headers=headers)
    try:
        with request.urlopen(req_head, timeout=timeout) as response:
            code = response.getcode() or 0
            if 200 <= code < 400:
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except error.HTTPError as exc:
        if exc.code in (405, 403):
            req_get = request.Request(url, method="GET", headers=headers)
            try:
                with request.urlopen(req_get, timeout=timeout) as response:
                    code = response.getcode() or 0
                    if 200 <= code < 400:
                        return True, f"HTTP {code} (GET fallback)"
                    return False, f"HTTP {code} (GET fallback)"
            except Exception as get_exc:
                return False, f"{type(get_exc).__name__}: {get_exc}"
        return False, f"HTTPError {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def write_report(
    report_path: Path,
    checked_urls: Iterable[str],
    broken: list[tuple[str, str]],
    dated_tr_urls: list[str],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Resource Link Check Report")
    lines.append("")
    lines.append(f"- URLs checked: {len(list(checked_urls))}")
    lines.append(f"- Broken URLs: {len(broken)}")
    lines.append(f"- Dated W3C TR URLs detected: {len(dated_tr_urls)}")
    lines.append("")

    if broken:
        lines.append("## Broken URLs")
        lines.append("")
        for url, message in broken:
            lines.append(f"- {url} :: {message}")
        lines.append("")

    if dated_tr_urls:
        lines.append("## Dated W3C TR URLs")
        lines.append("")
        lines.append("These URLs point to dated snapshots under /TR/YYYY/. Prefer the shortname alias under /TR/<shortname>/ when possible.")
        lines.append("")
        for url in dated_tr_urls:
            lines.append(f"- {url}")
        lines.append("")

    if not broken and not dated_tr_urls:
        lines.append("All checked links resolved and no dated W3C TR snapshot URLs were found.")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check URLs in repository resources and flag dated W3C TR URLs")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Glob pattern to include files (repeatable)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=20,
        help="Per-request timeout in seconds",
    )
    parser.add_argument(
        "--report",
        default="monitoring/resource-link-report.md",
        help="Path to markdown report output",
    )
    args = parser.parse_args()

    includes = args.include or [
        "README.md",
        "*.md",
        "*.yaml",
        "kitty-specs/001-wai-standards-yaml-ld-ingestion/research/**/*.yaml",
    ]

    files = expand_inputs(includes)
    if not files:
        raise SystemExit("no files matched the include patterns")

    all_urls: set[str] = set()
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        all_urls.update(extract_urls(text))

    broken: list[tuple[str, str]] = []
    dated_tr_urls: list[str] = []
    for url in sorted(all_urls):
        if should_skip_url(url):
            continue
        ok, message = check_url(url, timeout=args.timeout_seconds)
        if not ok:
            broken.append((url, message))
        if DATED_TR_RE.match(url):
            dated_tr_urls.append(url)

    report_path = Path(args.report)
    write_report(report_path, all_urls, broken, dated_tr_urls)

    if broken or dated_tr_urls:
        for url, message in broken:
            print(f"FAIL: {url} :: {message}")
        for url in dated_tr_urls:
            print(f"FAIL: dated W3C TR URL detected :: {url}")
        raise SystemExit(2)

    print(f"ok: checked {len(all_urls)} URLs, no failures")


if __name__ == "__main__":
    main()
