# Practice Set: Answers and Explanations

Score by domain rather than by total. Every option carries an explanation, because the reason a plausible option fails is the part worth learning.

> Independent study material. Not affiliated with, endorsed by, or reviewed by Anthropic. It reproduces no exam content: every item was written from the publicly published task statements in the official Exam Guide.

---

### 1. Correct answer: A

`D1 · Task 1.1`

- **✓** **A.** The stop signal is structural, and a single turn can carry both text and a `tool_use` block. Treating text as completion truncates work the model intended to continue.
- ✗ **B.** An iteration cap is a safety fuse, never the primary stopping mechanism; the loop here is ending early by design, not by exhaustion.
- ✗ **C.** Prose cannot repair a mechanical termination condition that fires before the model is consulted again.
- ✗ **D.** Dropping tool results produces an agent that loses track of its work, not one that halts while announcing an intention.

**Why:** The loop terminates on `stop_reason`, and text and a tool call can arrive together.

<sub>Exam Guide: 1.1 Skills in: avoiding anti-patterns such as checking for assistant text content as a completion indicator</sub>

### 2. Correct answer: B

`D1 · Task 1.4`

- ✗ **A.** This is the mechanism that already failed. Prompt instructions retain a non-zero failure rate, and the 3% is that rate.
- **✓** **B.** A prerequisite gate makes the out-of-order call structurally impossible rather than merely discouraged.
- ✗ **C.** Forcing the tool on every request is the right mechanism at the wrong scope: the agent could never return a final answer.
- ✗ **D.** Moving the call into a subagent relocates the work without gating it; nothing prevents the subagent from being invoked early.

**Why:** When compliance must be deterministic, a request is not a guarantee.

<sub>Exam Guide: 1.4 Skills in: implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed</sub>

### 3. Correct answer: D

`D1 · Task 1.4`

- ✗ **A.** Handing over raw material transfers the reading work rather than the conclusion, and the specialist has to redo the diagnosis.
- ✗ **B.** Three messages are a fragment of the case, and tone is not a fact the specialist can act on.
- ✗ **C.** The scenario states the specialist has no transcript access, so a link resolves to nothing.
- **✓** **D.** A self-contained package gives the specialist identity, cause, amount at stake, and a proposed action, which is everything needed to act.

**Why:** A handoff is a decision package, not a pointer to where the decision could be reconstructed.

<sub>Exam Guide: 1.4 Skills in: compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to human agents who lack access to the conversation transcript</sub>

### 4. Correct answer: D

`D1 · Task 1.5`

- ✗ **A.** Documenting the inconsistency leaves the model to reconcile it on every comparison instead of removing the variance.
- ✗ **B.** A prompt rule asks the model to do conversion work reliably on every turn, which is precisely what it is failing to do.
- ✗ **C.** A pre-call hook intercepts the outgoing request; the heterogeneity is in what comes back.
- **✓** **D.** Results are transformed once, in code, before they enter the model's reasoning at all.

**Why:** Normalize where the variance enters, not where the model has to cope with it.

<sub>Exam Guide: 1.5 Skills in: implementing PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools before the agent processes them</sub>

### 5. Correct answer: A

`D1 · Task 1.3`

- **✓** **A.** A subagent sees its prompt and nothing else. A constraint stated to the coordinator never reaches it unless it is written into the delegation.
- ✗ **B.** Without `Task` the coordinator could not spawn the subagent at all; here the subagent runs and completes work.
- ✗ **C.** Degradation would produce erratic delegations across the board, not the consistent omission of one class of information.
- ✗ **D.** There is no partial inheritance window. Subagents do not inherit parent memory at any point.

**Why:** Isolation is total, so anything the subagent must honor has to be handed to it.

<sub>Exam Guide: 1.3 Knowledge of: that subagent context must be explicitly provided in the prompt, subagents do not automatically inherit parent context</sub>

### 6. Correct answer: B

`D1 · Task 1.7`

- ✗ **A.** A caveat does not stop the model from reasoning over the stale values that are still sitting in context.
- **✓** **B.** When the great majority of tool results are stale, the reliable move is a clean session carrying forward only the part that survived, which is the reasoning.
- ✗ **C.** Targeted re-fetch is the right call when most of the context still holds. Here 24 of 26 results are invalid, so the session is stale rather than lightly outdated.
- ✗ **D.** Forking preserves a baseline for divergent exploration, which is not the problem: there is one line of investigation and its data expired.

**Why:** Resume when context is mostly valid; restart with a summary when it mostly is not.

<sub>Exam Guide: 1.7 Skills in: choosing between session resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale)</sub>

### 7. Correct answers: A, B

`D2 · Task 2.3`

- **✓** **A.** `any` guarantees a call is made while leaving selection to the model.
- **✓** **B.** If every request must call the named tool, the turn that would carry the final answer is consumed by another call.
- ✗ **C.** `auto` leaves the model free to answer in text without calling anything; that is exactly what distinguishes it from `any`.
- ✗ **D.** `tool_choice` is set per request. Nothing carries it forward on its own.

**Why:** `any` guarantees a call; `auto` does not; and forcing is per request, not a mode.

<sub>Exam Guide: 2.3 Knowledge of: tool_choice configuration options: "auto", "any", and forced tool selection</sub>

### 8. Correct answer: C

`D2 · Task 2.4`

