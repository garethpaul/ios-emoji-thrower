# Background Scroll Position

status: completed

## Context

`moveBackground()` is the helper for scrolling background nodes. It reset every
background node to `0 - backgroundVelocity`, which would collapse the two-node
scrolling loop to one offset if the helper is enabled. The helper should move
each node relative to its current position.

## Objectives

- Subtract `backgroundVelocity` from each background node's current x-position.
- Preserve the existing wraparound behavior for nodes that move off screen.
- Add static baseline coverage for relative background scroll movement.
- Document the background scroll guard alongside the SpriteKit guardrails.

## Verification

- `make check`
- `git diff --check`
