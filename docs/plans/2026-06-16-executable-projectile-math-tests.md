# Executable Projectile Math Tests

Status: Completed

## Goal

Replace static-only confidence in projectile direction validation with
executable Swift tests of the same implementation used by `GameScene`.

## Implementation

- Move finite, forward-only direction normalization into a Foundation-only
  `ProjectileMath` helper.
- Keep SpriteKit scene orchestration unchanged while delegating deterministic
  vector validation to the shared helper.
- Compile the helper and a repository-owned Swift harness through `make check`
  whenever `swiftc` is available.
- Keep the hosted macOS gate responsible for executable tests and the existing
  unsigned iOS Simulator application build.

## Verification

- Repository and external-directory `make check` passed with explicit local
  Swift/Xcode toolchain boundaries.
- The harness covers finite normalization, downward shots, zero-length and
  backward offsets, NaN and infinity, and overflowing vector lengths.
- Hostile mutations were rejected for runner invocation, app delegation,
  finite-vector guards, behavioral assertions, and Xcode source membership.