- ✗ **A.** Caching is defensible and would help, but it only makes an unnecessary call cheap. The call itself is what should disappear.
- ✗ **B.** Merging couples a browse operation to a fetch operation and returns catalog data the agent usually does not need.
- **✓** **C.** A resource gives the agent visibility into what exists without spending a tool call to ask.
- ✗ **D.** The agent is not calling the tool by mistake; it calls it because it genuinely has no other way to see the catalog.

**Why:** A resource makes the exploratory call unnecessary; a cache only makes it faster.

<sub>Exam Guide: 2.4 Knowledge of: MCP resources as a mechanism for exposing content catalogs to reduce exploratory tool calls</sub>

### 9. Correct answer: B

`D2 · Task 2.1`

- ✗ **A.** An enum constrains what goes in. What varies here is what comes out, so the consumers keep breaking.
- **✓** **B.** Each report type becomes a tool with a typed parameter and a single declared return shape, which is a contract consumers can rely on.
- ✗ **C.** A normalization layer hides the variance from consumers while leaving three shapes flowing through the system.
- ✗ **D.** The description is already accurate and selection already works; documenting the variance does not remove it.

**Why:** Varying input takes an enum; varying output takes separate tools.

<sub>Exam Guide: 2.1 Skills in: splitting generic tools into purpose-specific tools with defined input/output contracts</sub>

### 10. Correct answer: C

`D5 · Task 5.2`

- ✗ **A.** An explicit request for a human is the strongest trigger there is, and it is honored immediately.
- ✗ **B.** Acting outside documented authority is exactly the boundary escalation exists to respect.
- **✓** **C.** A self-reported score is the model grading its own work, and it correlates poorly with whether the case is actually beyond the agent.
- ✗ **D.** Lack of progress is observable from the outside and does not depend on the model assessing itself.

**Why:** Escalation triggers should be observable, not self-reported.

<sub>Exam Guide: 5.2 Knowledge of: why sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity</sub>

### 11. Correct answer: C

`D3 · Task 3.3`

- ✗ **A.** A skill is invoked on demand. Its description makes it findable, not automatic, so the conventions load only when someone thinks to ask.
- ✗ **B.** `CLAUDE.md` is always loaded, so the conventions would occupy context during every unrelated task.
- **✓** **C.** Path-scoped rules load automatically and only when a matching file is being edited, which is both requirements at once.
- ✗ **D.** A command depends on the engineer remembering to run it, which is the automatic loading the scenario rules out.

**Why:** Automatic plus conditional is exactly what a path glob buys you.

<sub>Exam Guide: 3.3 Skills in: creating .claude/rules/ files with YAML frontmatter path scoping so rules load only when editing matching files</sub>

### 12. Correct answer: A

`D3 · Task 3.2`

- **✓** **A.** A long procedure needed twice a month is on-demand work; a convention that governs every file is a universal standard that should always be loaded.
- ✗ **B.** Making the naming convention on-demand means it is absent from the many edits where nobody thinks to invoke it.
- ✗ **C.** This inverts both: a nine-step procedure occupies context permanently while a repository-wide rule loads only for some paths.
- ✗ **D.** A command is a reasonable home for a procedure, but putting a universal convention behind on-demand invocation repeats the error in B.

**Why:** Frequency and scope decide the home: universal and always, or specific and on demand.

<sub>Exam Guide: 3.2 Skills in: choosing between skills (on-demand invocation for task-specific workflows) and CLAUDE.md (always-loaded universal standards)</sub>

### 13. Correct answer: D

`D3 · Task 3.1`

- ✗ **A.** The project half is right, but instructions for Claude live in `CLAUDE.md`; there is no `config.json` in this hierarchy.
- ✗ **B.** `.claude/rules/` is a real home for team conventions, but a settings file is not where personal instructions go, and this pair puts hers inside the repository.
- ✗ **C.** Anything committed to the repository reaches everyone who clones it, so her preferences would be imposed on the team.
- **✓** **D.** User-level configuration follows the person across every repository and is never shared; project-level travels with the clone.

**Why:** The axis is who receives it: the user everywhere, or everyone who clones this repository.

<sub>Exam Guide: 3.1 Knowledge of: the CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level, and directory-level; user-level settings are not shared with teammates via version control</sub>

### 14. Correct answer: B

`D3 · Task 3.4`

- ✗ **A.** Plan mode earns its cost on architectural decisions and multi-file work; here the scope is one function and the cause is already known.
- **✓** **B.** A single-file fix with a known cause and a known failing input is the textbook case for direct execution.
- ✗ **C.** Test-driven iteration is valuable when behavior is unclear, but the failing input is already in hand and the fix is one line of judgment.
- ✗ **D.** Call-site exploration matters when a signature changes; the scenario states the callers are not in scope.

**Why:** Plan mode is for choosing among approaches, not for changes with one obvious shape.

<sub>Exam Guide: 3.4 Skills in: selecting direct execution for well-understood changes with clear scope (e.g., a single-file bug fix with a clear stack trace)</sub>

### 15. Correct answer: C

`D3 · Task 3.5`

- ✗ **A.** Examples are the strongest tool when you know the transformation you want. This team cannot yet state it.
- ✗ **B.** Plan mode produces a plan from the requirements you bring it, and the requirements are the missing piece.
- **✓** **C.** The interview pattern surfaces the considerations a team new to a domain does not know to raise, which is precisely the stated gap.
- ✗ **D.** Building first and discovering the requirements through rework is the cost the interview is meant to avoid.

**Why:** When the team cannot state the requirement, elicit it before designing to it.

