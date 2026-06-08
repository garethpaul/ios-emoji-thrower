# iOS Emoji Thrower SpriteKit Baseline Plan

status: completed

## Context

`ios-emoji-thrower` is a legacy Swift 3 SpriteKit game sample with bundled images, sound effects, a custom font, storyboards, and an `.sks` scene file. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Remove launch/gameplay debug console logging while keeping visible score behavior in the scene.
- Guard projectile launches before vector normalization.
- Add a local `make check` baseline for Xcode metadata, plist/storyboard/asset JSON, source inventory, bundled resources, and local-only gameplay guardrails.
- Keep the game dependency-free and free of network, analytics, account, or upload behavior.
- Document legacy Xcode verification expectations and non-macOS static checks.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
