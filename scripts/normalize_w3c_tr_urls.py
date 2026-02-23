#!/usr/bin/env python3
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from urllib import error, request
from urllib.parse import urlparse, urlunparse

URL_RE = re.compile(r"https?://[^\s<>'\")\]]+")
TR_DATED_PATH_RE = re.compile(r"^/TR/(?P<year>\d{4})/(?P<snapshot>[^/]+)/?$")
SNAPSHOT_TOKEN_RE = re.compile(r"^(?:(?:WD|CRD|CR|PR|PER|REC|NOTE)-)?(?P<shortname>.+?)-(?P<date>\d{8})$")


@dataclass
class Candidate:
    original: str
    canonical: str


def expand_inputs(includes: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in includes:
        for match in sorted(Path().glob(pattern)):
            if match.is_file() and match not in seen:
                files.append(match)
                seen.add(match)
    return files


def extract_urls(text: str) -> set[str]:
    found: set[str] = set()
    for raw in URL_RE.findall(text):
        found.add(raw.rstrip('.,;:`'))
    return found


def infer_shortname(snapshot: str) -> str | None:
    token = snapshot.strip()
    match = SNAPSHOT_TOKEN_RE.match(token)
    if not match:
        return None
    shortname = match.group("shortname").strip()
    if not shortname:
        return None
    return shortname


def build_canonical_url(url: str) -> Candidate | None:
    parsed = urlparse(url)
    if (parsed.scheme, parsed.netloc) not in {("https", "www.w3.org"), ("http", "www.w3.org")}:
        return None

    path_match = TR_DATED_PATH_RE.match(parsed.path)
    if not path_match:
        return None

    snapshot = path_match.group("snapshot")
    shortname = infer_shortname(snapshot)
    if not shortname:
        return None

    canonical_path = f"/TR/{shortname}/"
    canonical = urlunparse(("https", "www.w3.org", canonical_path, "", parsed.query, parsed.fragment))
    return Candidate(original=url, canonical=canonical)


def check_url_exists(url: str, timeout: int) -> bool:
    headers = {"User-Agent": "wai-yaml-ld-tr-normalizer/1.0 (+https://github.com/mgifford/wai-yaml-ld)"}
    req_head = request.Request(url, method="HEAD", headers=headers)
    try:
        with request.urlopen(req_head, timeout=timeout) as response:
            code = response.getcode() or 0
            return 200 <= code < 400
    except error.HTTPError as exc:
        if exc.code in (403, 405):
            req_get = request.Request(url, method="GET", headers=headers)
            try:
                with request.urlopen(req_get, timeout=timeout) as response:
                    code = response.getcode() or 0
                    return 200 <= code < 400
            except Exception:
                return False
        return False
    except Exception:
        return False


def replace_urls_in_text(text: str, replacements: dict[str, str]) -> str:
    if not replacements:
        return text

    def repl(match: re.Match[str]) -> str:
        raw = match.group(0)
        stripped = raw.rstrip('.,;:`')
        suffix = raw[len(stripped):]
        if stripped in replacements:
            return replacements[stripped] + suffix
        return raw

    return URL_RE.sub(repl, text)


def write_report(report: Path, changed_files: list[Path], replaced: list[Candidate], skipped: list[str]) -> None:
    report.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# W3C TR URL Normalization Report")
    lines.append("")
    lines.append(f"- Replacements applied: {len(replaced)}")
    lines.append(f"- Files changed: {len(changed_files)}")
    lines.append(f"- Unmappable or unresolved candidates: {len(skipped)}")
    lines.append("")

    if replaced:
        lines.append("## Replacements")
        lines.append("")
        for item in replaced:
            lines.append(f"- {item.original} -> {item.canonical}")
        lines.append("")

    if skipped:
        lines.append("## Skipped")
        lines.append("")
        for item in skipped:
            lines.append(f"- {item}")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize dated W3C TR URLs to canonical shortname aliases when safely mappable")
    parser.add_argument("--include", action="append", default=[], help="Glob pattern to include files (repeatable)")
    parser.add_argument("--report", default="monitoring/tr-url-normalization-report.md", help="Path to markdown report")
    parser.add_argument("--timeout-seconds", type=int, default=20, help="HTTP timeout per request")
    args = parser.parse_args()

    includes = args.include or [
        "README.md",
        "*.md",
        "*.yaml",
        "kitty-specs/001-wai-standards-yaml-ld-ingestion/research/**/*.yaml",
    ]

    files = expand_inputs(includes)
    if not files:
        raise SystemExit("no files matched include patterns")

    all_urls: set[str] = set()
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        all_urls.update(extract_urls(text))

    replacements: dict[str, str] = {}
    replaced_candidates: list[Candidate] = []
    skipped_candidates: list[str] = []

    for url in sorted(all_urls):
        candidate = build_canonical_url(url)
        if not candidate:
            continue
        if candidate.original == candidate.canonical:
            continue
        if candidate.canonical in replacements.values():
            replacements[candidate.original] = candidate.canonical
            replaced_candidates.append(candidate)
            continue
        if check_url_exists(candidate.canonical, timeout=args.timeout_seconds):
            replacements[candidate.original] = candidate.canonical
            replaced_candidates.append(candidate)
        else:
            skipped_candidates.append(f"{candidate.original} (canonical unresolved: {candidate.canonical})")

    changed_files: list[Path] = []
    for file_path in files:
        original = file_path.read_text(encoding="utf-8", errors="replace")
        updated = replace_urls_in_text(original, replacements)
        if updated != original:
            file_path.write_text(updated, encoding="utf-8")
            changed_files.append(file_path)

    write_report(Path(args.report), changed_files, replaced_candidates, skipped_candidates)

    print(f"replacements_applied={len(replaced_candidates)}")
    print(f"files_changed={len(changed_files)}")
    print(f"skipped_candidates={len(skipped_candidates)}")


if __name__ == "__main__":
    main()
