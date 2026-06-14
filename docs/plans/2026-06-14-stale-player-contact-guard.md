# Stale Player Contact Guard

status: completed

## Context

SpriteKit can deliver multiple contacts involving the same monster during one
physics step. A projectile contact removes the monster, but a queued player
contact can still reach `monsterDidCollideWithPlayer` and end the game even
though that monster is no longer active in the scene.

## Requirements

- Require both the monster and player to remain attached to the active scene
  before mutating player state or presenting game over.
- Preserve the existing game-over guard, loss transition, projectile scoring,
  and 20-hit win threshold.
- Extend the static baseline with an ordering contract that rejects a missing
  or late active-node guard.
- Keep project files, bundled assets, gameplay tuning, and workflow policy
  unchanged.

## Implementation

- Add an active-node guard at the start of the player collision handler after
  the existing game-over check.
- Update `scripts/check-baseline.py` to require the guard before player state
  mutation and node removal.
- Synchronize verification documentation after all local gates and hostile
  mutations complete.

## Verification

- Run the focused static baseline and all Make gates from the repository.
- Run the full gate through an absolute Makefile path from an external working
  directory.
- Compile the Python checker and validate shell, project, plist, XML, and
  workflow syntax where supported.
- Prove hostile mutations are rejected for the active-node predicate, guard
  ordering, checker discovery, plan status, and verification evidence.
- Audit the exact diff, generated artifacts, and intended files for secret
  patterns before committing.

## Work Completed

- Required both collision nodes to remain attached to the active scene before
  the player collision handler mutates state or presents the loss scene.
- Extended the static baseline with guard-presence and ordering assertions.
- Updated the README and changelog to describe the stale-contact boundary.

## Verification Completed

- All four Make gates passed from the checkout and reported that `xcodebuild` was unavailable,
  so this Linux host exercised the complete static baseline.
- The full gate passed from an external directory through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py`, shell syntax, plist, XML,
  project, and workflow parsing, and `git diff --check` passed.
- Five isolated hostile mutations were rejected: missing active-node guard,
  late guard ordering, missing plan discovery, stale plan status, and missing
  verification evidence.
- Exact intended-file generated-artifact and secret-pattern audits passed.
- Hosted macOS simulator compilation and code-scanning evidence is recorded
  separately after push; this plan claims only completed local evidence.
