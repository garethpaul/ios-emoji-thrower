# Projectile Duplicate Contact Guard

status: completed

## Context

SpriteKit may deliver multiple queued contacts involving the same projectile in
one physics step. `projectileDidCollideWithMonster` increments score before
checking whether the projectile or monster was already removed, so one shot can
score more than once when contacts overlap.

## Completed Scope

- Require both collision nodes to remain attached to the active scene before
  mutating score.
- Remove the nodes before incrementing and rendering the score.
- Preserve the existing game-over guard and 20-hit win threshold.
- Extend the static baseline with node-lifecycle ordering contracts.

## Verification

- `make check`
- `git diff --check`
- Mutations removing the active-node guard or moving score mutation before node
  removal must fail the baseline.
- Hosted macOS validation must build the Swift 5 SpriteKit sample.
