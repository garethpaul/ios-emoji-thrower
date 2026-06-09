# Collision Handler Game-Over Guard

status: completed

## Context

`didBegin(_:)` exits after game-over handling starts, but the collision handler
methods also mutate score and player state directly. Late or direct callbacks
should no-op at the handler boundary before changing game state.

## Objectives

- Guard projectile collision handling before score mutation.
- Guard player collision handling before player-state mutation.
- Keep win/loss presentation routed through the existing guarded presenter.
- Extend the static baseline so collision handler guards remain visible without
  Xcode.
- Document the handler-level guard alongside the existing SpriteKit guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
