#!/usr/bin/env python3
"""Generate every published format from questions.json.

questions.json is the only editable copy. questions.md, answers.md, and
practice-set.html are outputs, and editing them by hand is a mistake that the
next build silently reverts. Output is deterministic: running twice produces
byte-identical files, which is what test F1 checks.

Questions and answers are written to separate files on purpose. The set is meant
to be sat cold, and a single document that scrolls from an item to its key is
not a set anyone can sit honestly.

Usage:  python3 tools/build.py
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SET_DIR = ROOT / "practice-set"
QUESTIONS = SET_DIR / "questions.json"
LETTERS = ("A", "B", "C", "D")

DOMAIN_NAMES = {
    "D1": "Agentic Architecture & Orchestration",
    "D2": "Tool Design & MCP Integration",
    "D3": "Claude Code Configuration & Workflows",
    "D4": "Prompt Engineering & Structured Output",
    "D5": "Context Management & Reliability",
}

DISCLAIMER = (
    "Independent study material. Not affiliated with, endorsed by, or reviewed by "
    "Anthropic. It reproduces no exam content: every item was written from the "
    "publicly published task statements in the official Exam Guide."
)


def esc(text: str) -> str:
    """Markdown and HTML share a source string, so escape per target."""
    return html.escape(text, quote=False)


def md_code(text: str) -> str:
    return text


def html_code(text: str) -> str:
    """Turn `backticked` spans into <code>, escaping everything else."""
    out, last = [], 0
    for m in re.finditer(r"`([^`]+)`", text):
        out.append(esc(text[last:m.start()]))
        out.append(f"<code>{esc(m.group(1))}</code>")
        last = m.end()
    out.append(esc(text[last:]))
    return "".join(out)


def scenario_blocks(items):
    """Group items by scenario, preserving item order."""
    blocks, current = [], None
    for item in items:
        if current is None or item["scenario"] != current[0]:
            current = (item["scenario"], item["scenario_intro"], [])
            blocks.append(current)
        current[2].append(item)
    return blocks


def build_questions_md(data) -> str:
    lines = [
        "# Practice Set: Questions",
        "",
        f"{len(data['items'])} items. Answers and explanations are in "
        "[answers.md](answers.md), deliberately in a separate file so the set can be "
        "sat cold.",
        "",
        f"> {DISCLAIMER}",
        "",
        "---",
        "",
    ]
    for scenario, intro, items in scenario_blocks(data["items"]):
        lines += [f"## {scenario}", "", intro, ""]
        for item in items:
            heading = f"### {item['id']}."
            if item.get("select_instruction"):
                heading += f" _{item['select_instruction']}_"
            lines += [heading, "", md_code(item["stem"]), ""]
            for letter in LETTERS:
                lines.append(f"- **{letter}.** {md_code(item['options'][letter])}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_answers_md(data) -> str:
    lines = [
        "# Practice Set: Answers and Explanations",
        "",
        "Score by domain rather than by total. Every option carries an explanation, "
        "because the reason a plausible option fails is the part worth learning.",
        "",
        f"> {DISCLAIMER}",
        "",
        "---",
        "",
    ]
    for item in data["items"]:
        key = ", ".join(item["key"])
        label = "Correct answers" if item["multi_answer"] else "Correct answer"
        lines += [
            f"### {item['id']}. {label}: {key}",
            "",
            f"`{item['domain']} · Task {item['task']}`",
            "",
        ]
        for letter in LETTERS:
            mark = "**✓**" if letter in item["key"] else "✗"
            lines.append(f"- {mark} **{letter}.** {md_code(item['explanations'][letter])}")
        lines += ["", f"**Why:** {md_code(item['why'])}", ""]
        anchor = item.get("guide_anchor")
        if anchor:
            lines += [f"<sub>Exam Guide: {md_code(anchor)}</sub>", ""]
    return "\n".join(lines).rstrip() + "\n"


HTML_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CCAR-F Practice Set</title>
<style>
  :root {
    color-scheme: light dark;
    --paper: #E9E6DD; --sheet: #F7F5F0; --ink: #1C2024;
    --ink-soft: #575E66; --ink-faint: #8B9199; --line: #DEDACF;
    --accent: #135E58; --accent-wash: #E1EDEB;
    --mono: "SFMono-Regular", ui-monospace, Menlo, Consolas, monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --paper: #101317; --sheet: #181C21; --ink: #E8E6E1;
      --ink-soft: #A5ABB3; --ink-faint: #757C85; --line: #2C323A;
      --accent: #4FB3A7; --accent-wash: #13302D;
    }
  }
  :root[data-theme="dark"] {
    --paper: #101317; --sheet: #181C21; --ink: #E8E6E1;
    --ink-soft: #A5ABB3; --ink-faint: #757C85; --line: #2C323A;
    --accent: #4FB3A7; --accent-wash: #13302D;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--paper); color: var(--ink);
    font-family: var(--sans); line-height: 1.55;
  }
  .doc {
    max-width: 7.6in; margin: 0 auto; background: var(--sheet);
    border-left: 1px solid var(--line); border-right: 1px solid var(--line);
    padding: clamp(1.4rem, 4vw, 2.6rem) clamp(1.1rem, 4vw, 2.2rem) 3rem;
  }
  h1 { font-family: var(--mono); font-size: 1.9rem; letter-spacing: -.02em; margin: 0 0 .6rem; }
  h2 {
    font-family: var(--mono); font-size: 1.05rem; margin: 2.4rem 0 .4rem;
    padding-top: .8rem; border-top: 2px solid var(--accent); color: var(--accent);
  }
  h3 { font-size: .95rem; margin: 1.6rem 0 .5rem; }
  code { font-family: var(--mono); font-size: .86em; background: var(--accent-wash); padding: .1em .3em; border-radius: 3px; }
  .lede { color: var(--ink-soft); }
  .note { color: var(--ink-faint); font-size: .82rem; border-left: 2px solid var(--line); padding-left: .8rem; }
  .pick { font-family: var(--mono); font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; color: var(--accent); }
  ol.opts { list-style: none; padding-left: 0; margin: .5rem 0 0; }
  ol.opts li { margin: .32rem 0; padding-left: 1.9rem; text-indent: -1.9rem; }
  .ltr { font-family: var(--mono); font-weight: 600; }
  .q, .ans { break-inside: avoid; page-break-inside: avoid; }
  .meta { font-family: var(--mono); font-size: .72rem; color: var(--ink-faint); }
  .why { border-left: 2px solid var(--accent); padding-left: .8rem; margin-top: .6rem; }
  .anchor { font-size: .74rem; color: var(--ink-faint); }
  @page { size: 8.5in 11in; margin: 0.62in 0.7in; }
  @media print {
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body { background: #fff; }
    .doc { max-width: none; border: 0; padding: 0; background: #fff; }
  }
</style>
</head>
<body>
<div class="doc">
"""


