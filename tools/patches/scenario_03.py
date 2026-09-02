"""Scenario 3 rewrite: Multi-Agent Research System (items 21-30)."""

PATCH = {
    21: {
        "domain": "D1",
        "task": "1.2",
        "guide_anchor": "1.2 Skills in: designing coordinator agents that analyze query requirements and dynamically select which subagents to invoke rather than always routing through the full pipeline",
        "stem": (
            "The coordinator spawns the same five subagents for every query. Narrow questions come "
            "back with overlapping material, and broad ones leave whole areas uncovered. Each "
            "subagent completes its assignment successfully. What is the root cause?"
        ),
        "options": {
            "A": "The subagents cannot see each other's work, so overlap goes unnoticed.",
            "B": "The decomposition is fixed rather than derived from the query itself.",
            "C": "The synthesis step has no criteria for resolving overlapping claims.",
            "D": "Five full reports exceed what the coordinator can hold at synthesis.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Subagent isolation is by design, and the coordinator is the component meant to prevent overlap by partitioning scope before delegating.",
            "B": "One pipeline for every query is too much machinery for a narrow question and too little for a broad one, which is exactly the two symptoms reported.",
            "C": "Deduplicating at synthesis tidies the output after the redundant work has already been paid for, and it does nothing for the uncovered areas.",
            "D": "A capacity ceiling would truncate results, not produce coverage that is simultaneously duplicated and incomplete.",
        },
        "distractor_families": {
            "A": "describes the architecture, not the defect",
            "C": "band-aid downstream",
            "D": "wrong failure signature",
        },
        "why": "The coordinator should choose the decomposition per query, not run a fixed pipeline.",
    },
    22: {
        "domain": "D1",
        "task": "1.2",
        "guide_anchor": "1.2 Skills in: implementing iterative refinement loops where the coordinator evaluates synthesis output for gaps, re-delegates to search and analysis subagents with targeted queries, and re-invokes synthesis until coverage is sufficient",
        "stem": (
            "After synthesis, the report leaves two of the original sub-questions unanswered. The "
            "team wants the system to close those gaps itself rather than shipping an incomplete "
            "report. Which design fits?"
        ),
        "options": {
            "A": "Raise the number of subagents so more ground is covered on the first pass.",
            "B": "Have the synthesis subagent flag each gap so the reader knows what is missing.",
            "C": "Score coverage against the sub-questions, re-delegate, and re-synthesize.",
            "D": "Have each subagent verify its own coverage before it returns to the coordinator.",
        },
        "key": ["C"],
        "explanations": {
            "A": "More parallel work widens the first pass without ever checking whether the questions were answered.",
            "B": "Annotating the gaps is honest reporting and worth doing, but the team asked for the system to close them, not to describe them.",
            "C": "Evaluating the synthesis against the original sub-questions and re-delegating targeted queries is the loop that converges on coverage.",
            "D": "A subagent can confirm it finished its own assignment; it cannot know which sub-questions the report as a whole still misses.",
        },
        "distractor_families": {
            "A": "more capacity where a control loop is needed",
            "B": "reports the gap instead of closing it",
            "D": "verification at the wrong altitude",
        },
        "why": "Coverage is a property of the whole report, so only the coordinator can judge it.",
    },
    23: {
        "domain": "D1",
        "task": "1.3",
        "guide_anchor": "1.3 Skills in: spawning parallel subagents by emitting multiple Task tool calls in a single coordinator response rather than across separate turns",
        "stem": (
            "The coordinator needs four independent literature searches before drafting. It "
            "currently spawns them one per turn, each waiting for the previous to return, and "
            "latency is roughly four times what the team expected. What should change?"
        ),
        "options": {
            "A": "Build one composite search tool that runs the four searches internally.",
            "B": "Have the first subagent spawn the other three beneath it as children.",
            "C": "Emit the four `Task` calls within a single coordinator response.",
            "D": "Keep the sequence and narrow each subagent's scope to shorten it.",
        },
        "key": ["C"],
        "explanations": {
            "A": "A composite tool builds new infrastructure to obtain parallelism the coordinator can already express natively.",
            "B": "Nested spawning does run the work concurrently, but it moves three subagents outside the coordinator's view and breaks hub-and-spoke observability.",
            "C": "Multiple `Task` calls in one response start the four searches together while every result still returns to the coordinator.",
            "D": "Four shorter serial steps are still four serial steps, and the searches are independent.",
        },
        "distractor_families": {
            "A": "new infrastructure over native capability",
            "B": "correct outcome, loses observability",
            "D": "optimizes within the wrong structure",
        },
        "why": "Parallelism comes from one response carrying several calls, not from nesting agents.",
    },
    24: {
        "domain": "D1",
        "task": "1.3",
        "guide_anchor": "1.3 Knowledge of: the Task tool as the mechanism for spawning subagents, and the requirement that allowedTools must include Task for a coordinator to invoke subagents",
        "stem": (
            "The coordinator produces a written plan naming which subagents should run, then "
            "answers the question itself with no subagent executing. The subagent definitions are "
            "correct and their prompts have been reviewed. What is the most likely cause?"
        ),
        "options": {
            "A": "`Task` is absent from the coordinator's allowed tools, so it cannot spawn.",
            "B": "The system prompt frames delegation as guidance rather than as instruction.",
            "C": "The subagent descriptions do not make clear when each of them applies.",
            "D": "`maxTurns` is too low for the delegation round trip to complete in time.",
        },
        "key": ["A"],
        "explanations": {
            "A": "The coordinator reasons about delegation correctly and then has no mechanism to act, which is exactly what reasoning-but-not-executing looks like.",
            "B": "Softly worded delegation would produce inconsistent spawning across runs, not a plan that names the right subagents and then never invokes any.",
            "C": "Poor descriptions cause the wrong subagent to be chosen; here the coordinator names the right ones.",
            "D": "A turn ceiling truncates work in progress rather than preventing the first call from ever being emitted.",
        },
        "distractor_families": {
            "B": "prompt cause, wrong signature",
            "C": "selection problem, wrong symptom",
            "D": "configuration knob, wrong failure mode",
        },
        "why": "Naming the right subagent and never calling it points at the tool, not the prompt.",
    },
    25: {
        "domain": "D1",
        "task": "1.6",
        "guide_anchor": "1.6 Skills in: selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation",
        "negative": True,
        "stem": (
            "The coordinator must produce a comparative market report on three companies. Which "
            "step cannot run in parallel with the others?"
        ),
        "options": {
            "A": "Retrieving the last four quarterly filings for each of the three companies.",
            "B": "Searching recent news coverage for each of the three companies by name.",
            "C": "Collecting analyst ratings for the three from two subscription sources.",
            "D": "Writing the assessment that weighs the three companies against each other.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Filing retrieval is per company and depends on nothing else in the list.",
            "B": "News searches are independent per company and can be issued at once.",
            "C": "Rating collection touches two sources and no other step's output.",
            "D": "A comparison consumes all three companies' material, so it can only start once the gathering steps have returned.",
        },
        "distractor_families": {
            "A": "independent gathering step",
            "B": "independent gathering step",
            "C": "independent gathering step",
        },
        "why": "Gathering fans out; the step that consumes every branch has to wait.",
    },
    26: {
        "domain": "D2",
        "task": "2.1",
        "guide_anchor": "2.1 Skills in: renaming tools and updating descriptions to eliminate functional overlap (e.g., renaming analyze_content to extract_web_results with a web-specific description)",
        "stem": (
            "The coordinator exposes `analyze_content` for retrieved web pages and "
            "`analyze_document` for uploaded files. Each description is accurate about its own "
            "tool and neither is malformed. Traces show uploaded PDFs routed to `analyze_content` "
            "in 38% of cases, and both invoked on the same item. What is the most effective fix?"
        ),
        "options": {
            "A": "Expand `analyze_content`'s description until it excludes uploaded files.",
            "B": "Merge the two into one tool that branches internally on the input type.",
            "C": "Restrict `analyze_document` to the document analysis subagent's tool set.",
            "D": "Rename both and have each description say when the other one applies.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Adding exclusions to one side leaves the other still describing itself in terms that fit both, so the boundary is only half drawn.",
            "B": "Merging removes the confusion by removing the distinction, which costs the specificity that made two tools worth having.",
            "C": "Scoping stops one subagent from reaching the wrong tool, but the coordinator itself is the component doing the misrouting.",
            "D": "Names that do not compete, plus descriptions that each point at the other's territory, remove the ambiguity from both sides at once.",
        },
        "distractor_families": {
            "A": "one-sided fix for a two-sided overlap",
            "B": "collapses a useful distinction",
            "C": "right mechanism, wrong actor",
        },
        "why": "Overlap lives between two descriptions, so both have to change.",
    },
    27: {
        "domain": "D2",
        "task": "2.3",
        "guide_anchor": "2.3 Skills in: providing scoped cross-role tools for high-frequency needs (e.g., a verify_fact tool for the synthesis agent) while routing complex cases through the coordinator",
        "stem": (
            "The synthesis subagent has no search tools by design. Review shows that in 15% of "
            "reports it needed to confirm a single figure, and a small share of those cases "
            "require reconciling sources that contradict each other. What is the most effective "
            "change?"
        ),
        "options": {
            "A": "Give it the same full search tool set the research subagents already use.",
            "B": "Give it a scoped `verify_fact` tool and route contradictions to the coordinator.",
            "C": "Keep its tool set as it is and have the coordinator pre-verify every figure.",
            "D": "Move verification into the report generation step that runs after synthesis.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Handing a synthesis agent the full research kit is the over-broad access that leads agents to misuse tools outside their specialization.",
            "B": "A narrow tool covers the frequent simple need in place, while the harder judgment stays with the component that can see all the sources.",
            "C": "Pre-verifying every figure pays the cost on 100% of figures to serve the 15% that need it.",
            "D": "Verifying after synthesis means the claim has already been written into the report before anyone checks it.",
        },
        "distractor_families": {
            "A": "over-broad tool access",
            "C": "cost on everything for a minority need",
            "D": "verification after the commitment",
        },
        "why": "Scope the frequent simple case locally and escalate the rare hard one.",
    },
    28: {
        "domain": "D2",
        "task": "2.2",
        "guide_anchor": "2.2 Skills in: returning structured error metadata including errorCategory, isRetryable boolean, and human-readable descriptions; distinguishing between access failures and valid empty results",
        "select_instruction": "Select two",
        "stem": (
            "A document analysis subagent hits several failures in one run: a source times out and "
            "succeeds on retry, another returns a persistent authorization error, and a third "
            "returns zero matches. Which two responses follow the guidance?"
        ),
        "options": {
            "A": "Return an empty result for the authorization failure, since nothing came back.",
            "B": "Report the zero-match source as a valid empty result rather than as an error.",
            "C": "Return a uniform \"source unavailable\" message so all failures look alike.",
            "D": "Return `isError` with a category, a retryable flag, and a readable cause.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "Reporting a permission failure as an empty result silently converts a problem into an answer, and the coordinator never learns it needs credentials.",
            "B": "A successful query that matched nothing is information, not a fault, and labeling it an error would trigger pointless retries.",
            "C": "A uniform message is what prevents recovery: the coordinator cannot tell a timeout worth retrying from a permission wall that never will be.",
            "D": "Category, retryability, and a readable cause are exactly what let the coordinator choose between retrying, escalating, and moving on.",
        },
        "distractor_families": {
            "A": "silent suppression",
            "C": "generic error hiding the context",
        },
        "why": "An empty result is an answer; a failure needs enough structure to act on.",
    },
    29: {
        "domain": "D2",
        "task": "2.4",
        "guide_anchor": "2.4 Skills in: choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira), reserving custom servers for team-specific workflows",
        "stem": (
            "The team wants to connect a widely used issue tracker with a maintained community MCP "
            "server. A developer proposes writing their own instead, to keep full control. What "
            "do you tell them?"
        ),
        "options": {
            "A": "Write the custom server, since control over a central integration is worth it.",
            "B": "Write the custom server, because the tracker touches every team process.",
            "C": "Wrap the community server in a custom one to add team-specific behavior.",
            "D": "Use the community server and keep custom builds for team-specific work.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Control over a standard integration buys little and costs the ongoing maintenance of an API surface someone else already tracks.",
            "B": "How central the tracker is argues for a well-maintained integration, not for a bespoke one the team must keep current alone.",
            "C": "Wrapping is the right instinct once there is genuine team-specific behavior to add, but nothing in the scenario says there is any yet.",
            "D": "Standard integrations are where community servers are strongest, and custom effort is reserved for what only this team needs.",
        },
        "distractor_families": {
            "A": "control framed as value",
            "B": "importance framed as justification",
            "C": "premature abstraction",
        },
        "why": "Build custom where the workflow is yours, not where the integration is standard.",
    },
    30: {
        "domain": "D5",
        "task": "5.6",
        "guide_anchor": "5.6 Knowledge of: how to handle conflicting statistics from credible sources: annotating conflicts with source attribution rather than arbitrarily selecting one value; requiring publication or collection dates to enable correct temporal interpretation",
        "stem": (
            "Two sources report headcount for the same company: a regulatory filing dated March "
            "states 4,200, and a press article dated September states 3,850. Both sources are "
            "credible. The report must be defensible to the client. What should the agent do?"
        ),
        "options": {
            "A": "Report both figures with their sources and their collection dates attached.",
            "B": "Report the filing's figure, since regulatory filings outrank press coverage.",
            "C": "Report the September figure, since the later reading supersedes the earlier.",
            "D": "Report the average of the two, with a note describing the range observed.",
        },
        "key": ["A"],
        "explanations": {
            "A": "With both values dated and attributed, the reader can see whether this is a contradiction or a company that shrank over six months.",
            "B": "Ranking sources by type discards a later observation on the strength of a general rule about credibility.",
            "C": "Preferring the newer figure assumes the two are measuring the same moment, which is the very thing the dates would settle.",
            "D": "Averaging invents a number that neither source reported and that describes no point in time.",
        },
        "distractor_families": {
            "B": "arbitrary source ranking",
            "C": "assumes contradiction without checking dates",
            "D": "fabricates a value",
        },
        "why": "Dates decide whether two figures conflict or simply describe different moments.",
    },
}
