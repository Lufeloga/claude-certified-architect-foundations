#!/usr/bin/env python3
"""Statistical audit of the answer key.

Checks the ways a multiple-choice set leaks its answers through structure rather
than content: a favored letter, a predictable pair on multi-answer items, and
length correlating with correctness in either direction.

Usage:  python3 tools/audit_keys.py [practice-set/questions.json]
"""

import json
import pathlib
import statistics
import sys
from collections import Counter

LETTERS = ("A", "B", "C", "D")
PASS, FAIL = "PASS", "FAIL"


def main() -> int:
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "practice-set/questions.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data["items"]
    single = [i for i in items if not i.get("multi_answer")]
    multi = [i for i in items if i.get("multi_answer")]
    results = []

    def check(label, detail, ok):
        results.append((label, detail, PASS if ok else FAIL))

    # B1 letter distribution
    dist = Counter(i["key"][0] for i in single)
    shares = {l: dist[l] / len(single) * 100 for l in LETTERS}
    spread = ", ".join(f"{l} {dist[l]} ({shares[l]:.0f}%)" for l in LETTERS)
    check("B1 letter distribution", spread, all(20 <= shares[l] <= 30 for l in LETTERS))

    # B2 multi-answer pairs all distinct
    pairs = ["+".join(sorted(i["key"])) for i in multi]
    check(
        "B2 multi-answer pairs",
        f"{len(set(pairs))} distinct of {len(pairs)}: {', '.join(sorted(pairs))}",
        len(set(pairs)) == len(pairs),
    )

    # B3/B4 length tells
    longest = sum(1 for i in single if max(LETTERS, key=lambda l: len(i["options"][l])) in i["key"])
    shortest = sum(1 for i in single if min(LETTERS, key=lambda l: len(i["options"][l])) in i["key"])
    check("B3 key is longest option", f"{longest}/{len(single)} = {longest/len(single)*100:.1f}%",
          longest / len(single) <= 0.35)
    check("B4 key is shortest option", f"{shortest}/{len(single)} = {shortest/len(single)*100:.1f}%",
          shortest / len(single) <= 0.35)

    # B5 mean length gap
    correct, wrong = [], []
    for i in items:
        for l in LETTERS:
            (correct if l in i["key"] else wrong).append(len(i["options"][l]))
    gap = statistics.mean(correct) - statistics.mean(wrong)
    check("B5 mean length gap",
          f"key {statistics.mean(correct):.0f} vs distractor {statistics.mean(wrong):.0f} chars, "
          f"gap {gap:+.1f}", abs(gap) <= 3)

    # B7 runs of the same key letter
    run = best = 1
    for prev, cur in zip(single, single[1:]):
        run = run + 1 if cur["key"][0] == prev["key"][0] else 1
        best = max(best, run)
    check("B7 longest run of one letter", f"{best} consecutive", best <= 3)

    # A-series structural checks worth having in the same report
    check("A2 unique consecutive ids",
          f"{len(items)} items", [i["id"] for i in items] == list(range(1, len(items) + 1)))
    check("A4 four options each",
          f"{sum(1 for i in items if len(i['options']) == 4)}/{len(items)}",
          all(len(i["options"]) == 4 for i in items))
    check("A5 key letters exist",
          "all keys reference present options",
          all(all(l in i["options"] for l in i["key"]) for i in items))
    check("A6 multi-answer keys have two letters",
          f"{len(multi)} multi-answer items",
          all(len(i["key"]) == 2 for i in multi))
    check("A10 guide_anchor present",
          f"{sum(1 for i in items if i.get('guide_anchor'))}/{len(items)}",
          all(i.get("guide_anchor") for i in items))
    check("A11 explanation per option",
          f"{sum(1 for i in items if len(i.get('explanations') or {}) == 4)}/{len(items)}",
          all(len(i.get("explanations") or {}) == 4 for i in items))
    check("A13 why line present",
          f"{sum(1 for i in items if i.get('why'))}/{len(items)}",
          all(i.get("why") for i in items))

    width = max(len(r[0]) for r in results)
    print(f"Key audit of {len(items)} items ({len(single)} single, {len(multi)} multi)\n")
    for label, detail, verdict in results:
        print(f"{verdict:<5} {label:<{width}}  {detail}")
    failures = sum(1 for r in results if r[2] == FAIL)
    print(f"\n{len(results) - failures} passed, {failures} failed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
