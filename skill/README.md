# Practice runner skill

A Claude Code skill that runs the practice set cold and on a timer, scores by
domain, and points you at the frame covering your weakest one.

## Install

Nothing to install. The skill ships at
[`.claude/skills/ccar-f-practice/SKILL.md`](../.claude/skills/ccar-f-practice/SKILL.md),
so opening Claude Code inside your clone finds it:

```bash
git clone https://github.com/Lufeloga/claude-certified-architect-foundations.git
cd claude-certified-architect-foundations
claude
```

To have it everywhere instead, copy the whole `ccar-f-practice/` folder into
`~/.claude/skills/`. The skill
reads the item bank from this repository, so a global install means running it
from inside your clone, or giving it the path when it asks.

## Run

```
/ccar-f-practice        # 20 items
/ccar-f-practice 10     # a short sitting
/ccar-f-practice 60     # the full set
```

Pass a number and it starts immediately with sensible defaults: all domains,
feedback at the end. Run it bare and it asks those three things once, then runs
without interrupting you again.

## No prompts mid-sitting

The runner uses two tools only: it reads the item bank once, then presents every
item as a question. It runs no shell commands and writes no files, so a sitting
never stops to ask your permission for anything. That is a design constraint,
not an accident: a timed run interrupted on every item is not a timed run.

## What it does

**No feedback until the end, by default.** Immediate feedback teaches you the
item. A cold run tells you whether the reasoning transfers, which is the thing
worth knowing. The coaching mode is there when you want it, but it is not the
default.

**It times you.** The full set is written for 120 minutes.

**It scores by domain**, weighted to the published blueprint, and stays quiet
about any domain with fewer than five items answered rather than reporting a
percentage that will be over-read.

**It does not report a scaled score or a pass/fail verdict.** The scale belongs
to the certification, and a number from a practice set that looks like an
official one invites a false conclusion in either direction. The domain
breakdown is the part that tells you what to do next.

**It routes you somewhere.** Your weakest domain maps to a frame in the
[Frame Map](../frame-map/), and it names which one to read.

## How it reads the set

The skill reads [`practice-set/questions.json`](../practice-set/questions.json),
which is the source of truth for every format in this repository. Edit that file
and the skill picks up the change with no rebuild.
