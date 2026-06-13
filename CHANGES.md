# Changes

## 2026-06-13

- Skipped enemy spawning for invalid or undersized scene geometry before
  constructing a closed random range or adding the SpriteKit node.

## 2026-06-12

- Prevented duplicate queued projectile contacts from scoring after either
  collision node has already left the active scene.

## 2026-06-10

- Migrated the SpriteKit target from Swift 3 to Swift 5.
- Raised the deployment target from iOS 10 to iOS 12.
- Replaced the `arc4random` float conversion with bounded
  `CGFloat.random(in:)` generation.
- Upgraded Xcode-enabled validation from project parsing to an unsigned iOS
  Simulator build.
- Added a static guard requiring the CI workflow and completed CI baseline plan
  to remain checked in.
- Guarded delayed game-over restarts so only the current game-over scene can
  present a restarted game scene, using the same resize mode as initial launch.
- Added pinned, read-only macOS GitHub Actions CI for the canonical `make check`
  baseline.
- Made Xcode-enabled checks parse `EmojiThrower.xcodeproj` without running
  SpriteKit gameplay, rendering, audio, or physics simulation.

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static SpriteKit baseline.
- Cleared the physics contact delegate before game-over scene transitions so
  late SpriteKit contacts do not keep dispatching into the old scene.
- Enabled per-frame background scroll updates until game-over presentation
  starts.

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
