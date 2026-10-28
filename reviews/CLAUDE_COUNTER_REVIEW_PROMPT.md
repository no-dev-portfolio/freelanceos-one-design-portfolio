# Claude Code independent counter-review — second pass

Precondition: a **real** Codex review exists in `reviews/codex/REVIEW.md` and state `codex_complete`. Otherwise STOP and report blocker. Follow `CLAUDE.md` and common agreement. DESIGN ONLY.

PHASE A (independent): inspect original baseline revision and specifications; write your own failure cases and design objections before consulting Codex's judgments. Preserve these initial findings in the final review. If unable to review blind, disclose why.
PHASE B (adversarial): read Codex's actual review and its proposed design changes. For each major finding: CONFIRM / DISPUTE / PARTIAL, grounded in exact file/section, tests, and credible failure paths. Search specifically for flaws introduced by the Codex changes. Identify missed critical risks, scope creep, UX burden and unverifiable assumptions.
PHASE C (reconcile): propose prioritized corrections, acceptance tests and PoCs, plus the decisions requiring human approval. Do not approve your own changes; do not quietly implement features. Write `reviews/claude/COUNTER_REVIEW.md` using the template, update issue register with traceability, and report structural check output.
Do not impersonate Codex, do not claim you executed tests you did not run.
