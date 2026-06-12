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
- Local Apple development: `open EmojiThrower.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (9).
- Preserve the checked-in Swift 5, iOS 12, Xcode, and signing assumptions unless
  the change is explicitly about modernization.

## Testing guidance

- No dedicated test files were detected; treat `make check` as the minimum baseline.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, Apple toolchain assumptions, and any
  risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- Debug logging from launch and gameplay paths should stay removed; score should remain visible in-game rather than printed to the console.
- Runtime debug overlays should stay disabled outside explicit troubleshooting builds.
- Resource changes should keep image, sound, font, scene, and Xcode project references aligned, with fallback behavior for optional image helper rendering.
- This is an Apple platform sample. Xcode, Swift, and deployment target versions
  must stay aligned with the checked-in project settings.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
