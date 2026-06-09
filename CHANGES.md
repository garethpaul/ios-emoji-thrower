# Changes

## 2026-06-08

- Removed launch and gameplay debug console logging while preserving in-game score updates.
- Disabled SpriteKit debug overlays in the main game view.
- Initialized visible score text before the first collision.
- Guarded projectile launches so non-forward taps do not normalize invalid vectors.
- Made vector normalization return zero for zero-length vectors.
- Guarded rounded image helper asset loading and rendered image output.
- Guarded physics contact node casts and restored player-hit handling.
- Added a guarded game-over presenter so win/loss contacts cannot trigger repeated transitions.
- Keyed the enemy spawn action and stopped it when game-over presentation starts.
- Added `make check` and a static SpriteKit baseline for plist/storyboard/asset metadata, bundled resources, Xcode project wiring, source inventory, and local-only gameplay guardrails.
- Documented the legacy Xcode project, SpriteKit resources, and static verification workflow.
