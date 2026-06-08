# Changes

## 2026-06-08

- Removed launch and gameplay debug console logging while preserving in-game score updates.
- Disabled SpriteKit debug overlays in the main game view.
- Initialized visible score text before the first collision.
- Guarded projectile launches so non-forward taps do not normalize invalid vectors.
- Guarded physics contact node casts and restored player-hit handling.
- Added `make check` and a static SpriteKit baseline for plist/storyboard/asset metadata, bundled resources, Xcode project wiring, source inventory, and local-only gameplay guardrails.
- Documented the legacy Xcode project, SpriteKit resources, and static verification workflow.
