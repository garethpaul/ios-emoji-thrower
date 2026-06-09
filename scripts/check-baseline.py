#!/usr/bin/env python3
from pathlib import Path
import json
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-spritekit-baseline.md"
IMAGE_GUARD_PLAN = ROOT / "docs/plans/2026-06-08-image-helper-guard.md"
GAME_OVER_PLAN = ROOT / "docs/plans/2026-06-08-game-over-transition-guard.md"
SPAWN_LIFECYCLE_PLAN = ROOT / "docs/plans/2026-06-08-spawn-lifecycle-guard.md"
BACKGROUND_SCROLL_PLAN = ROOT / "docs/plans/2026-06-09-background-scroll-position.md"
COLLISION_HANDLER_PLAN = ROOT / "docs/plans/2026-06-09-collision-handler-game-over-guard.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


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
        "docs/plans/2026-06-08-image-helper-guard.md",
        "docs/plans/2026-06-08-game-over-transition-guard.md",
        "docs/plans/2026-06-08-spawn-lifecycle-guard.md",
        "docs/plans/2026-06-09-background-scroll-position.md",
        "docs/plans/2026-06-09-collision-handler-game-over-guard.md",
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
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    image_guard_plan = IMAGE_GUARD_PLAN.read_text(encoding="utf-8") if IMAGE_GUARD_PLAN.exists() else ""
    game_over_plan = GAME_OVER_PLAN.read_text(encoding="utf-8") if GAME_OVER_PLAN.exists() else ""
    spawn_lifecycle_plan = SPAWN_LIFECYCLE_PLAN.read_text(encoding="utf-8") if SPAWN_LIFECYCLE_PLAN.exists() else ""
    background_scroll_plan = BACKGROUND_SCROLL_PLAN.read_text(encoding="utf-8") if BACKGROUND_SCROLL_PLAN.exists() else ""
    collision_handler_plan = COLLISION_HANDLER_PLAN.read_text(encoding="utf-8") if COLLISION_HANDLER_PLAN.exists() else ""

    require("IPHONEOS_DEPLOYMENT_TARGET = 10.0;" in project and "SWIFT_VERSION = 3.0;" in project,
            "Xcode project must preserve the legacy iOS 10 / Swift 3 settings",
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
    add_monster_index = game_scene.find("func addMonster()")
    spawn_guard_index = game_scene.find("if gameIsOver { return }", add_monster_index)
    create_enemy_index = game_scene.find("let monster = SKSpriteNode", add_monster_index)
    require('withKey: "monsterSpawn"' in game_scene and 'removeAction(forKey: "monsterSpawn")' in game_scene,
            "GameScene must run enemy spawning with a key and remove it when game-over presentation starts",
            failures)
    require(add_monster_index != -1 and spawn_guard_index != -1 and spawn_guard_index < create_enemy_index,
            "GameScene must guard enemy spawning after game over before creating sprites",
            failures)
    require("guard let originalPicture = UIImage(named: imageName)" in game_scene and
            "guard let scaledImage = UIGraphicsGetImageFromCurrentImageContext()" in game_scene and
            "let fallbackImage = SKSpriteNode(imageNamed: imageName)" in game_scene,
            "roundSquareImage must tolerate missing images and failed image rendering",
            failures)
    require("bg.position.x - self.backgroundVelocity" in game_scene,
            "background scrolling must advance from each node's current x-position",
            failures)
    require("originalPicture!" not in game_scene and "scaledImage!" not in game_scene and "(originalPicture?.size" not in game_scene,
            "roundSquareImage must not force-unwrap image assets or rendered output",
            failures)
    require("let pointLength = length()" in game_scene and "return CGPoint.zero" in game_scene,
            "CGPoint normalization must handle zero-length vectors",
            failures)
    require("if (offset.x <= 0) { return }" in game_scene and "let direction = offset.normalized()" in game_scene,
            "GameScene must guard non-forward projectile vectors before normalization",
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
    require("presentGameOver(won: true, transition: reveal)" in game_scene and
            "presentGameOver(won: false, transition: reveal)" in game_scene,
            "GameScene win and loss paths must use the guarded game-over presenter",
            failures)
    projectile_collision_index = game_scene.find("func projectileDidCollideWithMonster")
    projectile_guard_index = game_scene.find("if gameIsOver { return }", projectile_collision_index)
    projectile_score_index = game_scene.find("monstersDestroyed += 1", projectile_collision_index)
    require(projectile_collision_index != -1 and projectile_guard_index != -1 and
            projectile_score_index != -1 and projectile_guard_index < projectile_score_index,
            "Projectile collision handler must ignore late contacts before mutating score",
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
    require("make check" in readme and "EmojiThrower.xcodeproj" in readme and "SpriteKit" in readme and
            "image" in readme.lower() and "game-over" in readme.lower() and "spawn" in readme.lower() and
            "background scroll" in readme.lower() and "collision handler" in readme.lower(),
            "README must document static verification, project usage, SpriteKit context, collision handler guardrails, and image guardrails",
            failures)
    require("local game" in readme.lower() and "debug logging" in readme.lower() and "debug overlays" in readme.lower(),
            "README must document local-only gameplay and debug logging/overlay expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "asset" in vision.lower() and
            "game-over" in vision.lower() and "spawn" in vision.lower() and
            "background scroll" in vision.lower() and "collision handler" in vision.lower(),
            "VISION must describe the current static SpriteKit baseline",
            failures)
    require("debug logging" in security.lower() and "debug overlays" in security.lower() and
            "spawn" in security.lower() and "background scroll" in security.lower() and
            "collision handler" in security.lower() and "make check" in security,
            "SECURITY must document debug logging/overlay and static baseline guardrails",
            failures)
    require("debug console logging" in changes and "debug overlays" in changes and "player-hit" in changes and
            "projectile" in changes and "zero-length" in changes and "image" in changes.lower() and
            "game-over" in changes.lower() and "spawn" in changes.lower() and "background scroll" in changes.lower() and "make check" in changes,
            "CHANGES must record the debug cleanup, contact handling, vector guard, image guard, game-over guard, spawn guard, and baseline",
            failures)
    require("collision handler" in changes.lower(),
            "CHANGES must record the collision handler game-over guard",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in image_guard_plan and
            "status: completed" in game_over_plan and "status: completed" in spawn_lifecycle_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in background_scroll_plan,
            "background scroll position plan must be marked completed",
            failures)
    require("status: completed" in collision_handler_plan,
            "collision handler game-over guard plan must be marked completed",
            failures)

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
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
