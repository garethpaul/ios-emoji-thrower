# Changes

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static SpriteKit baseline.
- Cleared the physics contact delegate before game-over scene transitions so
  late SpriteKit contacts do not keep dispatching into the old scene.

## 2026-06-08

- Removed launch and gameplay debug console logging while preserving in-game score updates.
- Disabled SpriteKit debug overlays in the main game view.
- Initialized visible score text before the first collision.
- Guarded projectile launches so non-forward taps do not normalize invalid vectors.
- Made vector normalization return zero for zero-length vectors.
- Guarded rounded image helper asset loading and rendered image output.
- Guarded physics contact node casts and restored player-hit handling.
- Added a guarded game-over presenter so win/loss contacts cannot trigger repeated transitions.
- Guarded collision handlers so late callbacks cannot mutate score or player state after game over starts.
- Keyed the enemy spawn action and stopped it when game-over presentation starts.
- Fixed background scroll movement so nodes advance from their current position.
- Added `make check` and a static SpriteKit baseline for plist/storyboard/asset metadata, bundled resources, Xcode project wiring, source inventory, and local-only gameplay guardrails.
- Documented the legacy Xcode project, SpriteKit resources, and static verification workflow.
