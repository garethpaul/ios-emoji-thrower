# Resize-Safe Persistent Layout

status: completed

## Context

The game presents `GameScene` with SpriteKit's `.resizeFill` scale mode and the
iPad metadata supports every interface orientation. SpriteKit therefore changes
the scene size when the presenting view changes size. The player and score were
positioned only during `didMove(to:)`, leaving both nodes at stale coordinates
after an iPad rotation or another view-size change.

Apple documents `didChangeSize(_:)` as the scene callback for adjusting node
positions after a size change, and documents `.resizeFill` as keeping scene and
view dimensions matched.

## Priority

Keep persistent gameplay controls and feedback inside the current visible scene
without changing projectile, collision, scoring, spawn, or transition behavior.

## Requirements

- R1. Initial player and score positions must derive from `SKScene.size`, not
  the presenting view's frame.
- R2. One layout helper must own both persistent-node positions.
- R3. `didMove(to:)` must apply that helper for initial presentation.
- R4. `didChangeSize(_:)` must call `super` and reapply that helper.
- R5. The player remains at 10 percent of scene width and half scene height.
- R6. The score remains horizontally centered and 40 points below the scene's
  top edge.
- R7. Portable contracts must reject missing, commented-out, weakened, or
  view-frame-based layout behavior.

## Implementation Units

### U1. Centralize persistent-node layout

**File:** `EmojiThrower/GameScene.swift`

Move player and score positioning into `layoutPersistentNodes()`, invoke it
after initial node setup, and invoke it from `didChangeSize(_:)`.

### U2. Portable regression contract

**File:** `scripts/check-baseline.py`

Strip block and line comments for this contract, then verify initial and resize
callbacks, exact scene-relative coordinates, and removal of view-frame layout.

### U3. Maintained evidence

**Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
and this plan.

Document the resize-safe layout invariant, runtime rotation check, verification
boundary, and timestamped change evidence.

## Test Scenarios

- Initial presentation places the player and score from the scene size.
- A scene resize re-centers the score against the new width and top edge.
- A scene resize moves the player to the same relative gameplay position.
- Commenting out either layout callback or coordinate assignment fails the
  portable baseline.
- Reintroducing `view.frame` layout fails the portable baseline.

## Scope Boundaries

- Do not change gameplay constants, score values, collision masks, spawn
  cadence, projectile motion, assets, audio, signing, or project metadata.
- Do not reposition in-flight projectiles or monsters during a resize.
- Do not add dependencies or a second test runner.
- Do not claim local SpriteKit runtime execution when Xcode is unavailable.

## Primary Sources

- Apple, `SKScene.didChangeSize(_:)`:
  https://developer.apple.com/documentation/spritekit/skscene/didchangesize%28_%3A%29
- Apple, `SKSceneScaleMode.resizeFill`:
  https://developer.apple.com/documentation/spritekit/skscenescalemode/resizefill
- Apple, `SKScene.size`:
  https://developer.apple.com/documentation/spritekit/skscene/size

## Verification

- Run `make lint`, `make test`, `make build`, and `make check`.
- Run the absolute-path Make gate from an external directory.
- Parse the checker and validate the Swift runner shell.
- Reject isolated hostile mutations for each callback, coordinate assignment,
  comment suppression, and view-frame regression.
- Run `git diff --check` and audit intended files for generated artifacts,
  protected metadata, and credential-shaped additions.

## Work Completed

- Centralized player and score positioning in `layoutPersistentNodes()`.
- Applied the shared layout during initial presentation and every scene-size
  change.
- Added a comment-aware portable contract and maintained documentation without
  changing gameplay constants or project metadata.

## Verification Completed

- All four Make gates passed from the checkout.
- The absolute Makefile `check` gate passed from `/tmp`.
- `python3 -m py_compile scripts/check-baseline.py`,
  `sh -n scripts/run-projectile-math-tests.sh`, and `git diff --check` passed.
- Eight isolated hostile mutations were rejected for the initial layout call,
  resize override, superclass callback, player coordinate, score coordinate,
  line-comment suppression, block-comment suppression, and view-frame
  regression.
- Generated-artifact, protected-metadata, and changed-line credential audits
  found no unintended additions.
- Local `swiftc` and `xcodebuild` were unavailable; hosted macOS remains
  authoritative for executable Swift tests and the unsigned simulator build.
