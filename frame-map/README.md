# Frame Map

A decision framework for the Claude Certified Architect – Foundations exam.

Its questions drop you into a concrete situation, sometimes a system
misbehaving, sometimes a design choice where no option is obviously wrong, and
ask for the best decision. This map turns that into three moves: read the
situation, open the frame it belongs to, apply its reflex.

It complements the official [Exam Guide](https://www.anthropic.com/learn/certification).
It does not replace it. The guide tells you what is examinable; this tells you
how to decide once you are looking at four defensible options.

> Independent study material. Not affiliated with, endorsed by, or reviewed by
> Anthropic. It reproduces no exam content. **The frame and lens names below are
> study scaffolding invented for this map, not official terminology.**

**[frame-map.pdf](frame-map.pdf) is the same content as a five-page printable
handout.** The print version encodes moves and traps visually; this page uses
labeled columns instead.

---

## The method

| | Move | Question | Output |
|---|---|---|---|
| **1** | Diagnose | What kind of problem is this, really? | a type |
| **2** | Open the frame | One of seven. The frame is the toolbox. | a reflex |
| **3** | Apply and confirm | Check the answer against the buried constraint. | a decision |

Read the whole scenario before the options. The clause that decides the answer
is usually buried mid-paragraph, not in the last line.

Run the moves in order. Never pick a frame before reading the case.

---

## Move 1 · The router

Classify before you medicate. The wording on the left is what a scenario tends
to say. A question can span two frames, in which case split it and treat each
part separately.

| The scenario says | Go to |
|---|---|
| inconsistent output · wrong format · invents values · can't guarantee a step · mishandles failures | **1 · Output Reliability** |
| find · trace · locate · which exploration strategy · next step to understand this code | **2 · Codebase Navigation** |
| coordinator · subagents · how information flows · decompose · parallel or sequential | **3 · Orchestration** |
| approaching the context limit · long session degrades · cached results are stale · resume or fork | **4 · Context & State** |
| where should this live · who should see it · CLAUDE.md, rules, skills, commands, settings | **5 · Configuration Placement** |
| the customer asks for a person · outside documented authority · irreversible action | **6 · Human Escalation** |
| balances cost and latency · plan or direct · sync or batch · automate or keep review | **7 · Execution Mode** |

Do not let the decorative technology intimidate you. Strip the jargon and ask
what decision sits underneath. It is almost always one of the seven.

---

## Move 2 · The seven frames

Each frame is a type of decision, never a technology. The reflexes are defaults:
a constraint buried in the scenario can overturn any of them.

### 1 · Output Reliability

*The output cannot be trusted. What actually fixes it?*

| When | Move |
|---|---|
| A tool exists and nobody calls it | Expand its description |
| Two tools get confused for each other | Rename both, update both |
| One tool, output shape varies | Split it into typed tools |
| Descriptions are fine and it still misroutes | Check the system prompt |
| `must` · `never` · before X runs | A deterministic mechanism, not prose |
| Retries what cannot succeed | Structured error metadata |

### 2 · Codebase Navigation

*How do I explore code I do not know yet?*

| When | Move |
|---|---|
| Searching contents | Grep |
| Searching names or paths | Glob |
| Building understanding | Entry points first, then follow imports |
| Wrappers re-export under new names | List every exported name first |
| `Edit` fails on a non-unique match | Read, modify, Write |
| It does not fit the window | Scoped subagents returning compact reports |

### 3 · Orchestration

*Several agents. How does information flow?*

| When | Move |
|---|---|
| Any inter-agent communication | Everything routes through the coordinator |
| A subagent needs a constraint | Put it in that subagent's own prompt |
| Delegating work | Delegate goals and quality criteria, not procedure |
| Parallel work | Several delegations in one response, not across turns |
| Gaps after synthesis | Assess coverage, re-delegate, re-synthesize |

### 4 · Context & State

*What lives in the window, and what must survive it?*

| When | Move |
|---|---|
| Near the limit | Manage what is in it. Restarting with nothing carried over always loses |
| Bloated tool output | Prune fields, keep exact values |
| Long multi-topic conversation | Summarize what is resolved, keep the live thread verbatim |
| Cached results are stale | Fresh session seeded with a summary, then refetch |

### 5 · Configuration Placement

*Where does this instruction live, and who sees it?*

| When | Move |
|---|---|
| Tied to a path | `.claude/rules/`, with a glob in the frontmatter |
| A procedure with steps | A skill, loaded on demand |
| A universal standard | `CLAUDE.md`, always loaded |
| Invoked by hand | A slash command in `.claude/commands/` |
| A hard guarantee | A hook, never a prompt |

Second axis: the project directory is the team, the home directory is you alone.

### 6 · Human Escalation

*When does a person take over?*

| When | Move |
|---|---|
| They asked for a person | Honor it immediately, no investigation first |
| Frustrated, has not asked, within your capability | Acknowledge and offer to resolve; escalate if they insist |
| Policy is silent or ambiguous on what they want | Escalate |
| Several possible matches | Ask for an identifier, do not guess |
| The handoff itself | A package: who, root cause, amount, recommended action |
| **Never** | Sentiment or self-reported confidence as the trigger |

### 7 · Execution Mode

*Nothing is broken. In what mode do I run this?*

| When | Move |
|---|---|
| Multi-file, architectural, or several valid approaches | Plan first |
| A clear single-file fix | Go direct |
| Blocking, or needs tools mid-request | Synchronous |
| Overnight and latency-tolerant | Batch |
| Reviewing work | An independent instance, not the one that produced it |

---

## Move 3 · The three lenses

The frame gives you the toolbox. These three questions run on top of every
frame, and they are what stop a good reflex from being applied in the wrong
world, at the wrong altitude, or in the wrong place.

### Build vs Use

Am I **building** the agent with an SDK, where the layers live in code, or
**using** a finished coding agent, where configuration lives in files?

A product for end users is always the first, even when the product writes code.

### Root vs Symptom

Fix it where the value is born, with the source document still in view.

Downstream work is legitimate to flag a problem, never to quietly paper over
one. Deterministic is not the same as being in the right place.

### The Reliability Ladder

Climb only as far as the failure justifies.

| | Rung |
|---|---|
| ↑ | Architecture · hooks, gates |
| | Tool design · contracts, schemas |
| | Context · what is in the window |
| | Few-shot · worked examples |
| ↓ | Instruction · prose in a prompt |

The test is not "I want this to always happen." It is **what happens if it fails
once**. Money moved wrongly buys a gate. One wasted API round trip does not.

Too high is over-engineering: a trained classifier where a better description
would do. Too low is a band-aid: asking the model nicely where the rule must be
enforced.

> **Requests ask. Mechanisms impose.**

---

## Two habits that decide more questions than any single fact

**Exoneration clauses.** When a scenario tells you a component was reviewed and
is sound, or that syntax errors are gone, it is not reassurance. It is telling
you where the cause is not, and it usually eliminates two options before you
have read them.

**Multi-part cases.** Count the problems before you look at the options, then
map one fix to each. If both of your picks aim at the same half, one of them is
wrong by construction, however good it sounds.

---

## Move 3 · Near neighbors

The frame narrows the answer to two or three defensible options. These are what
separate them.

### Values keep coming back inconsistent. Constrain the field, or split the tool?

| Move | Move | Trap |
|---|---|---|
| **Input is open.** A field accepting anything → enumerate the allowed values, plus an escape value for genuinely novel and genuinely unclear cases. | **Output shape varies.** One tool returning a table, then an object, then prose → split it into tools with declared return shapes. | Constraining the input when what varies is the output. The consumer keeps breaking. |

### The agent keeps burning calls. Better descriptions, a resource, or narrower access?

| Move | Move | Move | Trap |
|---|---|---|---|
| **Picks the wrong tool** among those it is entitled to use → a fuller description: inputs, outputs, and when to use this one over the neighbor. | **Asks what exists.** Repeated exploratory calls to list what is available → expose the catalog as a resource. | **Uses what is not its job.** Crossing a role boundary → scope its tool set, keeping the frequent narrow need. | Caching. It makes the same calls faster; a resource makes them unnecessary. |

### Judgment is inconsistent between runs. Show it, write it, or have it check itself?

| Move | Move | Move | Trap |
|---|---|---|---|
| **Enumerable.** The team can write the conditions and each is checkable → explicit criteria, checked one at a time. | **Demonstrable.** Granularity, where to cut, ambiguous phrasing → a few worked examples showing why one reading beat the other. | **Neither.** Gaps vary unpredictably and no stable list exists → have it critique its own draft. | "Be more conservative." An intensity dial is not a criterion, and it silences good findings too. |

### Asynchronous batch, or synchronous?

Run the filters in order and stop at the first hit.

| Filter 1 | Filter 2 | Filter 3 | Only then | Trap |
|---|---|---|---|---|
| Is anything blocked waiting on the result? → synchronous | Does the available window cover the full processing window? If not → synchronous | Does it need tool calls mid-request? Batch cannot do that. | Nothing fired → batch. | Reaching for the 50% saving before running the filters. The saving is what you gain, never what decides. |

### Extraction failed validation. Will retrying with feedback help?

| Move | Trap |
|---|---|
| **Yes, it is shape.** Wrong format or structure → retry with the failed output and the specific errors attached. | **No, it is absent.** The value only exists in a document you never supplied. Retrying pushes the model to invent it. Make the field optional and let it return nothing. |

---

## Where the weight sits

Weights are from the published blueprint. Study by weight, not by comfort.

### D1 · Agentic Architecture & Orchestration, 27% of the blueprint

- The loop runs on the model's judgment, not a decision tree
- The API keeps no state; the history is resent
- Subagent context is isolated
- Delegate goals, not procedures
- Hooks before and after a tool call
- Fixed pipeline vs decomposition that adapts

### D3 · Claude Code Configuration & Workflows, 20% of the blueprint

- `CLAUDE.md` hierarchy: user, project, directory
- Path-scoped rules with globs
- Skills and their frontmatter
- Plan first vs go direct
- Refinement: examples, tests, or an interview
- Non-interactive runs with a declared output schema

### D4 · Prompt Engineering & Structured Output, 20% of the blueprint

- A schema validates fields, never relationships between them
- Required fields force fabrication; optional ones prevent it
- Retry fixes shape, never absent information
- Extract the stated value and the computed one, and flag the gap
- Batch: cheaper, a long window, no latency promise, no mid-request tools
- An independent reviewer beats self-review

### D2 · Tool Design & MCP Integration, 18% of the blueprint

- Descriptions are the primary selection mechanism
- Too many tools degrades selection
- Resources expose content; tools perform actions
- Server scope: shared with the team, or personal
- Credentials by environment variable, never committed
- Structured errors: category, retryable, readable cause

### D5 · Context Management & Reliability, 15% of the blueprint

- Keep the established facts where the model reliably attends
- Objective escalation triggers, never sentiment
- Propagate what needs a decision, with partial results
- Aggregate accuracy hides weak segments
- Conflicting sources: report both, with dates

---

Read the official Exam Guide first and treat this as the layer on top.
