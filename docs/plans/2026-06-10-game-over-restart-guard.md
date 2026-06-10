# Game-Over Restart Guard

status: completed

## Context

`GameOverScene` schedules a delayed restart after showing win or loss text. The
restart closure created and presented a new `GameScene` directly, without first
confirming that the game-over scene was still the active SpriteKit scene. It
also skipped the `resizeFill` scale mode used by the initial game launch path.

## Completed Scope

- Added a `restartGame` helper that refuses delayed restarts unless the current
  `SKView` is still presenting the game-over scene.
- Applied `.resizeFill` to restarted game scenes so restart presentation matches
  initial game launch behavior.
- Routed the delayed restart action through the helper.
- Extended the static baseline and docs so game-over restart behavior remains
  guarded without adding networking, persistence, analytics, or account flows.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
