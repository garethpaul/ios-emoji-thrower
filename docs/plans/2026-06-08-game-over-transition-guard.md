# Game-Over Transition Guard Plan

status: completed

## Context

`GameScene` presents a game-over scene from both score and player-contact paths. SpriteKit can still deliver touches or contact callbacks while a transition is beginning, so scene presentation should be guarded in one place.

## Objectives

- Add a scene-level game-over state flag.
- Route win and loss transitions through one guarded presenter.
- Ignore touches and contacts after game-over handling begins.
- Extend the static baseline so repeated transition guards remain visible without Xcode.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