<sub>Exam Guide: 3.5 Skills in: using the interview pattern to surface design considerations before implementing solutions in unfamiliar domains</sub>

### 16. Correct answer: C

`D5 · Task 5.4`

- ✗ **A.** A larger window delays the same degradation without addressing where the findings live.
- ✗ **B.** Clearing discards the specific discoveries that are the expensive part of the session.
- **✓** **C.** A scratchpad moves the findings out of the window entirely, so they survive degradation and can be referenced deliberately.
- ✗ **D.** An in-session summary is a reasonable step, but it leaves the record inside the same degrading context it is meant to protect.

**Why:** Degradation is about where findings live, not how much room they have.

<sub>Exam Guide: 5.4 Skills in: having agents maintain scratchpad files recording key findings, referencing them for subsequent questions to counteract context degradation</sub>

### 17. Correct answer: D

`D5 · Task 5.1`

- ✗ **A.** Filtering by severity removes real findings to work around a position effect, and the missed issues include severe ones.
- ✗ **B.** Per-file comments are a genuine improvement in delivery, but each one still has a middle that readers skim.
- ✗ **C.** A trailing summary reinforces the end, which is already one of the two positions readers do attend to.
- **✓** **D.** Front-loading what matters and giving the body explicit structure works with the way long inputs are read rather than against it.

**Why:** Information in the middle gets lost, so put what matters where attention lands.

<sub>Exam Guide: 5.1 Skills in: placing key findings summaries at the beginning of aggregated inputs and organizing detailed results with explicit section headers to mitigate position effects</sub>

### 18. Correct answer: D

`D5 · Task 5.4`

- ✗ **A.** Grep finds the direct hits and misses every package that renames the symbol behind a wrapper, which is likely across 11 sets of conventions.
- ✗ **B.** Structural mapping is the right opening move for understanding one unfamiliar package, but eleven maps still land in the same window.
- ✗ **C.** Generalizing from three packages assumes the other eight follow their conventions, which the scenario explicitly denies.
- **✓** **D.** Each subagent absorbs the exploration in its own context and returns a compact answer, so the coordinator holds only conclusions.

**Why:** When the material exceeds the window, delegate the reading and keep the conclusions.

<sub>Exam Guide: 5.4 Skills in: spawning subagents to investigate specific questions while the main agent preserves high-level coordination</sub>

### 19. Correct answers: A, C

`D5 · Task 5.1`

- **✓** **A.** Thirty-six unused fields per call are pure accumulation, and trimming them is the cheapest reclamation available.
- ✗ **B.** A larger window postpones the limit without reducing what is consuming it.
- **✓** **C.** Compressing what is settled while preserving what is live is the shape progressive summarization is meant to take.
- ✗ **D.** A clean session discards the resolved history along with the active thread that still needs it.

**Why:** Reclaim context by removing what is unused and compressing what is finished.

<sub>Exam Guide: 5.1 Skills in: trimming verbose tool outputs to only relevant fields before they accumulate in context; extracting transactional facts into a persistent block outside summarized history</sub>

### 20. Correct answer: D

`D5 · Task 5.4`

- ✗ **A.** Compressing settled material is the standard way to reclaim room without losing the thread.
- ✗ **B.** Field pruning removes accumulation that was never contributing to the reasoning.
- ✗ **C.** Externalizing state is what allows work to cross a context boundary intact.
- **✓** **D.** Starting over with nothing carried forward throws away the findings the session was assembling, which is the cost the other three avoid.

**Why:** Every remedy here preserves the findings except the one that discards them.

<sub>Exam Guide: 5.4 Skills in: summarizing key findings from one exploration phase before spawning sub-agents for the next phase, injecting summaries into initial context</sub>

### 21. Correct answer: B

`D1 · Task 1.2`

- ✗ **A.** Subagent isolation is by design, and the coordinator is the component meant to prevent overlap by partitioning scope before delegating.
- **✓** **B.** One pipeline for every query is too much machinery for a narrow question and too little for a broad one, which is exactly the two symptoms reported.
- ✗ **C.** Deduplicating at synthesis tidies the output after the redundant work has already been paid for, and it does nothing for the uncovered areas.
- ✗ **D.** A capacity ceiling would truncate results, not produce coverage that is simultaneously duplicated and incomplete.

**Why:** The coordinator should choose the decomposition per query, not run a fixed pipeline.

<sub>Exam Guide: 1.2 Skills in: designing coordinator agents that analyze query requirements and dynamically select which subagents to invoke rather than always routing through the full pipeline</sub>

### 22. Correct answer: C

`D1 · Task 1.2`

- ✗ **A.** More parallel work widens the first pass without ever checking whether the questions were answered.
- ✗ **B.** Annotating the gaps is honest reporting and worth doing, but the team asked for the system to close them, not to describe them.
- **✓** **C.** Evaluating the synthesis against the original sub-questions and re-delegating targeted queries is the loop that converges on coverage.
- ✗ **D.** A subagent can confirm it finished its own assignment; it cannot know which sub-questions the report as a whole still misses.

**Why:** Coverage is a property of the whole report, so only the coordinator can judge it.

<sub>Exam Guide: 1.2 Skills in: implementing iterative refinement loops where the coordinator evaluates synthesis output for gaps, re-delegates to search and analysis subagents with targeted queries, and re-invokes synthesis until coverage is sufficient</sub>

### 23. Correct answer: C

`D1 · Task 1.3`

