#!/usr/bin/env python3
"""Prose and consistency checks across the repository, with no dependencies.

This is not a spell checker. The risk in a document set like this is not
misspelled words, it is drift: British spelling in one file and American in the
next, `sub-agent` here and `subagent` there, a stray personal detail, a claim
about the exam that the disclaimer says is not being made.

Usage:  python3 tools/lint_prose.py
Exit code is 1 if any error-level finding is present.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "__pycache__", "patches"}
TEXT_SUFFIXES = {".md", ".html", ".skill", ".cff", ".json"}

# Spelling: one convention, applied everywhere. American is the convention here.
BRITISH = {
    "neighbour": "neighbor", "behaviour": "behavior", "colour": "color",
    "favour": "favor", "licence": "license", "organise": "organize",
    "analyse": "analyze", "recognise": "recognize", "summarise": "summarize",
    "prioritise": "prioritize", "normalise": "normalize", "judgement": "judgment",
    "centre": "center", "catalogue": "catalog", "cancelled": "canceled",
}

# Terminology: the left form is wrong, the right form is the house style.
TERMS = {
    r"\bsub-agents?\b": "subagent",
    r"\bClaude code\b": "Claude Code",
    r"\bclaude\.md\b": "CLAUDE.md",
    r"\bMCP server's\b": "the MCP server's",
    r"\bagent SDK\b": "Agent SDK",
    r"\bstop reason\b": "stop_reason",
    r"\bfew shot\b": "few-shot",
}

# Personal detail must not appear anywhere except the authorship line.
PERSONAL = {
    r"\bgalarza\b": "surname beyond the authorship line",
    r"\bbankinglatam\b": "employer",
    r"@bankinglatam\.com": "personal email",
    r"\bvancouver\b": "location",
    r"\bI passed\b": "personal exam result",
    r"\bscored?\s+\d{3}\b": "personal exam score",
    r"\b(?:19|20)\d{2}-\d{2}-\d{2}\b": "dated personal record",
}

# Claims about how the actual exam behaves. The disclaimer says we make none.
EXAM_CLAIMS = (
    r"the real exam does",
    r"the real thing",
    r"on the actual exam",
    r"the exam also",
    r"as the exam does",
)

QUOTED = re.compile(r'"guide_anchor"\s*:|Exam Guide:|<sub>Exam Guide')
# CC BY 4.0 requires the author to be named. These are the lines where that
# happens, and they are the only place a personal name is allowed to appear.
ATTRIBUTION = re.compile(
    r'CC[- ]BY|Attribution:|family-names|given-names|\\balias\\b|"attribution"\\s*:',
    re.I,
)
DOUBLE_WORD = re.compile(r"\b(\w+)\s+\1\b", re.I)
TRAILING_WS = re.compile(r"[ \t]+$")
EM_DASH = re.compile(r"[—–]")
# The certification's own name carries an en dash. Renaming it would be wrong,
# so it is the single exempted string.
EM_DASH_OK = re.compile(r"Claude Certified Architect – Foundations")
# Words that legitimately repeat, so the double-word check does not cry wolf.
DOUBLE_OK = {"that", "had", "s"}


def files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS or part.startswith("_") for part in path.parts):
            continue
        yield path


def main() -> int:
    errors, warnings = [], []

    for path in files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            low = line.lower()
            where = f"{rel}:{n}"

            for british, american in BRITISH.items():
                if re.search(rf"\b{british}", low):
                    errors.append(f"{where}  British spelling '{british}' -> '{american}'")

            # Quotations from the official guide are reproduced exactly. House
            # style does not get applied to someone else's words.
            quoted = QUOTED.search(line) is not None
            for pattern, want in ({} if quoted else TERMS).items():
                if re.search(pattern, line):
                    match = re.search(pattern, line).group(0)
                    warnings.append(f"{where}  '{match}' -> '{want}'")

            attributing = ATTRIBUTION.search(line) is not None
            for pattern, what in ({} if attributing else PERSONAL).items():
                if re.search(pattern, low):
                    errors.append(f"{where}  personal detail: {what}")

            for pattern in EXAM_CLAIMS:
                if re.search(pattern, low):
                    errors.append(f"{where}  claim about the actual exam: '{pattern}'")

            if EM_DASH.search(EM_DASH_OK.sub("", line)):
                warnings.append(f"{where}  em or en dash; use a comma, colon, or period")

            # CSS shorthand repeats values legitimately, so structural checks
            # run on prose files only.
            if path.suffix in {".md", ".skill"}:
                m = DOUBLE_WORD.search(line)
                if m and m.group(1).lower() not in DOUBLE_OK:
                    warnings.append(f"{where}  doubled word '{m.group(1)}'")

            if TRAILING_WS.search(line):
                warnings.append(f"{where}  trailing whitespace")

            if ("  " in line.strip() and not in_fence
                    and not line.lstrip().startswith(("|", "-", "#"))):
                if path.suffix == ".md":
                    warnings.append(f"{where}  double space inside a sentence")

    for w in warnings:
        print(f"warn   {w}")
    for e in errors:
        print(f"ERROR  {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
