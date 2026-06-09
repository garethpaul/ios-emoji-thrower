# ios-emoji-thrower

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/ios-emoji-thrower` is an Apple platform application or Swift sample. An Emoji SpriteKit Game

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (9).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `README.md` - project overview and local usage notes
- `EmojiThrower` - source or example code
- `EmojiThrower.xcodeproj` - Xcode project file
- `Makefile` - local verification entry point
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static SpriteKit resource and source verifier
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: EmojiThrower
- Dependency and build manifests: none detected
- Entry points or build surfaces: `make check`, EmojiThrower.xcodeproj
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/ios-emoji-thrower.git
cd ios-emoji-thrower
make check
```

The checked-in project has no external dependency manifest. Use Xcode for full builds and `make check` for static verification on hosts without Xcode.

## Running or Using the Project

- Open `EmojiThrower.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- The game uses SpriteKit scene logic, bundled image resources, sound files, and `Sketch3D.otf`.
- Win and loss paths share a guarded game-over presenter so contacts do not trigger repeated scene transitions.
- This is a local game sample. Do not add accounts, analytics, persistence, upload, or network behavior without a dedicated design and security review.

## Testing and Verification

Run the local static baseline:

```bash
make check
```

The baseline runs `scripts/check-baseline.py`, parses plist/storyboard/asset metadata, validates the binary SpriteKit scene plist, checks Xcode resource references, verifies the Swift source inventory, and guards against image-helper force unwraps, repeated game-over transitions, debug logging, network, analytics, upload, or persistence behavior.

For full legacy verification on macOS, use Xcode's test action or `xcodebuild test` with the appropriate scheme and destination.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include EmojiThrower/Info.plist.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include EmojiThrower/GameScene.swift.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include EmojiThrower/GameScene.swift, EmojiThrower/Info.plist.
- Debug logging from launch and gameplay paths should stay removed; score should remain visible in-game rather than printed to the console.
- Runtime debug overlays should stay disabled outside explicit troubleshooting builds.
- Resource changes should keep image, sound, font, scene, and Xcode project references aligned, with fallback behavior for optional image helper rendering.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- Run `make check` before pushing changes to Swift sources, plist/storyboard files, SpriteKit assets, sounds, fonts, Xcode metadata, or gameplay/privacy documentation.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