- ✗ **A.** A composite tool builds new infrastructure to obtain parallelism the coordinator can already express natively.
- ✗ **B.** Nested spawning does run the work concurrently, but it moves three subagents outside the coordinator's view and breaks hub-and-spoke observability.
- **✓** **C.** Multiple `Task` calls in one response start the four searches together while every result still returns to the coordinator.
- ✗ **D.** Four shorter serial steps are still four serial steps, and the searches are independent.

**Why:** Parallelism comes from one response carrying several calls, not from nesting agents.

<sub>Exam Guide: 1.3 Skills in: spawning parallel subagents by emitting multiple Task tool calls in a single coordinator response rather than across separate turns</sub>

### 24. Correct answer: A

`D1 · Task 1.3`

- **✓** **A.** The coordinator reasons about delegation correctly and then has no mechanism to act, which is exactly what reasoning-but-not-executing looks like.
- ✗ **B.** Softly worded delegation would produce inconsistent spawning across runs, not a plan that names the right subagents and then never invokes any.
- ✗ **C.** Poor descriptions cause the wrong subagent to be chosen; here the coordinator names the right ones.
- ✗ **D.** A turn ceiling truncates work in progress rather than preventing the first call from ever being emitted.

**Why:** Naming the right subagent and never calling it points at the tool, not the prompt.

<sub>Exam Guide: 1.3 Knowledge of: the Task tool as the mechanism for spawning subagents, and the requirement that allowedTools must include Task for a coordinator to invoke subagents</sub>

### 25. Correct answer: D

`D1 · Task 1.6`

- ✗ **A.** Filing retrieval is per company and depends on nothing else in the list.
- ✗ **B.** News searches are independent per company and can be issued at once.
- ✗ **C.** Rating collection touches two sources and no other step's output.
- **✓** **D.** A comparison consumes all three companies' material, so it can only start once the gathering steps have returned.

**Why:** Gathering fans out; the step that consumes every branch has to wait.

<sub>Exam Guide: 1.6 Skills in: selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation</sub>

### 26. Correct answer: D

`D2 · Task 2.1`

- ✗ **A.** Adding exclusions to one side leaves the other still describing itself in terms that fit both, so the boundary is only half drawn.
- ✗ **B.** Merging removes the confusion by removing the distinction, which costs the specificity that made two tools worth having.
- ✗ **C.** Scoping stops one subagent from reaching the wrong tool, but the coordinator itself is the component doing the misrouting.
- **✓** **D.** Names that do not compete, plus descriptions that each point at the other's territory, remove the ambiguity from both sides at once.

**Why:** Overlap lives between two descriptions, so both have to change.

<sub>Exam Guide: 2.1 Skills in: renaming tools and updating descriptions to eliminate functional overlap (e.g., renaming analyze_content to extract_web_results with a web-specific description)</sub>

### 27. Correct answer: B

`D2 · Task 2.3`

- ✗ **A.** Handing a synthesis agent the full research kit is the over-broad access that leads agents to misuse tools outside their specialization.
- **✓** **B.** A narrow tool covers the frequent simple need in place, while the harder judgment stays with the component that can see all the sources.
- ✗ **C.** Pre-verifying every figure pays the cost on 100% of figures to serve the 15% that need it.
- ✗ **D.** Verifying after synthesis means the claim has already been written into the report before anyone checks it.

**Why:** Scope the frequent simple case locally and escalate the rare hard one.

<sub>Exam Guide: 2.3 Skills in: providing scoped cross-role tools for high-frequency needs (e.g., a verify_fact tool for the synthesis agent) while routing complex cases through the coordinator</sub>

### 28. Correct answers: B, C

`D2 · Task 2.2`

- ✗ **A.** Reporting a permission failure as an empty result silently converts a problem into an answer, and the coordinator never learns it needs credentials.
- **✓** **B.** A successful query that matched nothing is information, not a fault, and labeling it an error would trigger pointless retries.
- **✓** **C.** Category, retryability, and a readable cause are exactly what let the coordinator choose between retrying, escalating, and moving on.
- ✗ **D.** A uniform message is what prevents recovery: the coordinator cannot tell a timeout worth retrying from a permission wall that never will be.

**Why:** An empty result is an answer; a failure needs enough structure to act on.

<sub>Exam Guide: 2.2 Skills in: returning structured error metadata including errorCategory, isRetryable boolean, and human-readable descriptions; distinguishing between access failures and valid empty results</sub>

### 29. Correct answer: D

`D2 · Task 2.4`

- ✗ **A.** Control over a standard integration buys little and costs the ongoing maintenance of an API surface someone else already tracks.
- ✗ **B.** How central the tracker is argues for a well-maintained integration, not for a bespoke one the team must keep current alone.
- ✗ **C.** Wrapping is the right instinct once there is genuine team-specific behavior to add, but nothing in the scenario says there is any yet.
- **✓** **D.** Standard integrations are where community servers are strongest, and custom effort is reserved for what only this team needs.

**Why:** Build custom where the workflow is yours, not where the integration is standard.

<sub>Exam Guide: 2.4 Skills in: choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira), reserving custom servers for team-specific workflows</sub>

### 30. Correct answer: A

`D5 · Task 5.6`

- **✓** **A.** With both values dated and attributed, the reader can see whether this is a contradiction or a company that shrank over six months.
- ✗ **B.** Ranking sources by type discards a later observation on the strength of a general rule about credibility.
- ✗ **C.** Preferring the newer figure assumes the two are measuring the same moment, which is the very thing the dates would settle.
- ✗ **D.** Averaging invents a number that neither source reported and that describes no point in time.

