## iOS Emoji Thrower Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

iOS Emoji Thrower is a Swift SpriteKit game sample with player movement,
projectiles, scoring, sounds, and multiple scenes.

The repository is useful as a compact iOS game project with sprite atlases,
sound assets, storyboard entry, and SpriteKit scene logic.

The goal is to keep the game playable, inspectable, and easy to verify after
gameplay or asset changes.

The current focus is:

Priority:

- Preserve the core SpriteKit gameplay loop
- Keep scene, score, and game-over behavior easy to inspect
- Maintain asset and sound file alignment with project references
- Keep optional image helper rendering tolerant of missing assets
- Keep game-over transitions guarded against repeated contact handling
- Keep delayed game-over restarts tied to the current SpriteKit scene
- Keep collision handlers from mutating score or player state after game over
- Clear the physics contact delegate before game-over scene transitions
- Stop enemy spawning as soon as game-over presentation starts
- Keep background scroll movement running per-frame until game over
- Avoid adding account or network behavior without a clear purpose
- Keep `scripts/check-baseline.py` passing for bundled resources, Xcode
  metadata, SpriteKit source inventory, local-only gameplay, contact handling,
  and debug logging/overlay guardrails
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep the game target on Swift 5 with the iOS 12 deployment target
- Keep pinned macOS CI compiling an unsigned simulator build through the
  canonical `make check` gate

Next priorities:

- Add tests or manual checks for scene loading and score flow
- Add focused logic tests when the SpriteKit scene gains a test target
- Document asset provenance for future replacements

Contribution rules:

- One PR = one focused gameplay, asset, build, or documentation change.
- Verify the game launches and plays after scene or asset changes.
- Keep generated build products and signing files out of git.
- Include screenshots or notes for visible gameplay changes.

## Security

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

This is a local game sample. Future networking, accounts, or analytics should be
opt-in, documented, and unnecessary data collection should be avoided.

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` without Xcode. It verifies plist/storyboard/asset
metadata, bundled resource references, SpriteKit scene sources, image helper
fallbacks, game-over transition guards, game-over restart handling, collision
handler game-over guards, contact delegate cleanup, spawn lifecycle guards,
per-frame background scroll movement, and local-only gameplay with no debug
logging, network, analytics, upload, or persistence behavior.
On macOS, the baseline should compile an unsigned simulator build without
rendering frames, playing audio, simulating physics, or running gameplay.

## What We Will Not Merge (For Now)

- Asset replacements without purpose or provenance
- Analytics or account features unrelated to gameplay
- Broad Swift migration bundled with gameplay changes
- Build changes that make the game harder to open in Xcode

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
