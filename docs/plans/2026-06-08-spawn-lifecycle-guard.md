# Spawn Lifecycle Guard Plan

status: completed

## Context

The game starts a repeating SpriteKit action that adds enemies while play is
active. Once game-over presentation starts, that scheduler should stop and the
spawn function should also exit early if it is invoked after the game-over flag
is set.

## Objectives

- Run enemy spawning under a stable SpriteKit action key.
- Remove the spawn action when game-over presentation starts.
- Guard the spawn function before creating new sprites after game over.
- Extend the static baseline so the lifecycle guard remains visible without
  Xcode.
- Document the spawn lifecycle expectation alongside the existing game-over
  transition guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
