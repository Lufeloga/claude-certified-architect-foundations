# Practice Set

Sixty original items across the six scenarios named in the published exam
blueprint, with an explanation for every option.

- **[questions.md](questions.md)**. The items, with no answers
- **[answers.md](answers.md)**. The key, an explanation per option, and the guide reference
- **[questions.json](questions.json)**. The source of truth, and what the skill reads
- **[practice-set.pdf](practice-set.pdf)**. The whole thing as a printable handout

> Independent study material. Not affiliated with, endorsed by, or reviewed by
> Anthropic. It reproduces no exam content: every item was written from the
> publicly published task statements in the official
> [Exam Guide](https://www.anthropic.com/learn/certification).

## How to use it

**Sit it cold, on a timer, before you read anything else.** Answer with letters
only and look nothing up. A set you work through with the guide open measures
recognition, and recognition is not what you need on the day.

Questions and answers live in separate files for exactly this reason.

Then read [answers.md](answers.md) in full, including the items you got right.
Each option carries its own explanation, and the reason a plausible option fails
is usually the part worth keeping.

Finally, take your weakest domain to the [Frame Map](../frame-map/) and read the
frame that covers it.

## Scoring

**Score by domain, not by total.** A total tells you how you did; a domain
breakdown tells you what to study. The item counts here follow the weights the
blueprint publishes, so a domain percentage is comparable across sittings.

| Domain | Weight | Items |
|---|---|---|
| D1 · Agentic Architecture & Orchestration | 27% | 16 |
| D3 · Claude Code Configuration & Workflows | 20% | 12 |
| D4 · Prompt Engineering & Structured Output | 20% | 12 |
| D2 · Tool Design & MCP Integration | 18% | 11 |
| D5 · Context Management & Reliability | 15% | 9 |

[scoring.md](scoring.md) is a sheet you can print alongside the questions.

The `skill/` directory has a Claude Code skill that runs the set on a timer and
does this arithmetic for you.

## What is in the set

**Six items ask for two answers**, and they say so above the question.

**Five items ask which option is weakest, least appropriate, or false.** They
are not marked, so read every stem to the end. These are here as reasoning
practice: evaluating four statements independently is a different skill from
picking the best one, and it is worth rehearsing on its own terms. The published
guide describes the exam as multiple-choice and multiple-response, and nothing
here should be read as a claim about which formats appear on it.

**Some items name a flag or a file that does not exist.** A confident-sounding
artifact that is not real is one of the more useful things to be able to spot,
so it appears here as a distractor. No item is keyed to one.

**Every item is anchored.** Each entry in `answers.md` cites the specific
*Knowledge of* or *Skills in* line from the published guide that supports its
key. If you disagree with an answer, that line is where the argument should
start.

## A note on difficulty

The four options are written to be defensible. Roughly a third of the items have
two options that a reasonable architect could argue for, where one is better for
a reason stated in the explanation.

This is measurable rather than a claim: [QUALITY.md](../QUALITY.md) reports what
happens when the set is attacked by a program that answers using only surface
features of the options, with no understanding at all. Reading the question
should be the cheapest way to answer it, and the numbers say whether it is.

## Found a wrong answer?

Likely, in sixty items. Open an issue with the item number, the answer you
believe is correct, and the line of the official guide that supports it. See
[CONTRIBUTING.md](../CONTRIBUTING.md).
