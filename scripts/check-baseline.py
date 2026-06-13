#!/usr/bin/env python3
from pathlib import Path
import json
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-spritekit-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
IMAGE_GUARD_PLAN = ROOT / "docs/plans/2026-06-08-image-helper-guard.md"
GAME_OVER_PLAN = ROOT / "docs/plans/2026-06-08-game-over-transition-guard.md"
SPAWN_LIFECYCLE_PLAN = ROOT / "docs/plans/2026-06-08-spawn-lifecycle-guard.md"
BACKGROUND_SCROLL_PLAN = ROOT / "docs/plans/2026-06-09-background-scroll-position.md"
COLLISION_HANDLER_PLAN = ROOT / "docs/plans/2026-06-09-collision-handler-game-over-guard.md"
CONTACT_DELEGATE_PLAN = ROOT / "docs/plans/2026-06-09-contact-delegate-game-over-guard.md"
BACKGROUND_UPDATE_PLAN = ROOT / "docs/plans/2026-06-09-background-scroll-update.md"
GAME_OVER_RESTART_PLAN = ROOT / "docs/plans/2026-06-10-game-over-restart-guard.md"
CI_PLAN = ROOT / "docs/plans/2026-06-10-ci-baseline.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
SWIFT_5_BUILD_PLAN = ROOT / "docs/plans/2026-06-10-swift-5-spritekit-build.md"
DUPLICATE_CONTACT_PLAN = ROOT / "docs/plans/2026-06-12-projectile-duplicate-contact-guard.md"
UNDERSIZED_SPAWN_PLAN = ROOT / "docs/plans/2026-06-13-undersized-scene-spawn-guard.md"
FINITE_TOUCH_VECTOR_PLAN = ROOT / "docs/plans/2026-06-13-finite-projectile-touch-vector.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  baseline:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10
        with:
          persist-credentials: false
      - name: Validate project and SpriteKit baseline
        run: make check