**Why:** Dates decide whether two figures conflict or simply describe different moments.

<sub>Exam Guide: 5.6 Knowledge of: how to handle conflicting statistics from credible sources: annotating conflicts with source attribution rather than arbitrarily selecting one value; requiring publication or collection dates to enable correct temporal interpretation</sub>

### 31. Correct answer: B

`D2 · Task 2.5`

- ✗ **A.** Searching for a test function name finds files by their contents, which misses any suite written with a different harness and catches non-test files that mention it.
- **✓** **B.** Both naming conventions are file path patterns, so two globs cover the whole population exactly.
- ✗ **C.** The scenario states some test files define their own helpers, so this misses them by construction.
- ✗ **D.** Reading every `.tsx` file in a monorepo to classify it works, at a cost far above matching two patterns.

**Why:** Finding files by name is a Glob question; Grep answers questions about contents.

<sub>Exam Guide: 2.5 Skills in: selecting Glob for finding files matching naming patterns (e.g., **/*.test.tsx)</sub>

### 32. Correct answer: C

`D2 · Task 2.5`

- ✗ **A.** Widening the anchor sometimes works and is worth a try, but it depends on the surrounding lines happening to differ, which seven repetitions in one file make unlikely.
- ✗ **B.** Making six wrong changes in order to make one right one leaves the file correct only if every revert lands.
- **✓** **C.** Reading the full contents and writing them back is the documented fallback precisely because it does not depend on a unique anchor existing.
- ✗ **D.** Appending a duplicate definition changes behavior through shadowing rather than editing the value that was meant to change.

**Why:** When Edit has no unique anchor, Read plus Write is the reliable path.

<sub>Exam Guide: 2.5 Knowledge of: when Edit fails due to non-unique text matches, using Read + Write as a fallback for reliable file modifications</sub>

### 33. Correct answer: C

`D2 · Task 2.5`

- ✗ **A.** Searching the original name finds only the callers that use it, and the wrappers exist precisely to expose other names.
- ✗ **B.** The callers are spread across the codebase; reading the `auth/` directory describes the source, not its consumers.
- **✓** **C.** Enumerating the aliases first turns one incomplete search into a complete set of searches.
- ✗ **D.** Import tracing finds the wrappers themselves, then stops one hop short of the code that calls them by their new names.

**Why:** Enumerate the aliases before searching, or the search is incomplete by construction.

<sub>Exam Guide: 2.5 Skills in: tracing function usage across wrapper modules by first identifying all exported names, then searching for each name across the codebase</sub>

### 34. Correct answer: D

`D2 · Task 2.5`

- ✗ **A.** Reading everything fits here, but it spends the whole window on a question about one flow and buries the answer in unrelated material.
- ✗ **B.** File names are a weak proxy for behavior, and backoff logic frequently lives in files named for something else.
- ✗ **C.** Delegation earns its overhead when the material will not fit; the scenario states that it does.
- **✓** **D.** Finding the entry points and following imports traces the actual path through the service, which is the thing being asked about.

**Why:** Trace the flow from its entry points instead of ingesting the whole service.

<sub>Exam Guide: 2.5 Skills in: building codebase understanding incrementally: starting with Grep to find entry points, then using Read to follow imports and trace flows, rather than reading all files upfront</sub>

### 35. Correct answer: A

`D3 · Task 3.1`

- **✓** **A.** Different behavior on identical code means different instructions are in play, and listing what each session loaded shows that directly.
- ✗ **B.** User-level files are one plausible source of the difference, but reading them by hand guesses at what is loaded instead of observing it.
- ✗ **C.** Both engineers are on the same commit, so the checkout is not the variable.
- ✗ **D.** Consolidation might mask the difference without ever revealing which layer caused it.

**Why:** Observe which configuration layers loaded before theorizing about which one differs.

<sub>Exam Guide: 3.1 Skills in: using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions</sub>

### 36. Correct answer: D

`D1 · Task 1.6`

- ✗ **A.** Attention dilutes across 40 files regardless of tier, and the criteria are already known to work at smaller scale.
- ✗ **B.** Diff size is a poor proxy for risk, and the approach abandons coverage rather than restoring it.
- ✗ **C.** A second read of the same oversized input reproduces the same middle-of-the-set gap.
- **✓** **D.** Local issues get a focused pass per file, and the interactions that produce contradictions get a pass of their own.

**Why:** Split by concern: local findings per file, interactions in their own pass.

<sub>Exam Guide: 1.6 Skills in: splitting large code reviews into per-file local analysis passes plus a separate cross-file integration pass to avoid attention dilution</sub>

### 37. Correct answer: C

`D1 · Task 1.1`

- ✗ **A.** This is the loop's control flow exactly as specified.
- ✗ **B.** Appending results is what lets the model reason about what it has already learned.
- **✓** **C.** Reading natural language to infer completion is the named anti-pattern; the signal is structural, not textual.
- ✗ **D.** Model-driven decision making at each step is what separates an agentic loop from a fixed sequence.

**Why:** The loop reads `stop_reason`, never the prose.

<sub>Exam Guide: 1.1 Skills in: avoiding anti-patterns such as parsing natural language signals to determine loop termination</sub>

### 38. Correct answer: A

`D1 · Task 1.5`

- **✓** **A.** Intercepting before execution is the only point at which the deletion can still be prevented rather than merely noted.
- ✗ **B.** A post-execution hook produces an audit trail of deletions that already happened, which is not what never-without-approval means.
- ✗ **C.** Forcing a tool shapes what the model calls next; it does not stop a call the model has already decided to make.
- ✗ **D.** Examples raise compliance and leave a residual failure rate, which a policy written as never does not tolerate.

**Why:** Never means the action has to be impossible, not merely discouraged.

<sub>Exam Guide: 1.5 Skills in: implementing tool call interception hooks that block policy-violating actions and redirect to alternative workflows; choosing hooks over prompt-based enforcement when business rules require guaranteed compliance</sub>

### 39. Correct answers: A, D

`D1 · Task 1.3`

- **✓** **A.** Tool restriction per subagent is what keeps each one inside its specialization.
- ✗ **B.** Subagent context is isolated, which is why anything it must know has to be written into its prompt.
- ✗ **C.** Each subagent definition carries its own system prompt; there is no inheritance to fall back on.
- **✓** **D.** Without `Task` the coordinator can reason about delegating and never actually delegate.

**Why:** Subagents inherit nothing: prompt, context, and tools are all declared per definition.

<sub>Exam Guide: 1.3 Knowledge of: the AgentDefinition configuration including descriptions, system prompts, and tool restrictions; that subagent context must be explicitly provided in the prompt</sub>

### 40. Correct answer: A

`D1 · Task 1.7`

- **✓** **A.** Forking gives two independent branches that share the analysis without either overwriting the other.
- ✗ **B.** Resuming the same session twice extends one line of work; the second run inherits whatever the first one did.
- ✗ **C.** Fresh sessions with an injected summary do isolate the branches, at the cost of re-deriving context the baseline already holds in full.
- ✗ **D.** Continuing serializes the comparison and lets the first approach's context shape the second.

**Why:** Divergent branches from one baseline is what forking is for.

<sub>Exam Guide: 1.7 Skills in: using fork_session to create parallel exploration branches (e.g., comparing two testing strategies or refactoring approaches from a shared codebase analysis)</sub>

### 41. Correct answer: C

`D3 · Task 3.6`

- ✗ **A.** There is no such environment variable, and parsing free-form output is what structured output exists to replace.
- ✗ **B.** There is no `--batch` flag on the CLI; batching is a property of the API, not of a Claude Code invocation.
- **✓** **C.** Non-interactive mode prevents the hang, and the two output flags together produce findings a later step can post without parsing prose.
- ✗ **D.** Running interactively in CI is what hangs the job waiting for input that never arrives.

**Why:** Non-interactive plus a declared schema is what makes CI output usable downstream.

<sub>Exam Guide: 3.6 Skills in: running Claude Code in CI with the -p flag; using --output-format json with --json-schema to produce machine-parseable structured findings for automated posting as inline PR comments</sub>

### 42. Correct answer: B

`D3 · Task 3.6`

- ✗ **A.** Clearing inside one session depends on the clearing being complete every time, which is a weaker guarantee than never sharing the context at all.
- **✓** **B.** Separate sessions make cross-contamination structurally impossible rather than something the pipeline has to remember to prevent.
- ✗ **C.** Fewer pull requests per run reduces how often the bleed happens without removing the cause.
- ✗ **D.** An instruction asks the model not to use context that is still sitting in front of it.

**Why:** Isolation by construction beats an instruction to ignore what is present.

<sub>Exam Guide: 3.6 Knowledge of: session context isolation: why the same Claude session that generated code is less effective at reviewing its own changes compared to an independent review instance</sub>

### 43. Correct answer: A

`D3 · Task 3.6`

- **✓** **A.** The agent repeats itself because each run starts blind; giving it the prior findings is what lets it tell new from already-said.
- ✗ **B.** Restricting to the latest diff hides issues that earlier commits introduced and later commits never touched.
- ✗ **C.** Post-hoc deduplication cleans the thread after the noise has already reached the developers.
- ✗ **D.** Reviewing once abandons the point of re-running, which is to catch what the new commits introduce.

**Why:** An agent cannot avoid repeating what it was never told it already said.

<sub>Exam Guide: 3.6 Skills in: including prior review findings in context when re-running reviews after new commits, instructing Claude to report only new or still-unaddressed issues to avoid duplicate comments</sub>

### 44. Correct answer: D

`D3 · Task 3.6`

- ✗ **A.** Fewer tests means proportionally fewer duplicates and proportionally fewer new ones too.
- ✗ **B.** Filtering afterwards spends the generation on work that is discarded and needs a reliable equivalence check.
- ✗ **C.** File-level coverage is too coarse: a covered file can still have uncovered branches, which is where the useful tests are.
- **✓** **D.** Once the agent can see what the suite already asserts, it stops proposing it.

**Why:** The agent duplicates what it cannot see.

<sub>Exam Guide: 3.6 Skills in: providing existing test files in context so test generation avoids suggesting duplicate scenarios already covered by the test suite</sub>

### 45. Correct answer: A

`D3 · Task 3.6`

- **✓** **A.** All three symptoms are missing project knowledge, and the always-loaded project file is where CI-invoked runs pick that knowledge up.
- ✗ **B.** Examples are strong for format and for ambiguous judgment calls, but they cannot tell the agent which fixtures this repository has.
- ✗ **C.** A stronger model still cannot know which paths this team considers worth covering.
- ✗ **D.** Review catches bad tests after they are written rather than causing better ones to be written.

**Why:** Quality complaints that are really missing context get fixed by supplying the context.

<sub>Exam Guide: 3.6 Skills in: documenting testing standards, valuable test criteria, and available fixtures in CLAUDE.md to improve test generation quality and reduce low-value test output</sub>

### 46. Correct answer: A

`D3 · Task 3.5`

- **✓** **A.** The suite already encodes the specification, so each failure is a precise, checkable instruction for the next iteration.
- ✗ **B.** Examples communicate a transformation when no executable specification exists; here one already does, in more detail.
- ✗ **C.** An interview surfaces requirements nobody has stated, and the edge cases are stated already.
- ✗ **D.** Plan mode weighs approaches, and the approach here is to satisfy an existing suite.

**Why:** When the specification is executable, failures are the feedback loop.

<sub>Exam Guide: 3.5 Knowledge of: test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement</sub>

### 47. Correct answer: D

`D4 · Task 4.5`

- ✗ **A.** The pre-merge check fails two batch preconditions at once: it blocks a person, and it needs tool calls inside a single request.
- ✗ **B.** Running the weekly audit synchronously is correct but pays full price for a job with three days of slack.
- ✗ **C.** This is the correct reasoning applied to the wrong workload, and the batch limitation on mid-request tool calls makes the pre-merge check unrunnable.
- **✓** **D.** The blocking, tool-calling workload goes synchronous; the latency-tolerant one takes the savings.

**Why:** Batch suits work nobody is waiting on and that needs no tools mid-request.

<sub>Exam Guide: 4.5 Knowledge of: batch processing is appropriate for non-blocking, latency-tolerant workloads and inappropriate for blocking workflows; the batch API does not support multi-turn tool calling within a single request</sub>

### 48. Correct answer: B

`D4 · Task 4.6`

- ✗ **A.** An instance without the generator's reasoning has no commitment to the decisions it is inspecting.
- **✓** **B.** The session that produced the code carries the reasoning that made it look right, and more deliberation inside that same context does not dislodge it.
- ✗ **C.** Splitting the passes addresses attention dilution, which is a different failure and a real one.
- ✗ **D.** Per-finding confidence does not catch defects by itself, but it routes maintainer attention usefully.

**Why:** Self-review inherits the reasoning that produced the defect.

<sub>Exam Guide: 4.6 Knowledge of: self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session; independent review instances are more effective than self-review instructions or extended thinking</sub>

### 49. Correct answer: C

`D4 · Task 4.1`

- ✗ **A.** Confidence is not the problem: the agent is highly confident about style observations that this team simply does not want.
- ✗ **B.** Self-critique helps where the gaps vary unpredictably; here the unwanted class is stable and nameable, so it can just be excluded.
- **✓** **C.** The noise falls in one identifiable category, and a criterion that names it removes the category without touching the findings developers act on.
- ✗ **D.** A numeric threshold is the same confidence filter in numeric clothing, and it drops accurate findings alongside unwanted ones.

**Why:** If you can name the category you do not want, name it instead of tuning a dial.

<sub>Exam Guide: 4.1 Knowledge of: how general instructions like 'be conservative' or 'only report high-confidence findings' fail to improve precision compared to specific categorical criteria</sub>

### 50. Correct answers: C, D

`D4 · Task 4.3`

- ✗ **A.** Asking for JSON in prose produces JSON most of the time, and a pipeline that blocks merges cannot run on most of the time.
- ✗ **B.** Keyword search over prose is the least reliable option here: a single hedged sentence flips the verdict.
- **✓** **C.** A schema attached to a tool makes the response structurally conformant instead of hopefully conformant.
- **✓** **D.** The CLI flags enforce the same guarantee at the invocation level, which is where a pipeline consumes it.

**Why:** A schema enforces the shape; a prompt only requests it.

<sub>Exam Guide: 4.3 Knowledge of: tool use with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output; 3.6 --output-format json and --json-schema for enforcing structured output in CI</sub>

### 51. Correct answer: B

`D4 · Task 4.3`

- ✗ **A.** Sharper descriptions would help the misplaced identifier, and they say nothing about arithmetic that does not add up.
- **✓** **B.** A schema constrains shape and type. Both symptoms are well-formed values that happen to be wrong, which is exactly the gap schema enforcement leaves open.
- ✗ **C.** Layout variation produces inconsistent extraction, not values landing confidently in the wrong field.
- ✗ **D.** Fabrication fills fields that have no source; here the source has both values and they are being placed and summed incorrectly.

**Why:** Valid structure and wrong content are independent, and only one of them has a schema.

<sub>Exam Guide: 4.3 Knowledge of: that strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)</sub>

### 52. Correct answer: A

`D4 · Task 4.3`

- **✓** **A.** A required field the document does not contain leaves the model one way to satisfy the schema, which is to invent a value. Completeness is bought with fabrication.
- ✗ **B.** Nullable plus an explicit instruction gives absence a way to be recorded truthfully.
- ✗ **C.** An "unclear" value separates a clause that is missing from one that is present but unreadable.
- ✗ **D.** Flagging nulls routes the genuine gaps to a human rather than papering over them.

**Why:** Required fields do not create information; they force it to be invented.

<sub>Exam Guide: 4.3 Skills in: designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields</sub>

### 53. Correct answer: D

`D4 · Task 4.3`

- ✗ **A.** Enumerating forty categories chases a long tail that is novel by definition, and the next unfamiliar product still has no home.
- ✗ **B.** A single null collapses two different situations: a product that is new and one that is unreadable.
- ✗ **C.** Free text abandons the enum's guarantee and moves the categorization problem downstream unchanged.
- **✓** **D.** The escape hatch carries its own detail, and ambiguity gets a value of its own rather than sharing one with novelty.

**Why:** Novel and unclear are different answers and need different values.

<sub>Exam Guide: 4.3 Skills in: adding enum values like 'unclear' for ambiguous cases and 'other' + detail fields for extensible categorization</sub>

### 54. Correct answer: C

`D4 · Task 4.3`

- ✗ **A.** `auto` permits a text answer, and a pipeline that requires a record on every document cannot accept prose.
- ✗ **B.** Forcing one type would be right if the type were known; here it misroutes every document that is not the common case.
- **✓** **C.** The call is guaranteed while selection stays with the component that has actually read the document.
- ✗ **D.** Deciding in code requires classifying the document first, which is the step the model is being asked to perform.

**Why:** `any` when a call is mandatory and the right schema is only knowable after reading.

<sub>Exam Guide: 4.3 Skills in: setting tool_choice: 'any' to guarantee structured output when multiple extraction schemas exist and the document type is unknown</sub>

### 55. Correct answer: B

`D4 · Task 4.4`

- ✗ **A.** Retry with feedback is genuinely the remedy for the date group, and applying it to the second group misreads a missing document as a formatting mistake.
- **✓** **B.** A format error is correctable from the same source; a value that is not in the input can only be satisfied by making one up.
- ✗ **C.** Retry with validation feedback is squarely aimed at semantic and format errors, not just transport failures.
- ✗ **D.** No amount of re-reading recovers a number that lives in an annex nobody supplied.

**Why:** Retry repairs shape; it cannot supply what the source never contained.

<sub>Exam Guide: 4.4 Knowledge of: the limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)</sub>

### 56. Correct answer: A

`D4 · Task 4.4`

- **✓** **A.** Capturing both numbers turns an invisible disagreement into a field comparison that code can evaluate.
- ✗ **B.** A self-assessed boolean asks the model to grade the arithmetic it just performed, in the same pass that produced the error.
- ✗ **C.** A numeric constraint governs the format of the total, never whether it matches the items above it.
- ✗ **D.** Reacting to ledger rejections is detection after the record has already left the pipeline.

**Why:** Extract both values and let the comparison be mechanical.

<sub>Exam Guide: 4.4 Skills in: designing self-correction validation flows: extracting 'calculated_total' alongside 'stated_total' to flag discrepancies</sub>

### 57. Correct answer: D

`D4 · Task 4.2`

- ✗ **A.** The schema is already satisfied by both outputs, so tightening it constrains a shape that is not what varies.
- ✗ **B.** Normalizing afterwards standardizes the output while leaving the model interpreting the two structures differently.
- ✗ **C.** Feedback needs a validation failure to fire on, and both styles pass validation.
- **✓** **D.** Two worked examples show what the same fields look like when the document is laid out each way, which is exactly the ambiguity in play.

**Why:** When interpretation varies with document structure, show the model both structures.

<sub>Exam Guide: 4.2 Skills in: using few-shot examples to demonstrate correct handling of varied document structures (inline citations vs bibliographies)</sub>

### 58. Correct answers: B, D

`D4 · Task 4.5`

- ✗ **A.** Splitting bounds the blast radius without improving the first-pass rate, so the same proportion still fails.
- **✓** **B.** Refining on a sample is what keeps a 50,000-document run from repeating this at four times the scale.
- ✗ **C.** Reprocessing 11,600 successful documents pays for work already done, and chunking documents that fit degrades them for no reason.
- **✓** **D.** The correlation id exists precisely so failures can be identified and reprocessed on their own.

**Why:** Reprocess only what failed, and fix the prompt before you scale it up.

<sub>Exam Guide: 4.5 Skills in: handling batch failures by resubmitting only failed documents identified by custom_id with appropriate modifications; using prompt refinement on a sample set before batch-processing large volumes</sub>

### 59. Correct answer: B

`D5 · Task 5.5`

- ✗ **A.** An aggregate over all types can clear a threshold while the one type being automated sits well below it.
- **✓** **B.** The decision is scoped to one document type, so the evidence has to be scoped the same way.
- ✗ **C.** Self-reported confidence is the model's own estimate, and it needs calibration against labeled data before it means anything.
- ✗ **D.** An overall change rate is another aggregate, and it inherits the same masking problem as the accuracy figure.

**Why:** Measure the segment you are automating, not the average that contains it.

<sub>Exam Guide: 5.5 Knowledge of: the risk that aggregate accuracy metrics may mask poor performance on specific document types or fields; analyzing accuracy by document type and field before reducing human review</sub>

### 60. Correct answer: B

`D5 · Task 5.5`

- ✗ **A.** A guess with a footnote is still a guess in the field, and downstream consumers read the field rather than the note.
- **✓** **B.** Ambiguity is recorded as itself, the record still satisfies the schema, and a human is directed to the case that needs judgment.
- ✗ **C.** An empty field pushes an interpretation decision onto a system with less context than the extractor had.
- ✗ **D.** Repetition against ambiguous wording produces a confident answer without producing a correct one.

**Why:** Say that it is unclear, and send the case to someone who can decide.

<sub>Exam Guide: 5.5 Skills in: routing extractions with low model confidence or ambiguous/contradictory source documents to human review, prioritizing limited reviewer capacity</sub>
