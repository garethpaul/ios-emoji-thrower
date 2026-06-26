# Invalid Scene Width Spawn Guard

Status: Completed

## Goal

Prevent enemy creation when the scene width cannot produce a valid off-screen
monster position.

## Work

- Extended `monsterSpawnY` to require finite positive scene width.
- Kept the optional helper guard ahead of `addChild(monster)` and all physics or
  movement side effects.
- Added a red-first static contract for the horizontal geometry inputs.
- Updated maintained agent, README, security, vision, and change guidance.
- Added completed-plan and guidance checks to the canonical baseline.

## Verification

- Run all four Make aliases from the repository root and an external directory.
- Reject hostile scene-width spawn mutations across finite, positive, ordering,
  guidance, and plan contracts.
- Run projectile math tests when `swiftc` is available.
- Audit Python/shell syntax, whitespace, generated artifacts, and secret-shaped
  additions.

## Completion Evidence

- Before implementation, the baseline failed because `monsterSpawnY` did not
  require finite positive scene width.
- After implementation, the portable baseline passed.
- The repository-root and external-directory `make check` passed, and all four
  Make aliases passed from both invocation locations.
- Six hostile scene-width spawn mutations were rejected across finite-width,
  positive-width, zero-width, optional guard, guidance, and plan-status
  contracts.
- Python and shell syntax, whitespace, generated-artifact, and likely-secret
  audits passed.
- Native SpriteKit execution was not performed because Xcode is unavailable
  locally. Executable projectile math was also skipped because `swiftc` is
  unavailable; hosted checks must pass on the exact pull request head.
