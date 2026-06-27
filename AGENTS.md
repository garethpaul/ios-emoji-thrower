# AGENTS.md

## Repository purpose

`garethpaul/ios-emoji-thrower` is a Swift SpriteKit game sample in which the
player launches emoji projectiles at moving targets.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `EmojiThrower.xcodeproj` - Xcode project
- `EmojiThrower` - Swift gameplay source, scenes, assets, sounds, and app metadata

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check` (includes an unsigned simulator build when Xcode
  is available)
- Make gates support absolute checkout paths containing spaces; preserve the
  single-Makefile authority boundary and recursive regression.
- Local Apple development: `open EmojiThrower.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (10).
- Preserve the checked-in Swift 5, iOS 12, Xcode, and signing assumptions unless
  the change is explicitly about modernization.

## Testing guidance

- `make check` compiles and runs the shared projectile-math harness when
  `swiftc` is available; hosted macOS is the authoritative execution boundary.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, Apple toolchain assumptions, and any
  risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file is needed for current gameplay. Keep
  `GoogleService-Info.plist` and any future integration secrets out of git.
- Historical Google API key alerts must remain open until the credential owner
  verifies provider-side revocation or rotation.
- Debug logging from launch and gameplay paths should stay removed; score should remain visible in-game rather than printed to the console.
- Runtime debug overlays should stay disabled outside explicit troubleshooting builds.
- Resource changes should keep image, sound, font, scene, and Xcode project references aligned, with fallback behavior for optional image helper rendering.
- Keep active-scene game-over ownership ahead of terminal state, spawn,
  contact-delegate, and presentation side effects.
- Keep persistent player and score positions derived from `SKScene.size`, and
  reapply them from `didChangeSize(_:)` when `.resizeFill` resizes the scene.
- Enemy spawning rejects non-finite or non-positive scene width before deriving an off-screen monster position.
- Keep the two scrolling background tiles contiguous after initial setup and
  every scene-size change without resizing them independently per frame.
- The game-over label follows the current scene center after resize, and delayed restart uses the current game-over scene size instead of captured pre-resize geometry.
- This is an Apple platform sample. Xcode, Swift, and deployment target versions
  must stay aligned with the checked-in project settings.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
