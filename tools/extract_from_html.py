#!/usr/bin/env python3
"""One-shot importer: recovered practice-set HTML -> questions.json.

This runs once to seed the JSON source of truth. After that, questions.json is
the only editable copy and every other format is generated from it by build.py.
"""

import html
import json
import pathlib
import re
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_recovered-practice-set.html")
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "practice-set/questions.json")

TAG = re.compile(r"<[^>]+>")


def text(fragment: str) -> str:
    """Strip markup but keep `code` spans as backticked text."""
    fragment = re.sub(r"<code>(.*?)</code>", r"`\1`", fragment, flags=re.S)
    fragment = re.sub(r"<em>(.*?)</em>", r"\1", fragment, flags=re.S)
    fragment = re.sub(r"<b>(.*?)</b>", r"\1", fragment, flags=re.S)
    fragment = TAG.sub("", fragment)
    return " ".join(html.unescape(fragment).split())


def main() -> int:
    src = SRC.read_text(encoding="utf-8")
    part1, _, part2 = src.partition("Part 2 &middot; Answers")
    if not part2:
        print("could not split Part 1 from Part 2", file=sys.stderr)
        return 1

    # Scenario headings carry the shared intro paragraph that precedes their items.
    scenarios = []
    for m in re.finditer(
        r'<h3 class="scen">Scenario:\s*(.*?)</h3>\s*<p class="lede"[^>]*>(.*?)</p>',
        part1,
        flags=re.S,
    ):
        scenarios.append((m.start(), text(m.group(1)), text(m.group(2))))

    def scenario_at(pos: int):
        current = ("", "")
        for start, name, intro in scenarios:
            if start < pos:
                current = (name, intro)
        return current

    items = {}
    for m in re.finditer(
        r'<div class="q">(?:<span class="pick">(.*?)</span>)?'
        r'<p><span class="num">Question (\d+)\.</span>(.*?)</p>\s*'
        r'<ul class="opts">(.*?)</ul></div>',
        part1,
        flags=re.S,
    ):
        pick = text(m.group(1)) if m.group(1) else ""
        num = int(m.group(2))
        stem = text(m.group(3))
        options = {}
        for om in re.finditer(
            r'<li><span class="ltr">([A-D])\.</span>(.*?)</li>', m.group(4), flags=re.S
        ):
            options[om.group(1)] = text(om.group(2))
        scenario, intro = scenario_at(m.start())
        items[num] = {
            "id": num,
            "scenario": scenario,
            "scenario_intro": intro,
            "domain": None,
            "task": None,
            "guide_anchor": None,
            "select_instruction": pick,
            "stem": stem,
            "options": options,
            "key": [],
            "multi_answer": False,
            "negative": False,
            "explanations": {},
            "distractor_families": {},
            "why": None,
            "revision": 1,
        }

    for m in re.finditer(
        r'<div class="ans"><p class="hd">Question (\d+)\.\s*<em>Correct Answers?:\s*'
        r"(.*?)\.?</em></p><p>(.*?)</p></div>",
        part2,
        flags=re.S,
    ):
        num = int(m.group(1))
        raw_key = text(m.group(2))
        letters = re.findall(r"\b([A-D])\b", raw_key)
        if num not in items:
            print(f"answer for unknown question {num}", file=sys.stderr)
            continue
        items[num]["key"] = letters
        items[num]["multi_answer"] = len(letters) > 1
        items[num]["rationale_legacy"] = text(m.group(3))

    missing_opts = [n for n, it in items.items() if len(it["options"]) != 4]
    missing_key = [n for n, it in items.items() if not it["key"]]

    payload = {
        "set_version": "0.1.0-draft",
        "license": "CC-BY-4.0",
        "item_count": len(items),
        "items": [items[n] for n in sorted(items)],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"items extracted : {len(items)}")
    print(f"with 4 options  : {len(items) - len(missing_opts)}")
    print(f"with a key      : {len(items) - len(missing_key)}")
    if missing_opts:
        print(f"  !! option count wrong: {missing_opts}")
    if missing_key:
        print(f"  !! no key found: {missing_key}")
    multi = [n for n, it in items.items() if it["multi_answer"]]
    print(f"multi-answer    : {len(multi)} -> {multi}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
