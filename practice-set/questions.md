# Practice Set: Questions

60 items. Answers and explanations are in [answers.md](answers.md), deliberately in a separate file so the set can be sat cold.

> Independent study material. Not affiliated with, endorsed by, or reviewed by Anthropic. It reproduces no exam content: every item was written from the publicly published task statements in the official Exam Guide.

---

## Customer Support Resolution Agent

You are building a customer support resolution agent with the Claude Agent SDK and MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`), targeting 80%+ first-contact resolution.

### 1.

The agent sometimes stops mid-task, closing the conversation with a line like "I'll look that up now." Every tool the agent called returned successfully, and the loop exits as soon as the model produces text. What is the flaw?

- **A.** End the loop on `end_turn` rather than on the presence of assistant text.
- **B.** Raise `maxTurns`, which is capping the loop before the task can finish.
- **C.** Instruct the model to complete all tool work before producing narration.
- **D.** Append each tool result to the history so the model tracks what it did.

### 2.

Policy requires identity verification with `get_customer` before any refund executes. The system prompt states this explicitly and was reviewed for clarity, and 3% of transcripts still show `process_refund` running first. What should be done?

- **A.** Add explicit ordering language and two worked examples to the system prompt.
- **B.** Block `process_refund` programmatically until `get_customer` returns an id.
- **C.** Force `get_customer` with `tool_choice` on every request in the conversation.
- **D.** Route refunds to a subagent invoked only after verification has completed.

### 3.

The agent escalates mid-process to a human specialist who works from a separate queue and has no access to the conversation transcript. What should the handoff contain?

- **A.** The full transcript, so the specialist can form an independent judgment.
- **B.** The last three messages plus a read on the customer's current tone.
- **C.** A session link the specialist can open to review the case directly.
- **D.** Customer id, root cause, refund amount, and the recommended action.

### 4.

Three MCP tools return order status as a Unix timestamp, an ISO 8601 string, and a numeric code respectively. All three tools are healthy and their outputs are correct. The agent's reasoning about which event came first is inconsistent. Where does normalization belong?

- **A.** In each tool's description, documenting the timestamp format it returns.
- **B.** In the system prompt, as an explicit rule for comparing the three formats.
- **C.** In a `PreToolUse` hook that rewrites each request before it is dispatched.
- **D.** In a `PostToolUse` hook, before the model reasons over the returned values.

### 5.

A specialist subagent receives a prompt naming its task and the customer id. It completes every task it is given without error, yet its resolutions repeatedly violate constraints the customer stated earlier in the conversation. What explains this?

- **A.** Subagent context is isolated, so constraints must be restated in its prompt.
- **B.** The coordinator lacks `Task` in `allowedTools`, so the delegation is partial.
- **C.** The coordinator's context degraded before it composed the delegation prompt.
- **D.** Subagents retain parent memory only for the turn in which they are spawned.

### 6.

You return to an investigation session paused five days ago. Of its 26 cached tool results, 24 are order statuses that have since changed. The reasoning the session recorded about the customer's entitlement is unaffected by those changes. What do you do?

- **A.** Resume the session and flag in each response that statuses may be stale.
- **B.** Start fresh, inject a summary of the reasoning, and re-fetch the statuses.
- **C.** Resume the session and selectively re-fetch the 24 statuses that changed.
- **D.** Fork the session so both the old and the new investigation stay available.

### 7. _Select two_

Which two statements correctly describe `tool_choice`?

- **A.** Setting `any` forces a tool call but lets the model choose which one.
- **B.** Forcing one tool on every request prevents a final text answer.
- **C.** Setting `auto` guarantees the model calls at least one tool per turn.
- **D.** A forced tool selection persists for the remainder of the conversation.

### 8.

Before answering entitlement questions the agent calls `list_plans` to see what exists, then `get_plan` for the one it needs. `list_plans` runs in nearly every conversation and the catalog changes twice a year. An engineer proposes caching its response. What is the better approach?

- **A.** Cache the response, since the catalog changes only twice a year.
- **B.** Merge the two tools so a single call returns catalog and plan.
- **C.** Expose the plan catalog as an MCP resource the agent can consult.
- **D.** Sharpen the description so `list_plans` is called only when needed.

### 9.

A `run_report` tool takes a free-text spec and returns a rendered table, a JSON object, or prose depending on what was asked. Its description is thorough and accurate, and the tool is selected correctly every time. Downstream consumers fail on 20% of calls. What is the correct fix?

- **A.** Add an enum to the spec parameter listing the supported report types.
- **B.** Split it into purpose-specific tools with declared return shapes.
- **C.** Post-process the output into one shape before consumers receive it.
- **D.** Rename it and document the varying return shape in the description.

### 10.

Which is the weakest basis for escalating a conversation to a human?

- **A.** The customer has explicitly asked to speak with a person.
- **B.** The request falls outside the agent's documented authority.
- **C.** The agent reports low confidence in the answer it produced.
- **D.** Three turns have passed with no progress on the issue.

## Code Generation with Claude Code

You are configuring Claude Code for a team that shares one repository.

### 11.

Conventions for database migrations apply only when someone edits files under `migrations/`. They must load without anyone invoking them, and they should not occupy context when the work is elsewhere. Where do they belong?

- **A.** In a skill under `.claude/skills/` described as covering migrations.
- **B.** In the project `CLAUDE.md`, under a clearly marked migrations heading.
- **C.** In a rules file with a `paths` glob that matches `migrations/`.
- **D.** In a `.claude/commands/` command run before touching a migration.

### 12.

The team has a nine-step release procedure run about twice a month, and a file naming convention that applies to every file in the repository. Both are currently pasted into chat by hand. How should they be handled?

- **A.** The release procedure as a skill, the naming convention in `CLAUDE.md`.
- **B.** Both as skills, so that neither one loads until it becomes relevant.
- **C.** The release procedure in `CLAUDE.md`, the naming convention as a rule.
- **D.** The release procedure as a command, the naming convention as a skill.

### 13.

An engineer wants her personal preferences applied in every repository she works in, while the team's conventions must reach everyone who clones this one. Which pair is correct?

- **A.** `~/.claude/config.json` for hers, the repository `CLAUDE.md` for the team.
- **B.** `.claude/settings.yaml` for hers, the `.claude/rules/` directory for the team.
- **C.** The repository `CLAUDE.md` for both, with hers in a clearly marked section.
- **D.** `~/.claude/CLAUDE.md` for hers, the repository `CLAUDE.md` for the team.

### 14.

A developer asks for a fix to a null dereference in one utility function. She has the stack trace and the failing input, and the function has no other callers under change. What is the best first step?

- **A.** Enter plan mode so the change is scoped before any edit is made.
- **B.** Make the fix directly and review the resulting diff with her.
- **C.** Write a failing test first and iterate on it until it passes.
- **D.** Explore the function's call sites before changing anything at all.

### 15.

A team is adding rate limiting to a service for the first time. Nobody has worked with it before, and when asked what behavior they want they are unsure what they even need to specify. Which approach fits best?

- **A.** Supply input and output examples of limited and unlimited requests.
- **B.** Enter plan mode so the design is reviewed before implementation.
- **C.** Have the agent ask questions that surface what they have not considered.
- **D.** Implement a first version directly and refine it once the gaps appear.

### 16.

Two hours into a refactor the agent begins citing patterns typical of such services rather than what is in this repository, and repeats work it already completed. The code it produced earlier in the session was correct. What should be done?

- **A.** Move to a model configuration with a larger context window.
- **B.** Clear the context and restart with what has been learned so far.
- **C.** Persist the refactor state to a scratchpad and work from that file.
- **D.** Summarize the session so far and continue in the same session.

### 17.

A code review agent produces a long report. Reviewers act on the first and last sections and consistently miss issues in the middle, including severe ones. The findings themselves have been verified as accurate. What addresses this?

- **A.** Drop findings below a severity threshold so the report is shorter.
- **B.** Split the report into one comment attached to each affected file.
- **C.** Append a summary at the end so that nothing goes unnoticed.
- **D.** Lead with the key findings and add headers that make it navigable.

### 18.

You must assess whether a deprecation affects any of 11 packages, each around 80 files with its own conventions. The combined relevant code runs to several times your context window. Which approach fits?

- **A.** Grep the symbol across all packages and read the lines around each hit.
- **B.** Map each package from its imports before reading any implementation.
- **C.** Read the three largest packages in depth and generalize from those.
- **D.** Delegate one scoped subagent per package, each returning call sites.

### 19. _Select two_

A session is approaching its context limit. Tool outputs carry more than forty fields each, of which the agent uses four, and the conversation spans several topics that are already resolved. Which two actions are appropriate?

- **A.** Prune each tool output to the four fields the agent actually uses.
- **B.** Switch to a model configuration with a larger context window.
- **C.** Summarize the resolved topics, keeping the active thread verbatim.
- **D.** Start a new session so that the context is clean from this point.

### 20.

Which of these is not an appropriate response to a session approaching its context limit?

- **A.** Summarizing the portions of the conversation that are already resolved.
- **B.** Pruning verbose tool outputs down to the fields the agent actually uses.
- **C.** Persisting the working state externally and continuing from that file.
- **D.** Clearing the context and starting over without carrying a summary.

## Multi-Agent Research System

You are building a multi-agent research system: a coordinator delegating to web search, document analysis and synthesis subagents, producing a cited report.

### 21.

The coordinator spawns the same five subagents for every query. Narrow questions come back with overlapping material, and broad ones leave whole areas uncovered. Each subagent completes its assignment successfully. What is the root cause?

- **A.** The subagents cannot see each other's work, so overlap goes unnoticed.
- **B.** The decomposition is fixed rather than derived from the query itself.
- **C.** The synthesis step has no criteria for resolving overlapping claims.
- **D.** Five full reports exceed what the coordinator can hold at synthesis.

### 22.

After synthesis, the report leaves two of the original sub-questions unanswered. The team wants the system to close those gaps itself rather than shipping an incomplete report. Which design fits?

- **A.** Raise the number of subagents so more ground is covered on the first pass.
- **B.** Have the synthesis subagent flag each gap so the reader knows what is missing.
- **C.** Score coverage against the sub-questions, re-delegate, and re-synthesize.
- **D.** Have each subagent verify its own coverage before it returns to the coordinator.

### 23.

The coordinator needs four independent literature searches before drafting. It currently spawns them one per turn, each waiting for the previous to return, and latency is roughly four times what the team expected. What should change?

- **A.** Build one composite search tool that runs the four searches internally.
- **B.** Have the first subagent emit `Task` calls for the other three beneath it.
- **C.** Emit the four `Task` calls within a single coordinator response.
- **D.** Keep the sequence and narrow each subagent's scope to shorten it.

### 24.

The coordinator produces a written plan naming which subagents should run, then answers the question itself with no subagent executing. The subagent definitions are correct and their prompts have been reviewed. What is the most likely cause?

- **A.** `Task` is absent from the coordinator's allowed tools, so it cannot spawn.
- **B.** The system prompt frames delegation as guidance rather than as instruction.
- **C.** The subagent descriptions do not make clear when each of them applies.
- **D.** `maxTurns` is too low for the delegation round trip to complete in time.

### 25.

The coordinator must produce a comparative market report on three companies. Which step cannot run in parallel with the others?

- **A.** Retrieving the last four quarterly filings for each of the three companies.
- **B.** Searching recent news coverage for each of the three companies by name.
- **C.** Collecting analyst ratings for the three from two subscription sources.
- **D.** Writing the assessment that weighs the three companies against each other.

### 26.

The coordinator exposes `analyze_content` for retrieved web pages and `analyze_document` for uploaded files. Each description is accurate about its own tool and neither is malformed. Traces show uploaded PDFs routed to `analyze_content` in 38% of cases, and both invoked on the same item. What is the most effective fix?

- **A.** Expand `analyze_content`'s description until it excludes uploaded files.
- **B.** Merge the two into one tool that branches internally on the input type.
- **C.** Restrict `analyze_document` to the document analysis subagent's tool set.
- **D.** Rename both and have each description say when the other one applies.

### 27.

The synthesis subagent has no search tools by design. Review shows that in 15% of reports it needed to confirm a single figure, and a small share of those cases require reconciling sources that contradict each other. What is the most effective change?

- **A.** Give it the full `web_search` tool set the research subagents use.
- **B.** Give it a scoped `verify_fact` tool and route contradictions upward.
- **C.** Keep its tool set as it is and have the coordinator verify each figure.
- **D.** Move verification into the report step that runs after synthesis.

### 28. _Select two_

A document analysis subagent hits several failures in one run: a source times out and succeeds on retry, another returns a persistent authorization error, and a third returns zero matches. Which two responses follow the guidance?

- **A.** Return `isError: false` for the authorization failure, since nothing came back.
- **B.** Report the zero-match source as a valid empty result rather than an error.
- **C.** Return `isError` with a category, a retryable flag, and a readable cause.
- **D.** Return a uniform `source unavailable` status so all failures look alike.

### 29.

The team wants to connect a widely used issue tracker with a maintained community MCP server. A developer proposes writing their own instead, to keep full control. What do you tell them?

- **A.** Write the custom server, since control over a central integration is worth it.
- **B.** Write the custom server, because the tracker touches every team process.
- **C.** Wrap the community server in a custom one to add team-specific behavior.
- **D.** Use the community server and keep custom builds for team-specific work.

### 30.

Two sources report headcount for the same company: a regulatory filing dated March states 4,200, and a press article dated September states 3,850. Both sources are credible. The report must be defensible to the client. What should the agent do?

- **A.** Report both figures with their sources and their collection dates attached.
- **B.** Report the filing's figure, since regulatory filings outrank press coverage.
- **C.** Report the September figure, since the later reading supersedes the earlier.
- **D.** Report the average of the two, with a note describing the range observed.

## Developer Productivity with Claude

You are building developer productivity tools with the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, and automate repetitive tasks, using the built-in tools (Read, Write, Bash, Grep, Glob) and integrating with MCP servers.

### 31.

A job must run against every component test file in the monorepo. The convention is a `.test.tsx` suffix, three legacy directories still use `.spec.tsx`, and some test files import shared helpers while others define their own. What produces the complete list most reliably?

- **A.** Grep for `describe(` and `it(`, collecting every file that matches.
- **B.** Glob for `**/*.test.tsx` and `**/*.spec.tsx`, then merge the two.
- **C.** Grep for imports of the shared helpers and collect those files.
- **D.** Glob for `**/*.tsx` and read each file to decide what it is.

### 32.

A configuration constant appears in seven places in one file, and only the occurrence inside the staging block should change. The `Edit` call fails because the target text is not unique. What do you do?

- **A.** Extend the search text with surrounding lines until the match is unique.
- **B.** Use a replace-all edit and then revert the six unintended changes.
- **C.** Read the file, change the intended occurrence, and write it back whole.
- **D.** Append the corrected constant at the end so the later value wins.

### 33.

You need every call site of `validateToken`, which is exported from `auth/core.ts` and re-exported under different names by three wrapper modules. The wrappers themselves are documented and correct. What is the correct first move?

- **A.** Grep for `validateToken` repository-wide and compile the matches found.
- **B.** Glob for the files under `auth/` and read each one of them in turn.
- **C.** Read the library and wrappers for every exported name, then search each.
- **D.** Grep for imports of `auth/core` and trace outward from those files.

### 34.

You must understand how retry backoff is reached in an unfamiliar 28-file service before changing it. The whole service fits comfortably inside your context window. Which approach fits best?

- **A.** Read all 28 files in order so nothing in the service is missed.
- **B.** Glob for the files whose names reference retry or backoff logic.
- **C.** Delegate the survey to a subagent and work from the report it returns.
- **D.** Grep the retry entry points, read those, and follow their imports.

### 35.

Two engineers working in the same repository, on the same version, get noticeably different behavior from the assistant. Both have pulled the latest commit. What is the first step to diagnose it?

- **A.** Check which memory files each session has actually loaded.
- **B.** Compare their user-level settings files line by line for drift.
- **C.** Have both re-clone the repository to rule out a stale checkout.
- **D.** Consolidate every project convention into one `CLAUDE.md` file.

### 36.

A review across 40 changed files produces findings that contradict one another and misses issues in the middle of the set. The review criteria themselves have been validated on smaller changes. How should the review be decomposed?

- **A.** Run the same review once more against a more capable model tier.
- **B.** Review only the files carrying the largest diffs in the change set.
- **C.** Ask the model to re-read the full set before it states conclusions.
- **D.** Run per-file local passes plus one separate cross-file integration pass.

### 37.

Which of these does not describe how the agentic loop operates?

- **A.** It continues on `tool_use` and terminates when `end_turn` is returned.
- **B.** Tool results are appended to the history sent with the next request.
- **C.** The program reads the assistant's text to judge whether work is done.
- **D.** The model decides at each step whether to call a tool or to answer.

### 38.

Policy states that deletions above a threshold must never execute without a recorded approval. Deletions can be requested at any point in a session, and the current prompt-based rule is followed in the large majority of cases. Which mechanism enforces this?

- **A.** A `PreToolUse` hook that blocks the call and routes it to approval.
- **B.** A `PostToolUse` hook that records the approval once deletion completes.
- **C.** `tool_choice` forcing the approval tool on the turn after the request.
- **D.** A system prompt rule stating the threshold, plus two worked examples.

### 39. _Select two_

Which two statements are correct about subagent configuration?

- **A.** The `allowedTools` list restricts which tools the subagent may call.
- **B.** A subagent inherits the coordinator's conversation history automatically.
- **C.** A subagent's `systemPrompt` is inherited unless it is explicitly set.
- **D.** A coordinator can spawn subagents only if `Task` is among its tools.

### 40.

You want to compare two refactoring approaches that both start from the same completed codebase analysis, and you expect to revisit both branches later. What fits?

- **A.** Fork the session so each approach branches from the shared baseline.
- **B.** Resume the analysis session twice in succession by its session name.
- **C.** Start two fresh sessions, injecting the analysis summary into each.
- **D.** Continue the most recent session once the first approach is finished.

## Claude Code for Continuous Integration

You are integrating Claude Code into your CI/CD pipeline. It runs automated code reviews, generates test cases, and gives feedback on pull requests, and your prompts need to be actionable and to minimize false positives.

### 41.

A nightly job must run the assistant without any interaction and emit machine-readable findings that a later step posts automatically as inline comments. Which invocation is correct?

- **A.** Set `CLAUDE_HEADLESS=1` and parse the job's standard output.
- **B.** Run with `--batch` and read the aggregated results file it writes.
- **C.** Run with `-p`, `--output-format json`, and `--json-schema`.
- **D.** Run interactively in the container and capture the terminal output.

### 42.

The pipeline reviews several pull requests within one run, and reviewers notice comments on one pull request that reference code belonging to another. Each review on its own is accurate. What should the pipeline do?

- **A.** Clear the context between pull requests inside the same session.
- **B.** Run each pull request in a session isolated from the others.
- **C.** Reduce how many pull requests are handled in a single run.
- **D.** Instruct the agent to consider only the current diff each time.

### 43.

When the review re-runs after new commits, it posts duplicate comments on issues that were already raised and discussed in the thread. The findings themselves are accurate. What should change?

- **A.** Supply the prior findings and ask for new or unaddressed issues only.
- **B.** Review only the diff introduced by the most recent commit each time.
- **C.** Deduplicate the comments after they have been posted to the thread.
- **D.** Run the review a single time, when the pull request is first opened.

### 44.

Generated tests frequently duplicate scenarios the existing suite already covers. The duplicated tests are themselves correct and they pass. What addresses this?

- **A.** Ask for a smaller number of generated tests on each run.
- **B.** Filter out duplicates after the generation step completes.
- **C.** Generate tests only for files that currently have no coverage.
- **D.** Provide the existing test files in context during generation.

### 45.

The tests the CI job generates are low value: trivial assertions, the wrong fixtures, and coverage of paths nobody cares about. The job invocation and output handling are both correct. What is the most effective change?

- **A.** Document the standards, what makes a test valuable, and the fixtures.
- **B.** Add few-shot examples of well-written tests to the prompt used in CI.
- **C.** Raise the model tier the continuous integration job runs against.
- **D.** Have a second instance review the generated tests before they land.

### 46.

A module has a suite of assertions that already define its expected behavior, including its edge cases, and the implementation is now being written against them. Which refinement technique fits?

- **A.** Iterate by sharing the failing tests until the suite passes.
- **B.** Provide two or three input and output examples to work from.
- **C.** Have the agent interview the team about the module's design.
- **D.** Enter plan mode before any implementation code is written.

### 47.

The pipeline runs two workloads. A pre-merge check blocks the merge and requires the agent to call repository tools while it reasons. A weekly audit of the whole repository is read on Monday mornings and is submitted the preceding Friday. How should each be run?

- **A.** Both with the batch API, since both are bounded and repeatable jobs.
- **B.** Both synchronously, because batch carries no guaranteed latency floor.
- **C.** Pre-merge with batch at pull request open, and the audit synchronously.
- **D.** Pre-merge synchronously, and the weekly audit with the batch API.

### 48.

The team wants to catch subtle defects in code the same pipeline generated earlier in the run. Which approach is least effective?

- **A.** Reviewing in a separate instance that lacks the generation context.
- **B.** Having the generating session review its own output while thinking.
- **C.** Splitting the review into per-file passes plus a cross-file pass.
- **D.** Having the review self-report confidence per finding for triage.

### 49.

The review reports 14 findings per pull request and developers act on 4. The noise is concentrated in style-adjacent observations about patterns that are established conventions in this repository. A developer proposes adding "only report high-confidence issues" to the prompt. What is the most effective change?

- **A.** Add the proposed instruction, since it directly targets over-reporting.
- **B.** Have the agent critique its findings and drop the ones it cannot justify.
- **C.** Name explicitly which issue classes to report and which ones to skip.
- **D.** Attach a confidence score to each finding and suppress the low ones.

### 50. _Select two_

The continuous integration job must decide automatically whether to block a merge. Which two approaches produce output the pipeline can rely on?

- **A.** Ask for JSON in the prompt and parse the model's text output.
- **B.** Have the agent write prose and search it for a verdict keyword.
- **C.** Define a tool whose input is the verdict schema and read `tool_use`.
- **D.** Run headless with `--output-format json` and a declared verdict schema.

## Structured Data Extraction

You are building a structured data extraction pipeline that converts documents into JSON records.

### 51.

The pipeline uses tool use with a strict JSON schema, and the team confirms that schema violations and JSON syntax errors no longer occur. Operations reports that 8% of records carry the purchase order number in the invoice number field, and 5% have line items that do not sum to the declared total. What is the most likely cause?

- **A.** Field descriptions do not distinguish the two identifier fields clearly.
- **B.** The values are semantically wrong, which a schema has no way to detect.
- **C.** Source layouts vary, so few-shot examples are needed for consistency.
- **D.** The model is fabricating values for fields the documents do not contain.

### 52.

A contract schema includes `governing_law`, `renewal_term`, and `liability_cap`, and 30% of contracts genuinely omit at least one of the three. Which approach is least appropriate?

- **A.** Keeping all three required so every record arrives downstream complete.
- **B.** Declaring them nullable and instructing a null when the clause is absent.
- **C.** Adding an "unclear" value for clauses present but ambiguously worded.
- **D.** Flagging records that contain nulls so a reviewer confirms the omission.

### 53.

A product schema uses an enum of eight categories that covers 94% of listings. The remainder are genuinely novel products, and a separate handful of listings are worded too vaguely to categorize at all. What should the schema add?

- **A.** Forty categories in place of eight, so novel products find a match.
- **B.** A nullable category field that the model leaves empty when unsure.
- **C.** A free-text category with a mapping table maintained downstream.
- **D.** An "other" value with a detail field, plus an "unclear" value.

### 54.

Three document types arrive through the same pipeline, each with its own extraction tool and schema. The type is not known until the document has been read, and every document must produce a structured record. Which `tool_choice` setting fits?

- **A.** `auto`, so the model can decide whether extraction is needed at all.
- **B.** Forced selection on the tool for the most common document type.
- **C.** `any`, so a tool must be called and the model picks the schema.
- **D.** No tool at all, deciding the schema in code before making the call.

### 55.

Validation fails on two groups. In one, `effective_date` returns as `03/04/2026` where ISO 8601 is expected. In the other, `counterparty_registration` is empty because it appears only in an annex that was never part of the input. The team raises the retry limit with validation feedback attached. What will that achieve?

- **A.** It resolves both groups, since retry with feedback is the standard remedy.
- **B.** It fixes the dates and pushes the model to invent registration numbers.
- **C.** It resolves neither, since retries only address transient API failures.
- **D.** It fixes the registration group by forcing a closer read of the source.

### 56.

Discrepancies between a document's stated total and its itemized amounts must surface before records reach the ledger. The extraction itself is schema-compliant. Which design does that?

- **A.** Extract a calculated total beside the stated one and flag any difference.
- **B.** Add a required boolean the model sets after checking its own arithmetic.
- **C.** Restrict the total field in the schema to two-decimal numeric values.
- **D.** Retry the extraction whenever the ledger rejects an incoming record.

### 57.

Research papers cite sources in two ways: inline in the body, or gathered in a bibliography. Extraction of the citation fields is consistent within each style but differs between them, and the schema is satisfied in both cases. What addresses this?

- **A.** Tighten the citation field definitions in the extraction schema.
- **B.** Post-process the extracted citations into one common shape.
- **C.** Retry extraction with validation feedback when the style differs.
- **D.** Give few-shot examples of correct extraction from both structures.

### 58. _Select two_

A batch of 12,000 documents returns with 400 failures caused by exceeding the context limit. A 50,000-document run is planned for next month. Which two actions are appropriate?

- **A.** Split the coming run into five batches so that failures stay contained.
- **B.** Refine the prompt on a sample set before the 50,000-document run.
- **C.** Resubmit the full batch with chunking applied to every document.
- **D.** Resubmit only the failures, keyed by `custom_id`, once chunked.

### 59.

Before removing human review for one document type, the team measures 96% field-level accuracy across all document types combined, which clears the agreed threshold. What should govern the decision?

- **A.** The 96% figure, since it already exceeds the threshold the team agreed.
- **B.** Accuracy measured on that document type alone, which the aggregate hides.
- **C.** The agent's self-reported confidence on that type over a sampling window.
- **D.** The overall rate at which reviewers currently change the agent's output.

### 60.

An extraction cannot determine a value because the source wording is genuinely ambiguous, and the downstream system expects the field to be populated. What should the pipeline do?

- **A.** Return the most likely reading, with a note recording the ambiguity.
- **B.** Return the designated "unclear" value and flag the record for review.
- **C.** Leave the field empty and let the downstream system decide what to do.
- **D.** Retry the extraction until it produces a determinate, populated value.