def build_html(data) -> str:
    out = [HTML_HEAD]
    out.append("<h1>CCAR-F Practice Set</h1>")
    out.append(
        f'<p class="lede">{len(data["items"])} items across the six scenarios in the '
        "published exam blueprint, with answers and explanations at the end.</p>"
    )
    out.append(f'<p class="note">{esc(DISCLAIMER)}</p>')

    out.append("<h2>Part 1 &middot; Questions</h2>")
    for scenario, intro, items in scenario_blocks(data["items"]):
        out.append(f"<h3>Scenario: {esc(scenario)}</h3>")
        out.append(f'<p class="lede">{html_code(intro)}</p>')
        for item in items:
            out.append('<div class="q">')
            if item.get("select_instruction"):
                out.append(f'<p class="pick">{esc(item["select_instruction"])}</p>')
            out.append(f"<p><b>{item['id']}.</b> {html_code(item['stem'])}</p>")
            out.append('<ol class="opts">')
            for letter in LETTERS:
                out.append(
                    f'<li><span class="ltr">{letter}.</span> '
                    f"{html_code(item['options'][letter])}</li>"
                )
            out.append("</ol></div>")

    out.append("<h2>Part 2 &middot; Answers and Explanations</h2>")
    for item in data["items"]:
        label = "Correct answers" if item["multi_answer"] else "Correct answer"
        out.append('<div class="ans">')
        out.append(
            f"<p><b>{item['id']}. {label}: {', '.join(item['key'])}</b> "
            f'<span class="meta">{item["domain"]} &middot; Task {item["task"]}</span></p>'
        )
        out.append('<ol class="opts">')
        for letter in LETTERS:
            mark = "&check;" if letter in item["key"] else "&times;"
            out.append(
                f'<li><span class="ltr">{mark} {letter}.</span> '
                f"{html_code(item['explanations'][letter])}</li>"
            )
        out.append("</ol>")
        out.append(f'<p class="why"><b>Why:</b> {html_code(item["why"])}</p>')
        if item.get("guide_anchor"):
            out.append(
                f'<p class="anchor">Exam Guide: {html_code(item["guide_anchor"])}</p>'
            )
        out.append("</div>")

    out.append("</div></body></html>")
    return "\n".join(out) + "\n"


def main() -> int:
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = {
        SET_DIR / "questions.md": build_questions_md(data),
        SET_DIR / "answers.md": build_answers_md(data),
        SET_DIR / "practice-set.html": build_html(data),
    }
    for path, content in targets.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}  ({len(content):,} bytes)")

    counts = {}
    for item in data["items"]:
        counts[item["domain"]] = counts.get(item["domain"], 0) + 1
    total = len(data["items"])
    print("\ncoverage by domain")
    for domain in sorted(counts, key=lambda d: -counts[d]):
        share = counts[domain] / total * 100
        print(f"  {domain} {DOMAIN_NAMES[domain]:<42} {counts[domain]:>3} ({share:.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
