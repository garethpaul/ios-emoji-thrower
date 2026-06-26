# Resize-Safe Game Over

status: completed

## Goal

Keep result-screen layout and delayed restart geometry aligned with the current
game-over scene size.

## Work

- Promote the result label to scene-owned state.
- Center it during initialization and every `didChangeSize(_:)` callback.
- Read `self.size` when the delayed restart action fires.
- Add source, guidance, hostile mutation, and plan contracts.

## Verification

- The red-first checker failed on the local label and captured restart size.
- Six hostile game-over resize mutations covered scene-owned label state,
  relayout, current-center geometry, current-size restart, guidance, and plan evidence.
- All four Make aliases and repository-root and external-directory `make check` passed.
- Python compilation, shell syntax, and `git diff --check` passed.
- Local `swiftc` and `xcodebuild` were unavailable.

Implementation head `52f900b4c7cfb73e80cc7e8cdbbd1c3ee5f3fc76` passed hosted
push baseline `28269675521`, pull-request baseline `28269677372`, and CodeQL
run `28269677126`, including Swift analysis. Codex review stopped before
analysis with OpenAI HTTP 401; immutable manual review found no actionable
issues. The final evidence-only head must repeat hosted validation.

## Scope

No gameplay scoring, collision, audio, asset, transition, network, persistence,
project setting, or scene-ownership behavior changed.
