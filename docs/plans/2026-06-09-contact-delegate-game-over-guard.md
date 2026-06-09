# Contact Delegate Game-Over Guard

status: completed

## Context

The scene already guards repeated game-over presentation and collision handlers
ignore late callbacks after game over starts. Clearing the physics contact
delegate before presenting the game-over scene reduces late callback delivery
into the outgoing scene during transition.

## Completed Scope

- Cleared `physicsWorld.contactDelegate` in the guarded game-over presenter.
- Kept spawn cancellation and win/loss scene presentation behavior unchanged.
- Extended the static baseline and docs so contact delegate cleanup remains tied
  to game-over presentation.

## Verification

- `make check`
- `git diff --check`
