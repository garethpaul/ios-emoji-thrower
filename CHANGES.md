# Changes

- Preserved absolute Makefile roots containing spaces and added a recursive-safe
  baseline regression without changing gameplay or credential handling.

## 2026-06-26 17:52 PDT - P1 - Preserve historical Google key response

### Summary

Formalized the unresolved owner-response boundary for the historical Google API
key alert without exposing the value or claiming provider-side remediation.

### Work completed

- Added the retired Google service credential filename to `.gitignore`.
- Synchronized the revocation/rotation requirement across maintained security
  and contributor guidance.
- Added a static baseline contract and completed design/implementation evidence.

### Threads

- None; the alert metadata, current default branch, and maintained verifier were
  audited directly.

### Files changed

- `.gitignore` — excludes `GoogleService-Info.plist`.
- `scripts/check-baseline.py` — enforces the ignore and owner-response contract.
- `README.md`, `SECURITY.md`, and `AGENTS.md` — preserve the unresolved
  provider-action boundary.
- `docs/plans/2026-06-26-historical-google-key-response-design.md` and
  `docs/plans/2026-06-26-historical-google-key-response.md` — record the
  decision, scope, and verification plan.

### Validation

- GitHub secret-scanning metadata — the alert points to repository history, has
  unknown validity, and remains open.
- Current `master` review — the flagged credential file is absent.
- Red-first `make check` — rejected the missing ignore entry, guidance, and
  completed response evidence.
- `make check`, `make lint`, `make test`, and `make build` — passed the static
  SpriteKit baseline; local `swiftc` and `xcodebuild` skipped truthfully.
- `/usr/bin/make -C /tmp -f "$PWD/Makefile" check` — passed from an external
  caller directory.
- Ignore-entry and security-guidance hostile mutations — both rejected.
- Python AST parsing, shell syntax, and `git diff --check` — passed.
- `gitleaks detect --source . --no-git --redact` — no current-tree leaks found.

### Bugs / findings

- P1 security response gap: a README-only HOLD was not enforced by the baseline
  or repeated in the security policy and contributor guidance.
- Historical Google API key alerts must remain open until the credential owner
  verifies provider-side revocation or rotation.

### Blockers

- Only the credential owner can verify provider-side revocation or rotation;
  this change intentionally does not resolve the GitHub alert.

### Next action

- Complete local and hosted validation, run review on the exact head, and merge
  the focused security-response PR if all gates pass.

## 2026-06-26 15:55 - P1 - Keep game-over geometry current across resize

- The game-over label follows the current scene center after resize, and delayed restart uses the current game-over scene size instead of captured pre-resize geometry.
- Added red-first source contracts for resize relayout and current-size delayed restart.
- Preserved result copy, delay, transition, active-scene restart ownership, and `.resizeFill` behavior.
- Six hostile mutations covering scene-owned label state, resize callback,
  current-center geometry, current-size restart, guidance, and plan status were
  rejected.
- All four Make aliases and external-directory `make check`, Python/shell
  syntax, and `git diff --check` passed. Local `swiftc` and `xcodebuild` were
  unavailable, so hosted macOS remains authoritative.
- Hosted push baseline `28269675521`, pull-request baseline `28269677372`, and
  CodeQL run `28269677126` passed on implementation head
  `52f900b4c7cfb73e80cc7e8cdbbd1c3ee5f3fc76`, including Swift analysis.
- Codex review stopped before analysis with OpenAI HTTP 401; immutable manual
  review found no actionable issues.

## 2026-06-26 - P1 - Reject invalid scene width during enemy spawn

- Enemy spawning rejects non-finite or non-positive scene width before deriving an off-screen monster position.
- Extended the red-first spawn helper contract beyond vertical range safety to
  the horizontal position input used by `addMonster()`.

## 2026-06-26

- Centralized scrolling background sizing and adjacency on `SKScene.size`.
- Preserved the leading tile's scroll phase while retiling both backgrounds
  during initial setup and every `.resizeFill` size change.
- Removed independent per-frame background resizing, which could introduce gaps
  or overlap after rotation.
- Added a red-first, comment-aware static contract and completed verification
  plan without changing scroll speed, gameplay nodes, scoring, or collisions.

## 2026-06-25 06:22 PDT

- Centralized persistent player and score positioning on `SKScene.size` and
  reapplied it from `didChangeSize(_:)`, keeping both nodes correctly placed
  when `.resizeFill` updates the scene during iPad rotation or view resizing.
- Added a comment-aware static regression contract, a runtime rotation check,
  and a completed implementation plan without changing gameplay constants,
  assets, project metadata, or the local-only data boundary.

## 2026-06-18

- Required active-scene game-over ownership before terminal state changes,
  spawn cancellation, contact shutdown, or destination presentation.

## 2026-06-17

- Replaced the fixed projectile travel scalar with validated scene-aware
  projectile travel that includes node clearance for wide and tall scenes.
- Extended the executable Swift harness with scene geometry, projectile margin,
  invalid dimension, and overflow cases.

## 2026-06-16

- Added executable Swift tests for projectile direction normalization using the
  same finite-vector implementation as the SpriteKit scene.

## 2026-06-14

- Ignored queued player contacts after either collision node has already left
  the active scene.

## 2026-06-13

- Made all Make verification aliases location-independent when invoked through
  an absolute Makefile path.
- Rejected non-finite touch vectors before projectile physics, insertion,
  movement, or sound effects.
- Skipped enemy spawning for invalid or undersized scene geometry before
  constructing a closed random range or adding the SpriteKit node.

## 2026-06-12

- Prevented duplicate queued projectile contacts from scoring after either
  collision node has already left the active scene.

## 2026-06-10

- Migrated the SpriteKit target from Swift 3 to Swift 5.
- Raised the deployment target from iOS 10 to iOS 12.
- Replaced the `arc4random` float conversion with bounded
  `CGFloat.random(in:)` generation.
- Upgraded Xcode-enabled validation from project parsing to an unsigned iOS
  Simulator build.
- Added a static guard requiring the CI workflow and completed CI baseline plan
  to remain checked in.
- Guarded delayed game-over restarts so only the current game-over scene can
  present a restarted game scene, using the same resize mode as initial launch.
- Added pinned, read-only macOS GitHub Actions CI for the canonical `make check`
  baseline.
- Made Xcode-enabled checks parse `EmojiThrower.xcodeproj` without running
  SpriteKit gameplay, rendering, audio, or physics simulation.

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static SpriteKit baseline.
- Cleared the physics contact delegate before game-over scene transitions so
  late SpriteKit contacts do not keep dispatching into the old scene.
- Enabled per-frame background scroll updates until game-over presentation
  starts.

## 2026-06-08

- Removed launch and gameplay debug console logging while preserving in-game score updates.
- Disabled SpriteKit debug overlays in the main game view.
- Initialized visible score text before the first collision.
- Guarded projectile launches so non-forward taps do not normalize invalid vectors.
- Made vector normalization return zero for zero-length vectors.
- Guarded rounded image helper asset loading and rendered image output.
- Guarded physics contact node casts and restored player-hit handling.
- Added a guarded game-over presenter so win/loss contacts cannot trigger repeated transitions.
- Guarded collision handlers so late callbacks cannot mutate score or player state after game over starts.
- Keyed the enemy spawn action and stopped it when game-over presentation starts.
- Fixed background scroll movement so nodes advance from their current position.
- Added `make check` and a static SpriteKit baseline for plist/storyboard/asset metadata, bundled resources, Xcode project wiring, source inventory, and local-only gameplay guardrails.
- Documented the legacy Xcode project, SpriteKit resources, and static verification workflow.
