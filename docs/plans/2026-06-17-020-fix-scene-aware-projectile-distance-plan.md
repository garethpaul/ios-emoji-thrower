---
title: Scene-Aware Projectile Exit Distance
type: fix
date: 2026-06-17
---

# Scene-Aware Projectile Exit Distance

## Summary

Replace the fixed 1000-point projectile travel scalar with validated geometry
derived from the scene and projectile sizes. Extend the portable Swift harness
so wide-scene behavior and invalid geometry are executed in CI.

## Problem Frame

`GameScene` claims every projectile travels far enough to leave the screen, but
the destination is always 1000 points from the player. A wide landscape scene
can keep that destination visibly inside its bounds, causing the projectile to
disappear when its action completes before it reaches an edge.

## Requirements

- R1. Derive projectile travel distance from finite, positive scene dimensions
  and finite, non-negative projectile dimensions.
- R2. Return a distance greater than the scene diagonal by enough margin for
  the projectile node to clear the scene boundary from any in-bounds origin.
- R3. Reject invalid geometry before adding the projectile node, scheduling its
  action, or playing the launch sound.
- R4. Execute portable Swift cases for wide and tall scenes, projectile margin,
  zero or negative dimensions, non-finite dimensions, and overflow.
- R5. Preserve forward-only finite direction validation, collision masks,
  action duration, audio behavior for valid launches, and SpriteKit metadata.
- R6. Keep the canonical checker and project documentation aligned with the
  scene-aware projectile distance contract.

## Key Technical Decisions

- **Use the scene diagonal as the base distance:** the diagonal bounds the
  longest in-scene ray from any in-bounds origin without coupling portable math
  to SpriteKit frame APIs.
- **Add the projectile's largest dimension as clearance:** this moves the whole
  node beyond the boundary instead of stopping when only its center reaches it.
- **Keep geometry in `ProjectileMath`:** Foundation-only math remains executable
  through the existing `swiftc` harness and is shared directly by `GameScene`.
- **Fail closed on invalid geometry:** malformed or overflowing sizes suppress
  the launch instead of creating a node with a non-finite destination.

## Implementation Units

### U1. Add validated exit-distance math

- **Goal:** Calculate a finite scene-aware travel distance with projectile
  clearance and reject invalid or overflowing sizes.
- **Files:** `EmojiThrower/ProjectileMath.swift`
- **Patterns:** Follow the existing optional-return finite guard used by
  projectile direction normalization.
- **Test Scenarios:** Wide landscape, tall portrait, margin increase, zero,
  negative, NaN, infinity, and overflowing dimensions.
- **Covers:** R1, R2, R4.

### U2. Delegate launch distance to the shared helper

- **Goal:** Require a valid exit distance before adding or animating a
  projectile, then replace the fixed scalar with that distance.
- **Files:** `EmojiThrower/GameScene.swift`
- **Patterns:** Preserve the current direction guard and keep helper source in
  the application target.
- **Verification:** Static source ordering proves geometry validation occurs
  before `addChild`, movement, and sound playback.
- **Covers:** R3, R5.

### U3. Extend executable and static contracts

- **Goal:** Run the new geometry cases through the existing portable harness and
  document the runtime boundary.
- **Files:** `Tests/ProjectileMathTests/main.swift`, `scripts/check-baseline.py`,
  `README.md`, `CHANGES.md`
- **Patterns:** Reuse `scripts/run-projectile-math-tests.sh` and the canonical
  `make check` path without adding a second test runner.
- **Verification:** Root and external-directory Make gates plus isolated
  mutations of the math, scene delegation, tests, docs, and checker contract.
- **Covers:** R4, R6.

## Risks And Mitigations

- Large finite dimensions can overflow during diagonal calculation; require a
  finite positive result before returning a distance.
- Linux cannot exercise SpriteKit node movement; use the shared Foundation-only
  helper locally and require hosted macOS validation for the application build.
- The repository has a historical secret-scanning alert; do not inspect or
  reproduce its value, and keep this change free of credentials.

## Scope Boundaries

- Do not change projectile direction, speed, collision behavior, scoring,
  spawning, scene transitions, assets, sounds, signing, or dependencies.
- Do not rewrite history or resolve the historical secret alert without owner
  confirmation that the exposed credential was revoked or rotated.
- Do not introduce a new test framework or duplicate the existing Swift harness.

## Verification

- Compile and run the portable projectile-math harness.
- Run `make lint`, `make test`, `make build`, and `make check` from the checkout.
- Run the absolute-path Make gate from an external directory.
- Parse Python and project metadata, then run `git diff --check`.
- Reject isolated mutations covering the distance formula, invalid geometry,
  launch ordering, executable cases, documentation, and checker enforcement.
- Audit intended files for generated artifacts and credential-shaped content.
