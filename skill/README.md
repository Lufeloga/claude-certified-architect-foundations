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

**It tells you the time budget and leaves the clock to you.** The full set is
written for 120 minutes, about two minutes an item. The runner cannot measure
elapsed time between turns, so it does not pretend to.

**It reports what the sample can support.** A run under 25 items gets no
percentages at all: just the count, the misses, and which frame they cluster
in. Ten items across five domains give two items each, and a percentage
computed from two items is noise wearing a number. From 25 items up, you get the
per-domain breakdown weighted to the published blueprint.

**It does not report a scaled score or a pass/fail verdict.** The scale belongs
to the certification, and a number from a practice set that looks like an
official one invites a false conclusion in either direction. The domain
breakdown is the part that tells you what to do next.

**It routes you somewhere.** Either way it names exactly one frame in the
[Frame Map](../frame-map/) to read next: on a short run the frame your misses
cluster in, on a long one the frame covering your weakest domain.

## How it reads the set

The skill reads [`practice-set/questions.json`](../practice-set/questions.json),
which is the source of truth for every format in this repository. Edit that file
and the skill picks up the change with no rebuild.

## If you edit the skill

Three things this runner promised at some point and could not deliver. Each was
invisible when reading the file and obvious within minutes of running it, so
run it after any edit rather than reviewing it.

**A skill is a directory, not a file.** It has to be
`.claude/skills/<name>/SKILL.md`, and the slash command comes from the directory
name. A single `.skill` file is loaded by nothing, silently.

**Declare every tool the runner needs.** It needs to read one file and ask
questions. Leave the question tool out and the model reaches for the shell to
present each item, which puts a permission prompt between the user and every
question. A sitting interrupted on every item is not a sitting.

**Do not ask it for a number the runtime cannot produce.** There is no clock
between turns, so a report template with a duration field invites a fabricated
one. The same applies to a percentage computed from two items: the template
should not have a slot that the sample cannot fill honestly.
