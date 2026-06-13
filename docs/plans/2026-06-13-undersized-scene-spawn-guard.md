# Undersized Scene Spawn Guard

status: planned

## Context

`addMonster()` builds a closed random Y range from half the monster height to
the scene height minus half the monster height. If the SpriteKit scene is
temporarily smaller than the sprite, that range is inverted and
`CGFloat.random(in:)` traps before the spawn can be skipped.

## Priority

Scene dimensions can be transient during presentation, resizing, previews, or
future tests. Enemy scheduling should tolerate an unusable layout frame without
crashing the local game loop.

## Requirements

- R1. Calculate monster spawn Y through one helper that returns an optional.
- R2. Reject non-finite scene or sprite heights, non-positive sprite height, and
  scenes shorter than the sprite before constructing a random range.
- R3. `addMonster()` must return before adding a node, physics, movement, or
  sound when no valid Y position exists.
- R4. Valid scenes must preserve the existing uniform closed-range placement.
- R5. Preserve game-over spawn guards, spawn action keys, speed range, physics,
  scoring, contacts, transitions, assets, and local-only behavior.
- R6. Add method-scoped static contracts and completed verification evidence.

## Implementation Units

### U1. Validate vertical spawn geometry

- **File:** `EmojiThrower/GameScene.swift`
- Add an optional spawn-Y helper and guard its result before node insertion.

### U2. Enforce crash-safe ordering

- **File:** `scripts/check-baseline.py`
- Require finite and positive inputs, ordered range validation, optional return,
  and guard-before-`addChild` placement.

### U3. Document the SpriteKit boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that undersized or invalid scenes skip enemy spawning.

## Scope Boundaries

- Do not change normal scene dimensions, monster assets, speed, cadence,
  collision masks, score thresholds, or game-over behavior.
- Do not add persistence, telemetry, networking, analytics, or a new test target.
- Do not claim interactive gameplay validation without Xcode.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- Parse plist, storyboard, workspace, project, and workflow metadata with all
  available local parsers.
- `git diff --check`
- Hostile mutations removing finite, positive, or ordered-range validation,
  optional failure, guard-before-add ordering, plan status, or verification
  evidence must be rejected.
