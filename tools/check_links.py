#!/usr/bin/env python3
"""Check that every link in the repository resolves.

A study guide that sends readers to a 404 loses their trust for the whole
document, and the official Exam Guide link is the one a careful reader clicks
first. Relative links are checked against the filesystem; external ones are
requested over the network.

Usage:  python3 tools/check_links.py [--offline]
        --offline skips the network and checks relative links only.
"""

import pathlib
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TIMEOUT = 15
# A browser-ish agent, because some hosts refuse the default urllib one.
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; link-check/1.0)"}


def markdown_files():
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


CURL = shutil.which("curl")


def check_with_curl(url: str) -> tuple[bool, str]:
    """Preferred path: curl carries the system trust store.

    Python on macOS frequently ships without root certificates installed, which
    makes every HTTPS check fail with a verification error that looks exactly
    like a dead link. Using curl when it is present avoids reporting a false
    404 because of a local certificate problem.
    """
    result = subprocess.run(
        [CURL, "-sL", "-o", "/dev/null", "-w", "%{http_code}",
         "--max-time", str(TIMEOUT), "-A", HEADERS["User-Agent"], url],
        capture_output=True, text=True,
    )
    code = result.stdout.strip()
    return code.isdigit() and int(code) < 400, code or "no response"


def check_external(url: str) -> tuple[bool, str]:
    if CURL:
        return check_with_curl(url)
    request = urllib.request.Request(url, headers=HEADERS, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status < 400, str(response.status)
    except urllib.error.HTTPError as exc:
        # Some hosts reject HEAD but serve GET.
        if exc.code in (403, 405):
            try:
                get = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(get, timeout=TIMEOUT) as response:
                    return response.status < 400, f"{response.status} (GET)"
            except Exception as inner:  # noqa: BLE001
                return False, f"{exc.code} then {type(inner).__name__}"
        return False, str(exc.code)
    except Exception as exc:  # noqa: BLE001
        return False, type(exc).__name__


def main() -> int:
    offline = "--offline" in sys.argv
    seen: dict[str, tuple[bool, str]] = {}
    failures = []
    checked = 0

    for path in markdown_files():
        rel = path.relative_to(ROOT)
        for match in LINK.finditer(path.read_text(encoding="utf-8")):
            target = match.group(2)
            where = f"{rel}"

            if target.startswith("#") or target.startswith("mailto:"):
                continue

            if target.startswith(("http://", "https://")):
                if offline:
                    continue
                if target not in seen:
                    seen[target] = check_external(target)
                ok, detail = seen[target]
                checked += 1
                if not ok:
                    failures.append(f"{where}  {target}  [{detail}]")
                continue

            resolved = (path.parent / target.split("#")[0]).resolve()
            checked += 1
            if not resolved.exists():
                failures.append(f"{where}  {target}  [missing file]")

    for failure in failures:
        print(f"BROKEN  {failure}")
    scope = "relative links only" if offline else "relative and external links"
    how = "curl" if CURL and not offline else "urllib" if not offline else "filesystem"
    print(f"\n{checked} links checked ({scope}, via {how}), {len(failures)} broken")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
