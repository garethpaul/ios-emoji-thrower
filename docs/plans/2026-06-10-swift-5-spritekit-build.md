# Swift 5 SpriteKit Build

status: completed

## Context

The hosted gate parsed the Xcode project but did not compile it. The game target
still selected Swift 3 and iOS 10, and several SpriteKit/UIKit APIs used syntax
that current Xcode no longer accepts.

## Completed Scope

- Migrated app-launch, SpriteKit color/action, coder-initializer, and status-bar
  APIs to Swift 5 syntax.
- Replaced the `arc4random` float conversion with bounded
  `CGFloat.random(in:)` generation.
- Set both game target configurations to Swift 5.
- Raised the deployment target from iOS 10 to iOS 12.
- Upgraded Xcode-enabled `make check` runs to compile an unsigned Debug build for
  the iOS Simulator without launching gameplay.
- Extended the baseline and documentation to preserve the toolchain contract.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- hosted macOS simulator build
- `git diff --check`