"""


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_json(relative_path, failures):
    try:
        return json.loads(read(relative_path))
    except json.JSONDecodeError as error:
        failures.append(f"{relative_path} is not valid JSON: {error}")
        return {}


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def main():
    failures = []
    required_files = [
        ".gitignore",
        ".github/workflows/check.yml",
        ".github/CODEOWNERS",
        "AGENTS.md",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "EmojiThrower.xcodeproj/project.pbxproj",
        "EmojiThrower.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "EmojiThrower/Info.plist",
        "EmojiThrower/AppDelegate.swift",
        "EmojiThrower/GameScene.swift",
        "EmojiThrower/GameViewController.swift",
        "EmojiThrower/GameOverScene.swift",
        "EmojiThrower/GameScene.sks",
        "EmojiThrower/Main.storyboard",
        "EmojiThrower/Base.lproj/LaunchScreen.storyboard",
        "EmojiThrower/Assets.xcassets/Contents.json",
        "EmojiThrower/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "EmojiThrower/Assets.xcassets/bg.imageset/Contents.json",
        "EmojiThrower/Assets.xcassets/bg.imageset/bg.png",
        "EmojiThrower/sprites.atlas/player.png",
        "EmojiThrower/sprites.atlas/player@2x.png",
        "EmojiThrower/sprites.atlas/projectile.png",
        "EmojiThrower/sprites.atlas/projectile@2x.png",
        "EmojiThrower/sprites.atlas/monster.png",
        "EmojiThrower/sprites.atlas/monster@2x.png",
        "EmojiThrower/Sounds/background-music-aac.caf",
        "EmojiThrower/Sounds/pew-pew-lei.caf",
        "EmojiThrower/Sketch3D.otf",
        "docs/plans/2026-06-08-spritekit-baseline.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-image-helper-guard.md",
        "docs/plans/2026-06-08-game-over-transition-guard.md",
        "docs/plans/2026-06-08-spawn-lifecycle-guard.md",
        "docs/plans/2026-06-09-background-scroll-position.md",
        "docs/plans/2026-06-09-collision-handler-game-over-guard.md",
        "docs/plans/2026-06-09-contact-delegate-game-over-guard.md",
        "docs/plans/2026-06-09-background-scroll-update.md",
        "docs/plans/2026-06-10-game-over-restart-guard.md",
        "docs/plans/2026-06-10-ci-baseline.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-swift-5-spritekit-build.md",
        "docs/plans/2026-06-12-projectile-duplicate-contact-guard.md",
        "docs/plans/2026-06-13-undersized-scene-spawn-guard.md",
        "docs/plans/2026-06-13-finite-projectile-touch-vector.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/readme-overview.svg",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "EmojiThrower.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "EmojiThrower/Main.storyboard",
        "EmojiThrower/Base.lproj/LaunchScreen.storyboard",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    for json_file in [
        "EmojiThrower/Assets.xcassets/Contents.json",
        "EmojiThrower/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "EmojiThrower/Assets.xcassets/bg.imageset/Contents.json",
    ]:
        parse_json(json_file, failures)

    app_plist = parse_plist("EmojiThrower/Info.plist", failures)
    parse_plist("EmojiThrower/GameScene.sks", failures)

    project = read("EmojiThrower.xcodeproj/project.pbxproj")
    swift_sources = "\n".join(strip_swift_line_comments(path.read_text(encoding="utf-8", errors="replace"))
                              for path in sorted((ROOT / "EmojiThrower").glob("*.swift")))
    game_scene = read("EmojiThrower/GameScene.swift")
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    workflow = read(".github/workflows/check.yml")
    codeowners = read(".github/CODEOWNERS")
    agent_guidance = read("AGENTS.md")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    image_guard_plan = IMAGE_GUARD_PLAN.read_text(encoding="utf-8") if IMAGE_GUARD_PLAN.exists() else ""
    game_over_plan = GAME_OVER_PLAN.read_text(encoding="utf-8") if GAME_OVER_PLAN.exists() else ""
    spawn_lifecycle_plan = SPAWN_LIFECYCLE_PLAN.read_text(encoding="utf-8") if SPAWN_LIFECYCLE_PLAN.exists() else ""
    background_scroll_plan = BACKGROUND_SCROLL_PLAN.read_text(encoding="utf-8") if BACKGROUND_SCROLL_PLAN.exists() else ""
    collision_handler_plan = COLLISION_HANDLER_PLAN.read_text(encoding="utf-8") if COLLISION_HANDLER_PLAN.exists() else ""
    contact_delegate_plan = CONTACT_DELEGATE_PLAN.read_text(encoding="utf-8") if CONTACT_DELEGATE_PLAN.exists() else ""
    background_update_plan = BACKGROUND_UPDATE_PLAN.read_text(encoding="utf-8") if BACKGROUND_UPDATE_PLAN.exists() else ""
    game_over_restart_plan = GAME_OVER_RESTART_PLAN.read_text(encoding="utf-8") if GAME_OVER_RESTART_PLAN.exists() else ""
    ci_plan = CI_PLAN.read_text(encoding="utf-8") if CI_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    swift_5_build_plan = SWIFT_5_BUILD_PLAN.read_text(encoding="utf-8") if SWIFT_5_BUILD_PLAN.exists() else ""
    duplicate_contact_plan = DUPLICATE_CONTACT_PLAN.read_text(encoding="utf-8") if DUPLICATE_CONTACT_PLAN.exists() else ""
    undersized_spawn_plan = UNDERSIZED_SPAWN_PLAN.read_text(encoding="utf-8") if UNDERSIZED_SPAWN_PLAN.exists() else ""
    finite_touch_vector_plan = FINITE_TOUCH_VECTOR_PLAN.read_text(encoding="utf-8") if FINITE_TOUCH_VECTOR_PLAN.exists() else ""
    location_independent_make_plan = LOCATION_INDEPENDENT_MAKE_PLAN.read_text(encoding="utf-8") if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")

    require(project.count("IPHONEOS_DEPLOYMENT_TARGET = 12.0;") == 2 and
            "IPHONEOS_DEPLOYMENT_TARGET = 10.0;" not in project and
            project.count("SWIFT_VERSION = 5.0;") == 2 and
            "SWIFT_VERSION = 3.0;" not in project,
            "Xcode project must use Swift 5 with the iOS 12 deployment target",
            failures)
    require("[UIApplication.LaunchOptionsKey: Any]?" in swift_sources,
            "AppDelegate must use the Swift 5 launch-options signature",
            failures)
    for resource in ["Assets.xcassets", "sprites.atlas", "background-music-aac.caf", "pew-pew-lei.caf", "Sketch3D.otf", "GameScene.sks"]:
        require(resource in project, f"Xcode project must keep resource reference: {resource}", failures)
    require(app_plist.get("UIAppFonts") == ["Sketch3D.otf"],
            "Info.plist must register the bundled Sketch3D font",
            failures)
    require("Pods" not in project and not (ROOT / "Podfile").exists(),
            "SpriteKit sample must stay dependency-free unless dependencies are explicitly documented",
            failures)

    require("class GameScene: SKScene" in game_scene and "SKPhysicsContactDelegate" in game_scene,
            "GameScene must retain SpriteKit scene and physics contact behavior",
            failures)
    require('scoreLabel.text = "Score: \\(monstersDestroyed)"' in game_scene,
            "GameScene must keep visible score label updates",
            failures)
    require('scoreLabel.text = "Score: 0"' in game_scene and "view.frame.width/2" in game_scene,
            "GameScene must initialize visible score text without force-unwrapping self.view",
            failures)
    require("SKAction.playSoundFileNamed" in game_scene and "background-music-aac.caf" in game_scene,
            "GameScene must keep bundled sound playback references",
            failures)
    require("CGFloat.random(in: min...max)" in game_scene and "arc4random" not in game_scene,
            "GameScene must use Swift bounded random generation",
            failures)
    add_monster_index = game_scene.find("func addMonster()")
    spawn_guard_index = game_scene.find("if gameIsOver { return }", add_monster_index)
    create_enemy_index = game_scene.find("let monster = SKSpriteNode", add_monster_index)
    spawn_y_index = game_scene.find("func monsterSpawnY(spriteHeight: CGFloat) -> CGFloat?")
    next_helper_index = game_scene.find("func roundSquareImage", spawn_y_index)
    spawn_y_body = game_scene[spawn_y_index:next_helper_index]
    spawn_y_guard_index = game_scene.find(
        "guard let actualY = monsterSpawnY(spriteHeight: monster.size.height) else",
        add_monster_index,
    )
    add_child_index = game_scene.find("addChild(monster)", add_monster_index)
    require('withKey: "monsterSpawn"' in game_scene and 'removeAction(forKey: "monsterSpawn")' in game_scene,
            "GameScene must run enemy spawning with a key and remove it when game-over presentation starts",
            failures)
    require(add_monster_index != -1 and spawn_guard_index != -1 and spawn_guard_index < create_enemy_index,
            "GameScene must guard enemy spawning after game over before creating sprites",
            failures)
    require(spawn_y_index != -1 and next_helper_index != -1 and
            "guard spriteHeight.isFinite, size.height.isFinite, spriteHeight > 0 else" in spawn_y_body and
            "let minY = spriteHeight / 2" in spawn_y_body and
            "let maxY = size.height - minY" in spawn_y_body and
            "guard minY <= maxY else" in spawn_y_body and
            "return random(min: minY, max: maxY)" in spawn_y_body,
            "monsterSpawnY must reject invalid geometry before constructing the closed random range",
            failures)
    require(spawn_y_guard_index != -1 and add_child_index != -1 and
            create_enemy_index < spawn_y_guard_index < add_child_index and
            "random(min: monster.size.height/2" not in game_scene,
            "addMonster must skip invalid spawn geometry before adding the monster",
            failures)
    require("guard let originalPicture = UIImage(named: imageName)" in game_scene and
            "guard let scaledImage = UIGraphicsGetImageFromCurrentImageContext()" in game_scene and
            "let fallbackImage = SKSpriteNode(imageNamed: imageName)" in game_scene,
            "roundSquareImage must tolerate missing images and failed image rendering",
            failures)
    require("bg.position.x - self.backgroundVelocity" in game_scene,
            "background scrolling must advance from each node's current x-position",
            failures)
    update_index = game_scene.find("override func update")
    move_background_index = game_scene.find("moveBackground()", update_index)
    require(update_index != -1 and
            "if !gameIsOver" in game_scene[update_index:] and
            move_background_index != -1,
            "GameScene must run background scrolling from the per-frame update loop until game over",
            failures)
    require("originalPicture!" not in game_scene and "scaledImage!" not in game_scene and "(originalPicture?.size" not in game_scene,
            "roundSquareImage must not force-unwrap image assets or rendered output",
            failures)
    require("let pointLength = length()" in game_scene and "return CGPoint.zero" in game_scene,
            "CGPoint normalization must handle zero-length vectors",
            failures)
    projectile_direction_index = game_scene.find(
        "func projectileDirection(offset: CGPoint) -> CGPoint?"
    )
    projectile_direction_end = game_scene.find(
        "func roundSquareImage", projectile_direction_index
    )
    projectile_direction_body = game_scene[
        projectile_direction_index:projectile_direction_end
    ]
    touches_ended_index = game_scene.find("override func touchesEnded")
    touch_direction_guard_index = game_scene.find(
        "guard let direction = projectileDirection(offset: offset) else",
        touches_ended_index,
    )
    projectile_physics_index = game_scene.find(
        "projectile.physicsBody =", touches_ended_index
    )
    projectile_add_index = game_scene.find("addChild(projectile)", touches_ended_index)
    projectile_sound_index = game_scene.find(
        "SKAction.playSoundFileNamed", touches_ended_index
    )
    require(projectile_direction_index != -1 and
            "offset.x.isFinite" in projectile_direction_body and
            "offset.y.isFinite" in projectile_direction_body and
            "offset.x > 0" in projectile_direction_body and
            "offsetLength.isFinite" in projectile_direction_body and
            "offsetLength > 0" in projectile_direction_body and
            "direction.x.isFinite" in projectile_direction_body and
            "direction.y.isFinite" in projectile_direction_body,
            "GameScene must reject non-finite, non-forward, and overflowed projectile vectors",
            failures)
    require(touches_ended_index != -1 and touch_direction_guard_index != -1 and
            projectile_physics_index != -1 and projectile_add_index != -1 and
            projectile_sound_index != -1 and
            touch_direction_guard_index < projectile_physics_index <
            projectile_add_index < projectile_sound_index,
            "GameScene must validate projectile direction before physics, insertion, and sound",
            failures)
    require("projectileDidCollideWithMonster(projectile, monster: monster)" in game_scene and
            "monsterDidCollideWithPlayer(monster, player: player)" in game_scene and
            "as? SKSpriteNode" in game_scene,
            "GameScene must guard physics contact casts and handle projectile/player contacts",
            failures)
    require("var gameIsOver = false" in game_scene and
            "func presentGameOver(won: Bool, transition: SKTransition)" in game_scene and
            "if gameIsOver { return }" in game_scene and
            "gameIsOver = true" in game_scene,
            "GameScene must guard repeated game-over transition handling",
            failures)
    present_game_over_index = game_scene.find("func presentGameOver")
    contact_delegate_clear_index = game_scene.find("physicsWorld.contactDelegate = nil", present_game_over_index)
    present_scene_index = game_scene.find("presentScene", present_game_over_index)
    require("physicsWorld.contactDelegate = self" in game_scene and
            present_game_over_index != -1 and contact_delegate_clear_index != -1 and
            present_scene_index != -1 and contact_delegate_clear_index < present_scene_index,
            "GameScene must clear the physics contact delegate before presenting game over",
            failures)
    require("presentGameOver(won: true, transition: reveal)" in game_scene and
            "presentGameOver(won: false, transition: reveal)" in game_scene,
            "GameScene win and loss paths must use the guarded game-over presenter",
            failures)
    projectile_collision_index = game_scene.find("func projectileDidCollideWithMonster")
    projectile_guard_index = game_scene.find("if gameIsOver { return }", projectile_collision_index)
    projectile_active_node_guard_index = game_scene.find("guard projectile.parent === self, monster.parent === self else { return }", projectile_collision_index)
    projectile_remove_index = game_scene.find("projectile.removeFromParent()", projectile_collision_index)
    monster_remove_index = game_scene.find("monster.removeFromParent()", projectile_collision_index)
    projectile_score_index = game_scene.find("monstersDestroyed += 1", projectile_collision_index)
    require(projectile_collision_index != -1 and projectile_guard_index != -1 and
            projectile_score_index != -1 and projectile_guard_index < projectile_score_index,
            "Projectile collision handler must ignore late contacts before mutating score",
            failures)
    require(projectile_active_node_guard_index != -1 and
            projectile_guard_index < projectile_active_node_guard_index < projectile_remove_index and
            projectile_remove_index < projectile_score_index and monster_remove_index < projectile_score_index,
            "Projectile collisions must require active nodes and remove them before mutating score",
            failures)
    player_collision_index = game_scene.find("func monsterDidCollideWithPlayer")
    player_guard_index = game_scene.find("if gameIsOver { return }", player_collision_index)
    player_destroyed_index = game_scene.find("playerDestroyed = true", player_collision_index)
    require(player_collision_index != -1 and player_guard_index != -1 and
            player_destroyed_index != -1 and player_guard_index < player_destroyed_index,
            "Player collision handler must ignore late contacts before mutating player state",
            failures)
    game_view_controller = read("EmojiThrower/GameViewController.swift")
    require("guard let skView = view as? SKView" in game_view_controller,
            "GameViewController must guard the SpriteKit view cast",
            failures)
    require("showsFPS = false" in game_view_controller and "showsNodeCount = false" in game_view_controller,
            "GameViewController must keep SpriteKit debug overlays disabled",
            failures)
    game_over_scene = read("EmojiThrower/GameOverScene.swift")
    require("func restartGame(size: CGSize, transition: SKTransition) -> Bool" in game_over_scene and
            "guard let view = self.view, view.scene === self else" in game_over_scene and
            "scene.scaleMode = .resizeFill" in game_over_scene and
            "view.presentScene(scene, transition: transition)" in game_over_scene and
            "self.restartGame(size: size, transition: reveal)" in game_over_scene,
            "GameOverScene must guard delayed restarts and keep restart scale mode aligned",
            failures)
    require(not re.search(r"\b(?:print|println|NSLog)\s*\(", swift_sources),
            "Game sources must not use debug console logging",
            failures)
    for forbidden in ["NSURL", "URLSession", "NSURLConnection", "http://", "https://", "upload", "analytics", "NSUserDefaults", "UserDefaults"]:
        require(forbidden not in swift_sources,
                f"Game sample must not add network, upload, analytics, or persistence behavior: {forbidden}",
                failures)

    swift_files = sorted((ROOT / "EmojiThrower").glob("*.swift"))
    require(len(swift_files) >= 8,
            "expected Swift source inventory is missing",
            failures)
    require("*.local.xcconfig" in gitignore and ".env" in gitignore and "DerivedData" in gitignore,
            ".gitignore must exclude local config and Xcode build products",
            failures)
    require(".PHONY: build check lint test" in makefile and
            "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile and
            "lint test build: check" in makefile and
            'python3 "$(ROOT)/scripts/check-baseline.py"' in makefile and
            "python3 scripts/check-baseline.py" not in makefile,
            "Makefile must expose location-independent lint, test, build, and check aliases",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "EmojiThrower.xcodeproj" in readme and "SpriteKit" in readme and
            "image" in readme.lower() and "game-over" in readme.lower() and "spawn" in readme.lower() and
            "background scroll" in readme.lower() and "per-frame" in readme.lower() and "collision handler" in readme.lower() and
            "contact delegate" in readme.lower() and "restart" in readme.lower() and
            "undersized scene" in readme.lower() and "GitHub Actions" in readme,
            "README must document static verification, project usage, SpriteKit context, collision handler guardrails, and image guardrails",
            failures)
    require("local game" in readme.lower() and "debug logging" in readme.lower() and "debug overlays" in readme.lower(),
            "README must document local-only gameplay and debug logging/overlay expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "asset" in vision.lower() and
            "game-over" in vision.lower() and "spawn" in vision.lower() and
            "background scroll" in vision.lower() and "per-frame" in vision.lower() and "collision handler" in vision.lower() and
            "contact delegate" in vision.lower() and "restart" in vision.lower() and
            "undersized scene" in vision.lower() and "GitHub Actions" in vision,
            "VISION must describe the current static SpriteKit baseline",
            failures)
    require("debug logging" in security.lower() and "debug overlays" in security.lower() and
            "spawn" in security.lower() and "background scroll" in security.lower() and "per-frame" in security.lower() and
            "collision handler" in security.lower() and "contact delegate" in security.lower() and
            "restart" in security.lower() and "undersized scene" in security.lower() and
            "make check" in security and "GitHub Actions" in security,
            "SECURITY must document debug logging/overlay and static baseline guardrails",
            failures)
    require("debug console logging" in changes and "debug overlays" in changes and "player-hit" in changes and
            "projectile" in changes and "zero-length" in changes and "image" in changes.lower() and
            "game-over" in changes.lower() and "restart" in changes.lower() and "spawn" in changes.lower() and
            "background scroll" in changes.lower() and "per-frame" in changes.lower() and
            "undersized scene" in changes.lower() and "make check" in changes and
            "make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record the debug cleanup, contact handling, vector guard, image guard, game-over guard, spawn guard, and baseline",
            failures)
    require("non-finite touch vectors" in readme.lower() and
            "non-finite touch vectors" in security.lower() and
            "non-finite touch vectors" in vision.lower() and
            "non-finite touch vectors" in changes.lower(),
            "Docs must record finite projectile touch-vector validation",
            failures)
    require("absolute makefile path" in readme.lower() and
            "location-independent" in changes.lower(),
            "README and CHANGES must document location-independent Make verification",
            failures)
    require("collision handler" in changes.lower(),
            "CHANGES must record the collision handler game-over guard",
            failures)
    require("contact delegate" in changes.lower(),
            "CHANGES must record the contact delegate game-over guard",
            failures)
    require("GitHub Actions" in changes,
            "CHANGES must record the GitHub Actions baseline",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in image_guard_plan and
            "status: completed" in game_over_plan and "status: completed" in spawn_lifecycle_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in background_scroll_plan,
            "background scroll position plan must be marked completed",
            failures)
    require("status: completed" in collision_handler_plan,
            "collision handler game-over guard plan must be marked completed",
            failures)
    require("status: completed" in contact_delegate_plan,
            "contact delegate game-over guard plan must be marked completed",
            failures)
    require("status: completed" in background_update_plan,
            "background scroll update plan must be marked completed",
            failures)
    require("status: completed" in game_over_restart_plan,
            "game-over restart guard plan must be marked completed",
            failures)
    require("status: completed" in ci_plan and "make check" in ci_plan and
            "simulator" in ci_plan.lower(),
            "CI baseline plan must record completed status and make check verification",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be completed and document make check",
            failures)
    require("status: completed" in swift_5_build_plan and "simulator" in swift_5_build_plan.lower(),
            "Swift 5 SpriteKit build plan must be completed and document simulator verification",
            failures)
    require("status: completed" in undersized_spawn_plan and
            "All four Make gates" in undersized_spawn_plan and
            "hostile mutations" in undersized_spawn_plan.lower(),
            "undersized scene spawn plan must record completed status and verification",
            failures)
    location_make_statuses = re.findall(
        r"^status: .+$", location_independent_make_plan, flags=re.MULTILINE
    )
    location_make_verification = markdown_section(
        location_independent_make_plan, "Verification Completed"
    )
    require(location_make_statuses == ["status: completed"] and
            "All four Make gates passed from the checkout" in location_make_verification and
            "All four Make gates passed from `/tmp` through the absolute Makefile path" in location_make_verification and
            "python3 -m py_compile scripts/check-baseline.py" in location_make_verification and
            "git diff --check" in location_make_verification and
            "`xcodebuild` was unavailable" in location_make_verification and
            "Five isolated hostile mutations were rejected" in location_make_verification and
            re.search(r"\b(?:pending|todo|tbd|not run)\b",
                      location_make_verification,
                      re.IGNORECASE) is None,
            "location-independent Make plan must record completed status and actual local verification",
            failures)
    finite_touch_statuses = re.findall(
        r"^status: .+$", finite_touch_vector_plan, flags=re.MULTILINE
    )
    finite_touch_sections = finite_touch_vector_plan.split(
        "## Verification Completed\n", 1
    )
    finite_touch_verification = (
        finite_touch_sections[1] if len(finite_touch_sections) == 2 else ""
    )
    finite_touch_required_evidence = (
        "All four Make gates",
        "`xcodebuild` was",
        "python3 -m py_compile scripts/check-baseline.py",
        "plist, XML, and workflow YAML parsing",
        "git diff --check",
        "Seven isolated hostile mutations",
    )
    require(finite_touch_statuses == ["status: completed"]
            and all(item in finite_touch_verification
                    for item in finite_touch_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b",
                          finite_touch_verification,
                          re.IGNORECASE) is None,
            "finite projectile touch-vector plan must record completed status and actual local verification",
            failures)
    duplicate_contact_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", duplicate_contact_plan
    )
    duplicate_contact_work = markdown_section(duplicate_contact_plan, "Work Completed")
    duplicate_contact_verification = markdown_section(
        duplicate_contact_plan, "Verification Completed"
    )
    require(duplicate_contact_status == ["completed"] and duplicate_contact_work,
            "duplicate projectile contact plan must record one completed status and completed work",
            failures)
    require(duplicate_contact_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", duplicate_contact_verification),
            "duplicate projectile contact plan must record finished verification without pending markers",
            failures)
    for evidence in [
        "make check",
        "make lint",
        "make test",
        "make build",
        "python3 -m py_compile scripts/check-baseline.py",
        "git diff --check",
        "27394998651",
        "27395002711",
        "27395075194",
        "27402323210",
        "560e645d46cd073f7d062719c486e022e0d79611",
        "8ce9716ffb4a523612fad6a401a326b2d17b22ac",
        "guard projectile.parent === self, monster.parent === self else { return }",
        "monstersDestroyed += 1",
    ]:
        require(evidence in duplicate_contact_verification,
                f"duplicate projectile contact plan must preserve verification evidence: {evidence}",
                failures)
    workflow_files = sorted(
        str(path.relative_to(ROOT))
        for path in (ROOT / ".github/workflows").rglob("*")
        if path.is_file()
    )
    require(workflow == EXPECTED_WORKFLOW and
            workflow_files == [".github/workflows/check.yml"],
            "GitHub Actions must match the sole reviewed macOS baseline workflow",
            failures)
    require(codeowners.strip() == "* @garethpaul",
            "CODEOWNERS must assign repository-wide ownership to @garethpaul",
            failures)
    require("Swift 5" in agent_guidance and "iOS 12" in agent_guidance and
            "make check" in agent_guidance and "SpriteKit" in agent_guidance,
            "AGENTS guidance must document the current SpriteKit toolchain and gate",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            [
                "xcodebuild",
                "-project", "EmojiThrower.xcodeproj",
                "-target", "EmojiThrower",
                "-configuration", "Debug",
                "-sdk", "iphonesimulator",
                "CODE_SIGNING_ALLOWED=NO",
                "build",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        require(result.returncode == 0,
                "xcodebuild could not compile EmojiThrower for the simulator: " + result.stdout.strip(),
                failures)
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("ios-emoji-thrower SpriteKit baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
