# iOS Emoji Thrower CI Baseline

status: completed

## Context

`ios-emoji-thrower` has a Python-backed static SpriteKit resource and source
baseline behind `make check`. The repository needs that baseline to run in
GitHub Actions so gameplay, resource, and local-only guardrails are checked
before review.

## Objectives

- Run the existing `make check` wrapper in GitHub Actions.
- Run the canonical gate on macOS so current Xcode compiles the game target.
- Make the workflow presence part of the static baseline contract.

## Work Completed

- Added `.github/workflows/check.yml` to run `make check` on pushes, pull
  requests, and manual dispatches.
- Integrated the static checker with the pinned, least-privilege macOS gate.
- Compile an unsigned Swift 5 Debug build for the iOS Simulator when Xcode is
  available, without launching gameplay.
- Extended `scripts/check-baseline.py` to require the CI workflow and this
  completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`

## Boundary

The hosted build does not launch gameplay, render SpriteKit frames, play audio,
run physics simulation, sign an app, or replace interactive simulator testing.
