"""Scenario 6 rewrite: Structured Data Extraction (items 51-60)."""

PATCH = {
    51: {
        "domain": "D4",
        "task": "4.3",
        "guide_anchor": "4.3 Knowledge of: that strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)",
        "stem": (
            "The pipeline uses tool use with a strict JSON schema, and the team confirms that "
            "schema violations and JSON syntax errors no longer occur. Operations reports that 8% "
            "of records carry the purchase order number in the invoice number field, and 5% have "
            "line items that do not sum to the declared total. What is the most likely cause?"
        ),
        "options": {
            "A": "Field descriptions do not distinguish the two identifier fields clearly.",
            "B": "The values are semantically wrong, which a schema has no way to detect.",
            "C": "Source layouts vary, so few-shot examples are needed for consistency.",
            "D": "The model is fabricating values for fields the documents do not contain.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Sharper descriptions would help the misplaced identifier, and they say nothing about arithmetic that does not add up.",
            "B": "A schema constrains shape and type. Both symptoms are well-formed values that happen to be wrong, which is exactly the gap schema enforcement leaves open.",
            "C": "Layout variation produces inconsistent extraction, not values landing confidently in the wrong field.",
            "D": "Fabrication fills fields that have no source; here the source has both values and they are being placed and summed incorrectly.",
        },
        "distractor_families": {
            "A": "explains half the symptom",
            "C": "plausible cause, wrong signature",
            "D": "different failure mode",
        },
        "why": "Valid structure and wrong content are independent, and only one of them has a schema.",
    },
    52: {
        "domain": "D4",
        "task": "4.3",
        "guide_anchor": "4.3 Skills in: designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields",
        "negative": True,
        "stem": (
            "A contract schema includes `governing_law`, `renewal_term`, and `liability_cap`, and "
            "30% of contracts genuinely omit at least one of the three. Which approach is least "
            "appropriate?"
        ),
        "options": {
            "A": "Keeping all three required so every record arrives downstream complete.",
            "B": "Declaring them nullable and instructing a null when the clause is absent.",
            "C": "Adding an \"unclear\" value for clauses present but ambiguously worded.",
            "D": "Flagging records that contain nulls so a reviewer confirms the omission.",
        },
        "key": ["A"],
        "explanations": {
            "A": "A required field the document does not contain leaves the model one way to satisfy the schema, which is to invent a value. Completeness is bought with fabrication.",
            "B": "Nullable plus an explicit instruction gives absence a way to be recorded truthfully.",
            "C": "An \"unclear\" value separates a clause that is missing from one that is present but unreadable.",
            "D": "Flagging nulls routes the genuine gaps to a human rather than papering over them.",
        },
        "distractor_families": {
            "B": "correct design offered as if wrong",
            "C": "correct design offered as if wrong",
            "D": "correct design offered as if wrong",
        },
        "why": "Required fields do not create information; they force it to be invented.",
    },
    53: {
        "domain": "D4",
        "task": "4.3",
        "guide_anchor": "4.3 Skills in: adding enum values like 'unclear' for ambiguous cases and 'other' + detail fields for extensible categorization",
        "stem": (
            "A product schema uses an enum of eight categories that covers 94% of listings. The "
            "remainder are genuinely novel products, and a separate handful of listings are worded "
            "too vaguely to categorize at all. What should the schema add?"
        ),
        "options": {
            "A": "Forty categories in place of eight, so novel products find a match.",
            "B": "A nullable category field that the model leaves empty when unsure.",
            "C": "A free-text category with a mapping table maintained downstream.",
            "D": "An \"other\" value with a detail field, plus an \"unclear\" value.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Enumerating forty categories chases a long tail that is novel by definition, and the next unfamiliar product still has no home.",
            "B": "A single null collapses two different situations: a product that is new and one that is unreadable.",
            "C": "Free text abandons the enum's guarantee and moves the categorization problem downstream unchanged.",
            "D": "The escape hatch carries its own detail, and ambiguity gets a value of its own rather than sharing one with novelty.",
        },
        "distractor_families": {
            "A": "enumerating an open set",
            "B": "collapses two distinct cases",
            "C": "moves the problem downstream",
        },
        "why": "Novel and unclear are different answers and need different values.",
    },
    54: {
        "domain": "D4",
        "task": "4.3",
        "guide_anchor": "4.3 Skills in: setting tool_choice: 'any' to guarantee structured output when multiple extraction schemas exist and the document type is unknown",
        "stem": (
            "Three document types arrive through the same pipeline, each with its own extraction "
            "tool and schema. The type is not known until the document has been read, and every "
            "document must produce a structured record. Which `tool_choice` setting fits?"
        ),
        "options": {
            "A": "`auto`, so the model can decide whether extraction is needed at all.",
            "B": "Forced selection on the tool for the most common document type.",
            "C": "`any`, so a tool must be called and the model picks the schema.",
            "D": "No tool at all, deciding the schema in code before making the call.",
        },
        "key": ["C"],
        "explanations": {
            "A": "`auto` permits a text answer, and a pipeline that requires a record on every document cannot accept prose.",
            "B": "Forcing one type would be right if the type were known; here it misroutes every document that is not the common case.",
            "C": "The call is guaranteed while selection stays with the component that has actually read the document.",
            "D": "Deciding in code requires classifying the document first, which is the step the model is being asked to perform.",
        },
        "distractor_families": {
            "A": "permits the outcome the pipeline forbids",
            "B": "right mechanism, unknown precondition",
            "D": "assumes the classification already exists",
        },
        "why": "`any` when a call is mandatory and the right schema is only knowable after reading.",
    },
    55: {
        "domain": "D4",
        "task": "4.4",
        "guide_anchor": "4.4 Knowledge of: the limits of retry: retries are ineffective when the required information is simply absent from the source document (vs format or structural errors)",
        "stem": (
            "Validation fails on two groups. In one, `effective_date` returns as `03/04/2026` "
            "where ISO 8601 is expected. In the other, `counterparty_registration` is empty "
            "because it appears only in an annex that was never part of the input. The team raises "
            "the retry limit with validation feedback attached. What will that achieve?"
        ),
        "options": {
            "A": "It resolves both groups, since retry with feedback is the standard remedy.",
            "B": "It fixes the dates and pushes the model to invent registration numbers.",
            "C": "It resolves neither, since retries only address transient API failures.",
            "D": "It fixes the registration group by forcing a closer read of the source.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Retry with feedback is genuinely the remedy for the date group, and applying it to the second group misreads a missing document as a formatting mistake.",
            "B": "A format error is correctable from the same source; a value that is not in the input can only be satisfied by making one up.",
            "C": "Retry with validation feedback is squarely aimed at semantic and format errors, not just transport failures.",
            "D": "No amount of re-reading recovers a number that lives in an annex nobody supplied.",
        },
        "distractor_families": {
            "A": "correct for one group, generalized to both",
            "C": "understates what retry is for",
            "D": "assumes information that is absent",
        },
        "why": "Retry repairs shape; it cannot supply what the source never contained.",
    },
    56: {
        "domain": "D4",
        "task": "4.4",
        "guide_anchor": "4.4 Skills in: designing self-correction validation flows: extracting 'calculated_total' alongside 'stated_total' to flag discrepancies",
        "stem": (
            "Discrepancies between a document's stated total and its itemized amounts must surface "
            "before records reach the ledger. The extraction itself is schema-compliant. Which "
            "design does that?"
        ),
        "options": {
            "A": "Extract a calculated total beside the stated one and flag any difference.",
            "B": "Add a required boolean the model sets after checking its own arithmetic.",
            "C": "Restrict the total field in the schema to two-decimal numeric values.",
            "D": "Retry the extraction whenever the ledger rejects an incoming record.",
        },
        "key": ["A"],
        "explanations": {
            "A": "Capturing both numbers turns an invisible disagreement into a field comparison that code can evaluate.",
            "B": "A self-assessed boolean asks the model to grade the arithmetic it just performed, in the same pass that produced the error.",
            "C": "A numeric constraint governs the format of the total, never whether it matches the items above it.",
            "D": "Reacting to ledger rejections is detection after the record has already left the pipeline.",
        },
        "distractor_families": {
            "B": "self-assessment as verification",
            "C": "format constraint for a semantic problem",
            "D": "detection after the fact",
        },
        "why": "Extract both values and let the comparison be mechanical.",
    },
    57: {
        "domain": "D4",
        "task": "4.2",
        "guide_anchor": "4.2 Skills in: using few-shot examples to demonstrate correct handling of varied document structures (inline citations vs bibliographies)",
        "stem": (
            "Research papers cite sources in two ways: inline in the body, or gathered in a "
            "bibliography. Extraction of the citation fields is consistent within each style but "
            "differs between them, and the schema is satisfied in both cases. What addresses this?"
        ),
        "options": {
            "A": "Tighten the citation field definitions in the extraction schema.",
            "B": "Post-process the extracted citations into one common shape.",
            "C": "Retry extraction with validation feedback when the style differs.",
            "D": "Give few-shot examples of correct extraction from both structures.",
        },
        "key": ["D"],
        "explanations": {
            "A": "The schema is already satisfied by both outputs, so tightening it constrains a shape that is not what varies.",
            "B": "Normalizing afterwards standardizes the output while leaving the model interpreting the two structures differently.",
            "C": "Feedback needs a validation failure to fire on, and both styles pass validation.",
            "D": "Two worked examples show what the same fields look like when the document is laid out each way, which is exactly the ambiguity in play.",
        },
        "distractor_families": {
            "A": "constrains the shape, not the interpretation",
            "B": "band-aid downstream",
            "C": "requires a failure that never occurs",
        },
        "why": "When interpretation varies with document structure, show the model both structures.",
    },
    58: {
        "domain": "D4",
        "task": "4.5",
        "guide_anchor": "4.5 Skills in: handling batch failures by resubmitting only failed documents identified by custom_id with appropriate modifications; using prompt refinement on a sample set before batch-processing large volumes",
        "select_instruction": "Select two",
        "stem": (
            "A batch of 12,000 documents returns with 400 failures caused by exceeding the context "
            "limit. A 50,000-document run is planned for next month. Which two actions are "
            "appropriate?"
        ),
        "options": {
            "A": "Resubmit the whole batch with chunking applied to every document uniformly.",
            "B": "Refine the prompt against a sample set before the 50,000-document run.",
            "C": "Split the coming run into five batches so that failures stay contained.",
            "D": "Resubmit only the failed documents, keyed by `custom_id`, once chunked.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "Reprocessing 11,600 successful documents pays for work already done, and chunking documents that fit degrades them for no reason.",
            "B": "Refining on a sample is what keeps a 50,000-document run from repeating this at four times the scale.",
            "C": "Splitting bounds the blast radius without improving the first-pass rate, so the same proportion still fails.",
            "D": "The correlation id exists precisely so failures can be identified and reprocessed on their own.",
        },
        "distractor_families": {
            "A": "reprocesses successful work",
            "C": "contains the symptom, not the cause",
        },
        "why": "Reprocess only what failed, and fix the prompt before you scale it up.",
    },
    59: {
        "domain": "D5",
        "task": "5.5",
        "guide_anchor": "5.5 Knowledge of: the risk that aggregate accuracy metrics may mask poor performance on specific document types or fields; analyzing accuracy by document type and field before reducing human review",
        "stem": (
            "Before removing human review for one document type, the team measures 96% field-level "
            "accuracy across all document types combined, which clears the agreed threshold. What "
            "should govern the decision?"
        ),
        "options": {
            "A": "The 96% figure, since it already exceeds the threshold the team agreed.",
            "B": "Accuracy measured on that document type alone, which the aggregate hides.",
            "C": "The agent's self-reported confidence on that type over a sampling window.",
            "D": "The overall rate at which reviewers currently change the agent's output.",
        },
        "key": ["B"],
        "explanations": {
            "A": "An aggregate over all types can clear a threshold while the one type being automated sits well below it.",
            "B": "The decision is scoped to one document type, so the evidence has to be scoped the same way.",
            "C": "Self-reported confidence is the model's own estimate, and it needs calibration against labeled data before it means anything.",
            "D": "An overall change rate is another aggregate, and it inherits the same masking problem as the accuracy figure.",
        },
        "distractor_families": {
            "A": "aggregate masking a segment",
            "C": "uncalibrated self-report",
            "D": "a different aggregate, same flaw",
        },
        "why": "Measure the segment you are automating, not the average that contains it.",
    },
    60: {
        "domain": "D5",
        "task": "5.5",
        "guide_anchor": "5.5 Skills in: routing extractions with low model confidence or ambiguous/contradictory source documents to human review, prioritizing limited reviewer capacity",
        "stem": (
            "An extraction cannot determine a value because the source wording is genuinely "
            "ambiguous, and the downstream system expects the field to be populated. What should "
            "the pipeline do?"
        ),
        "options": {
            "A": "Return the most likely reading, with a note recording the ambiguity.",
            "B": "Return the designated \"unclear\" value and flag the record for review.",
            "C": "Leave the field empty and let the downstream system decide what to do.",
            "D": "Retry the extraction until it produces a determinate, populated value.",
        },
        "key": ["B"],
        "explanations": {
            "A": "A guess with a footnote is still a guess in the field, and downstream consumers read the field rather than the note.",
            "B": "Ambiguity is recorded as itself, the record still satisfies the schema, and a human is directed to the case that needs judgment.",
            "C": "An empty field pushes an interpretation decision onto a system with less context than the extractor had.",
            "D": "Repetition against ambiguous wording produces a confident answer without producing a correct one.",
        },
        "distractor_families": {
            "A": "guess with a disclaimer",
            "C": "defers the judgment downstream",
            "D": "repetition as resolution",
        },
        "why": "Say that it is unclear, and send the case to someone who can decide.",
    },
}
