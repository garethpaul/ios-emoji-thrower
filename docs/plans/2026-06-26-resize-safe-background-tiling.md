# Resize-Safe Background Tiling

status: completed

## Context

The scrolling backgrounds changed each sprite's size independently during every
frame update. Initial x-positions still came from the texture width, and scene
resizes did not re-establish adjacency. Under `.resizeFill`, rotation or another
view-size change could therefore leave a gap or overlap between the two tiles.

## Design

- Collect exactly the two named background sprites and sort them by x-position.
- Reject non-finite or non-positive scene geometry before layout.
- Normalize the leading tile into the interval immediately behind or at the
  scene origin, preserving its current scroll phase.
- Size both sprites from `SKScene.size` and place the second exactly one scene
  width after the first.
- Apply the helper after initial node creation and from `didChangeSize(_:)`.
- Keep per-frame scrolling responsible only for movement and wraparound.

## Test First

The portable baseline first required a shared tiling helper, finite geometry,
phase normalization, initial and resize calls, exact adjacency, and removal of
per-frame resizing. The unchanged source failed this red-first contract.

## Verification Completed

- All four Make gates passed from the checkout.
- All four Make gates passed from `/tmp` through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- `sh -n scripts/run-projectile-math-tests.sh` passed.
- Seven isolated hostile mutations were rejected: removed initial layout, removed
  resize layout, removed x-order sorting, removed scene sizing, weakened exact
  adjacency, removed constant-time phase normalization, and restored per-frame
  resizing.
- `git diff --check` passed.
- Local `swiftc` and `xcodebuild` were unavailable; hosted macOS remains
  authoritative for executable Swift tests and the unsigned simulator build.

## Scope Boundaries

- No scroll speed, background asset, player, score, projectile, monster,
  collision, audio, transition, persistence, network, signing, or project
  metadata change.
- Existing monsters and projectiles are not repositioned during resize.
- Runtime rotation still benefits from manual simulator confirmation.

## Primary Sources

- Apple, `SKScene.didChangeSize(_:)`:
  https://developer.apple.com/documentation/spritekit/skscene/didchangesize%28_%3A%29
- Apple, `SKScene.size`:
  https://developer.apple.com/documentation/spritekit/skscene/size
