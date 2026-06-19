# Projectile Duplicate Contact Guard

status: completed

## Context

SpriteKit may deliver multiple queued contacts involving the same projectile in
one physics step. `projectileDidCollideWithMonster` increments score before
checking whether the projectile or monster was already removed, so one shot can
score more than once when contacts overlap.

## Work Completed

- Require both collision nodes to remain attached to the active scene before
  mutating score.
- Remove the nodes before incrementing and rendering the score.
- Preserve the existing game-over guard and 20-hit win threshold.
- Extend the static baseline with node-lifecycle ordering contracts.

## Verification Completed

- Local `make check`, `make lint`, `make test`, and `make build` passed. The
  local environment did not provide `xcodebuild`, so these runs exercised the
  complete static baseline and reported the hosted Xcode requirement.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Hostile mutations changing the plan status, inserting an unfinished-work
  marker, falsifying a run ID, removing the active-node predicate, or moving
  score mutation before node removal were rejected by the baseline.
- The implementation push Check run `27394998651` completed successfully for
  commit `560e645d46cd073f7d062719c486e022e0d79611`.
- The implementation pull-request Check run `27395002711` completed
  successfully for commit `560e645d46cd073f7d062719c486e022e0d79611` and
  built the Swift 5 SpriteKit sample on hosted macOS.
- The post-merge push Check run `27395075194` completed successfully for
  commit `8ce9716ffb4a523612fad6a401a326b2d17b22ac`.
- The CodeQL setup run `27402323210` completed successfully for commit
  `8ce9716ffb4a523612fad6a401a326b2d17b22ac`.
- The collision handler preserves
  `guard projectile.parent === self, monster.parent === self else { return }`
  and removes both nodes before `monstersDestroyed += 1`.
