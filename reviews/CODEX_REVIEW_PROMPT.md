# Codex primary design review — instructions

ROLE: lead architecture/design reviewer, first pass. Read `AGENTS.md`, `handoff/START_HERE.md`, entire `docs/` and UI prototype. Design-only; do not build the app. Your job is to actively attempt to invalidate the design, not praise it.

1. Analyze concept, target users and genuine value; challenge overengineering and scope.
2. Walk through each UI journey: first run, job initiation, knowledge search, correction, approval, sync conflict, and failure recovery. Include accessibility, mobile, privacy and progress feedback.
3. Inspect knowledge data authority, Markdown concurrent edits, revision/hash consistency, stale index, delete propagation and prompt injection.
4. Analyze workflow state transitions, idempotency, approval TOCTOU, tool allowlists, data classification, audit, local/cloud model boundaries, costs and offline behavior.
5. Trace every requirement to design and verification; propose missing test cases, edge cases and destructive tests.
6. Produce issue-prioritized findings with exact references, falsifiable assertions, competing solutions, new risks, and a PoC plan; log disagreements and decisions explicitly.
7. Record the **real** review in `reviews/codex/REVIEW.md` using `reviews/CODEX_REVIEW_TEMPLATE.md`. Update existing issues and ADR proposals where justified; do not quietly change high-impact decisions. Run integrity script, report command output.
8. Stop with unresolved critical issues clearly identified. Never mark Claude counter-review done.
