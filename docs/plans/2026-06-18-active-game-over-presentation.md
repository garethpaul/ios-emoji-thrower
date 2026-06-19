# Active Game-Over Presentation

status: completed

## Context

`presentGameOver` marks the scene terminal, cancels monster spawning, and clears
the physics contact delegate before optionally presenting the next scene. If a
late callback reaches a scene that is no longer the `SKView`'s active scene,
those side effects still occur even though no game-over transition can be
presented.

## Priority

Keep terminal scene mutation coupled to authoritative presentation ownership.
The project already applies the equivalent active-scene guard when restarting
from `GameOverScene`; the outgoing transition should fail closed at the same
boundary.

## Requirements

- R1. Game-over presentation must require a non-nil `SKView` whose active scene
  is the current `GameScene`.
- R2. Ownership validation must occur before setting `gameIsOver`, cancelling
  spawning, clearing the contact delegate, or creating the destination scene.
- R3. An already terminal scene must continue rejecting duplicate transitions.
- R4. Valid win and loss paths must preserve their existing transitions,
  scoring, collision guards, and scene size.
- R5. The presenter must report whether it accepted the transition so the
  ownership boundary remains directly testable and reviewable.
- R6. Portable static contracts must reject a missing, weakened, or late guard
  and incomplete plan or guidance evidence.

## Implementation Units

### U1. Guard terminal transition ownership

**File:** `EmojiThrower/GameScene.swift`

Return `Bool` from `presentGameOver`, require both a non-terminal state and
active `SKView` ownership in one guard, perform terminal mutations only after
that guard, and present through the validated view reference.

### U2. Portable regression contracts

**File:** `scripts/check-baseline.py`

Parse the presenter body and require the exact ownership predicate, ordering
before every terminal side effect, validated-view presentation, and accepted
or rejected return values.

### U3. Maintained evidence

**Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
and this plan.

Document active-scene game-over ownership while preserving the existing local
gameplay, no-network boundary, and historical secret-rotation warning.

## Test Scenarios

- An already terminal scene rejects another game-over transition.
- A detached scene rejects the transition before terminal state changes.
- A scene attached to a view but no longer active rejects the transition.
- The active scene performs terminal shutdown and presents the requested
  game-over scene exactly once.
- Existing projectile, collision, spawn, restart, and math contracts remain
  green.

## Scope Boundaries

- Do not change projectile motion, collision masks, scoring thresholds,
  spawning cadence, assets, audio, signing, dependencies, or project metadata.
- Do not retrieve, reproduce, rewrite, or resolve the historical secret alert;
  owner-side rotation or revocation remains required.
- Do not add a second test runner or claim local SpriteKit execution on Linux.

## Verification

- Run `make lint`, `make test`, `make build`, and `make check` from the checkout.
- Run the absolute-path Make gate from an external directory.
- Parse the checker, validate the Swift runner shell, and run `git diff --check`.
- Reject isolated mutations for the ownership predicate, guard ordering,
  validated view use, return contract, guidance, and completed plan evidence.
- Audit intended files for generated artifacts, protected metadata, and
  credential-shaped additions.

## Work Completed

- Guarded terminal presentation with active `SKView` scene ownership before
  every terminal side effect.
- Returned accepted or rejected transition status and presented through the
  validated view reference.
- Added portable ordering, guidance, and completed-evidence contracts without
  changing gameplay constants or project metadata.

## Verification Completed

- All four Make gates passed after the completed implementation.
- The absolute Makefile gate passed from an external directory.
- `python3 -m py_compile scripts/check-baseline.py` and
  `sh -n scripts/run-projectile-math-tests.sh` passed.
- Seven isolated hostile mutations were rejected for ownership, ordering,
  validated view use, return behavior, guidance, and plan evidence.
- `git diff --check` passed with generated-artifact, protected-metadata, and
  changed-line credential audits.
- Local `swiftc and xcodebuild were unavailable`; hosted macOS remains
  authoritative for Swift and SpriteKit builds.
