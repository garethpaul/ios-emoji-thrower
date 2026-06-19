# Finite Projectile Touch Vector Guard

status: completed

## Context

Projectile launching rejects non-forward touches, but a NaN horizontal offset
makes the `<= 0` comparison false. Non-finite or overflow-length touch vectors
can then propagate through normalization into SpriteKit positions and actions
before the projectile is removed.

## Requirements

- R1. Reject non-finite horizontal and vertical touch offsets.
- R2. Reject non-forward offsets and zero, non-finite, or overflowed vector
  lengths before normalization.
- R3. Return a finite normalized direction only for valid forward vectors.
- R4. Validate direction before projectile physics, node insertion, movement,
  or sound effects.
- R5. Preserve ordinary forward-shot behavior, game-over guards, collision
  handling, and local-only gameplay.

## Scope Boundaries

- Do not change projectile speed, distance, image, physics categories, sound, or
  collision scoring.
- Do not add network, persistence, analytics, authentication, or remote assets.
- Do not modify project files, bundled resources, or hosted workflow policy.
- Local Linux validation must remain truthful about unavailable `xcodebuild`.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- plist, XML, and workflow YAML parsing
- `git diff --check`
- Hostile mutations must reject missing component or length finiteness checks,
  acceptance of non-forward vectors, direction validation after node insertion,
  stale plan status, and missing verification evidence.

## Work Completed

- Added a pure optional direction helper that rejects non-finite components,
  non-forward offsets, and zero, non-finite, or overflowed lengths.
- Required the normalized direction itself to remain finite before returning it.
- Moved direction validation before projectile physics, node insertion,
  movement, and sound effects.
- Documented the finite touch-vector boundary without changing gameplay tuning,
  resources, project files, or workflow policy.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py`, plist, XML, and workflow YAML parsing,
  and `git diff --check` passed.
- Seven isolated hostile mutations were rejected: removed horizontal component
  finiteness, removed vertical component finiteness, removed length finiteness,
  accepted non-forward vectors, validated after node insertion, stale plan
  status, and missing verification evidence.
- Exact-base comparison confirmed project files, bundled resources, and hosted
  workflow configuration remained unchanged.
- Intended-file generated-artifact, secret-pattern, and forbidden data-flow
  scans passed.
- Hosted macOS simulator compilation and code-scanning evidence is recorded
  separately after push; this plan claims only completed local static evidence.
