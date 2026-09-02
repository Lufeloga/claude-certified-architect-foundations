#!/usr/bin/env python3
"""Answer the set without understanding it.

A question bank is only a diagnostic if reading the question is the cheapest way
to answer it. This script attacks the set the way a test-wise candidate would:
no domain knowledge, no reasoning about the scenario, just surface features of
the options. Every strategy below is a shortcut real candidates actually use.

If any strategy beats chance by a meaningful margin, the set leaks its answers
and the items that leak need rewriting. Chance is 25% on a four-option item.

Several strategies abstain when the surface feature they look for is absent or
tied, so they judge only part of the set. A strategy that fires on a handful of
items carries no evidence either way: one lucky hit out of two reads as 50% and
means nothing. Those are reported as INSUFFICIENT rather than scored, and the
attempt count is printed so the reader can see which verdicts rest on what.

Usage:  python3 tools/heuristic_solver.py [practice-set/questions.json]
"""

import json
import pathlib
import re
import sys
from collections import Counter

LETTERS = ("A", "B", "C", "D")

CHANCE = 25.0
THRESHOLD = 35.0
# Below this many attempts a hit rate is noise, so no verdict is issued.
MIN_ATTEMPTS = 10

# Words that make an option sound safely qualified, and words that make it sound
# absolute. Item writers tend to hedge the key and overstate the distractors.
HEDGES = (
    "typically", "generally", "usually", "often", "may", "can", "tends",
    "in most", "where", "when the", "unless", "rather than", "before",
)
ABSOLUTES = (
    "always", "never", "every", "all ", "any ", "none", "only", "guarantees",
    "eliminates", "ensures", "prevents", "cannot", "must ", "impossible",
)

STOPWORDS = frozenset("""
a an and are as at be been but by for from has have if in into is it its of on
or that the their then there these this to was were what when which while with
you your not no does do can could should would will shall may might must
""".split())


def tokens(s: str) -> set:
    return {w for w in re.findall(r"[a-z_]+", s.lower()) if w not in STOPWORDS and len(w) > 2}


def count_any(text: str, needles) -> int:
    low = text.lower()
    return sum(low.count(n) for n in needles)


# Each strategy returns the letter it would pick, or None to abstain.

def pick_longest(opts, stem):
    return max(LETTERS, key=lambda l: len(opts[l]))


def pick_shortest(opts, stem):
    return min(LETTERS, key=lambda l: len(opts[l]))


def pick_stem_overlap(opts, stem):
    st = tokens(stem)
    scored = {l: len(tokens(opts[l]) & st) for l in LETTERS}
    best = max(scored.values())
    if best == 0 or list(scored.values()).count(best) > 1:
        return None
    return max(scored, key=scored.get)


def pick_most_hedged(opts, stem):
    scored = {l: count_any(opts[l], HEDGES) for l in LETTERS}
    best = max(scored.values())
    if best == 0 or list(scored.values()).count(best) > 1:
        return None
    return max(scored, key=scored.get)


def pick_fewest_absolutes(opts, stem):
    scored = {l: count_any(opts[l], ABSOLUTES) for l in LETTERS}
    if len(set(scored.values())) == 1:
        return None
    low = min(scored.values())
    if list(scored.values()).count(low) > 1:
        return None
    return min(scored, key=scored.get)


def pick_most_technical(opts, stem):
    """Options naming concrete artifacts read as more informed."""
    scored = {l: opts[l].count("`") for l in LETTERS}
    best = max(scored.values())
    if best == 0 or list(scored.values()).count(best) > 1:
        return None
    return max(scored, key=scored.get)


STRATEGIES = {
    "longest option": pick_longest,
    "shortest option": pick_shortest,
    "most stem overlap": pick_stem_overlap,
    "most hedged wording": pick_most_hedged,
    "fewest absolutes": pick_fewest_absolutes,
    "most technical tokens": pick_most_technical,
}


def combined(opts, stem):
    """What a real test-wise candidate does: let the strategies vote."""
    votes = Counter()
    for fn in STRATEGIES.values():
        pick = fn(opts, stem)
        if pick:
            votes[pick] += 1
    if not votes:
        return None
    top = votes.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None
    return top[0][0]


def main() -> int:
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "practice-set/questions.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    # Multi-answer items are scored separately; these strategies pick one letter.
    items = [i for i in data["items"] if not i.get("multi_answer")]

    rows = []
    for name, fn in list(STRATEGIES.items()) + [("COMBINED VOTE", combined)]:
        hits = attempts = 0
        leaked = []
        for it in items:
            pick = fn(it["options"], it["stem"])
            if pick is None:
                continue
            attempts += 1
            if pick in it["key"]:
                hits += 1
                leaked.append(it["id"])
        rate = hits / attempts * 100 if attempts else 0.0
        rows.append((name, hits, attempts, rate, leaked))

    print(f"Blind heuristic attack on {len(items)} single-answer items")
    print(f"Chance = {CHANCE}%   Threshold = {THRESHOLD}%   "
          f"Minimum attempts for a verdict = {MIN_ATTEMPTS}\n")
    print(f"{'strategy':<24}{'hits':>6}{'tried':>7}{'rate':>9}   verdict")
    print("-" * 66)
    worst = 0.0
    for name, hits, attempts, rate, _ in rows:
        if attempts < MIN_ATTEMPTS:
            verdict = "INSUFFICIENT"
        elif rate <= THRESHOLD:
            verdict = "PASS"
            worst = max(worst, rate)
        else:
            verdict = "LEAK"
            worst = max(worst, rate)
        print(f"{name:<24}{hits:>6}{attempts:>7}{rate:>8.1f}%   {verdict}")

    # Items that fall to two or more independent shortcuts are the ones to rewrite.
    leak_count = Counter()
    for name, _, _, _, leaked in rows:
        if name == "COMBINED VOTE":
            continue
        for i in leaked:
            leak_count[i] += 1
    repeat = sorted(i for i, c in leak_count.items() if c >= 2)
    print(f"\nItems solved by 2+ independent shortcuts: {len(repeat)}")
    if repeat:
        print(f"  {repeat}")

    print(f"\nWorst scored strategy: {worst:.1f}%  ->  "
          f"{'PASS' if worst <= THRESHOLD else 'FAIL'}")
    return 0 if worst <= THRESHOLD else 1


if __name__ == "__main__":
    raise SystemExit(main())
