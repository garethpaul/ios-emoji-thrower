# Image Helper Guard Plan

status: completed

## Context

`ios-emoji-thrower` includes a `roundSquareImage` helper that creates rounded SpriteKit textures from bundled images. The helper force-unwraps image loading and rendered graphics output, which can crash if an asset is renamed, removed, or fails to render.

## Objectives

- Guard image loading before creating the rounded texture.
- Return a named fallback sprite when the source image is unavailable.
- Guard rendered image output before creating an `SKTexture`.
- Extend the static baseline so image helper force unwraps do not return.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
