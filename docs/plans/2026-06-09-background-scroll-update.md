# Background Scroll Update Loop

status: completed

## Context

The scene had a `moveBackground()` helper that advanced each background node
from its current position, but the per-frame `update(_:)` callback was not
calling it. The scroll behavior should be active during gameplay and stop after
game-over presentation starts.

## Completed Scope

- Called `moveBackground()` from `update(_:)`.
- Guarded the call with `!gameIsOver` so scrolling does not continue during
  scene transition.
- Extended the static baseline and docs so the per-frame background scroll path
  remains connected.

## Verification

- `make check`
- `git diff --check`
