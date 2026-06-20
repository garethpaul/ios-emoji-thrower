#!/usr/bin/env python3
import argparse
import plistlib
import re
import subprocess
import sys
from pathlib import Path


FIREBASE_PATH = Path("EmojiThrower/GoogleService-Info.plist")
TWITTER_PATH = Path("EmojiThrower/Config.plist")
FIREBASE_EXAMPLE_PATH = Path(f"{FIREBASE_PATH}.example")
TWITTER_EXAMPLE_PATH = Path(f"{TWITTER_PATH}.example")

FIREBASE_FIELDS = (
    "AD_UNIT_ID_FOR_BANNER_TEST",
    "AD_UNIT_ID_FOR_INTERSTITIAL_TEST",
    "API_KEY",
    "BUNDLE_ID",
    "CLIENT_ID",
    "DATABASE_URL",
    "GCM_SENDER_ID",
    "GOOGLE_APP_ID",
    "IS_ADS_ENABLED",
    "IS_ANALYTICS_ENABLED",
    "IS_APPINVITE_ENABLED",
    "IS_GCM_ENABLED",
    "IS_SIGNIN_ENABLED",
    "PLIST_VERSION",
    "PROJECT_ID",
    "REVERSED_CLIENT_ID",
    "STORAGE_BUCKET",
)
TWITTER_FIELDS = ("twtrKey", "twtrSecret")


def read_plist(path):
    try:
        with path.open("rb") as handle:
            return plistlib.load(handle), None
    except (OSError, plistlib.InvalidFileException):
        return None, f"invalid property list: {path.name}"


def firebase_example():
    return read_plist(Path(__file__).resolve().parents[1] / FIREBASE_EXAMPLE_PATH)[0]


def twitter_example():
    return read_plist(Path(__file__).resolve().parents[1] / TWITTER_EXAMPLE_PATH)[0]


def is_placeholder(value):
    return isinstance(value, str) and (
        value.startswith("REPLACE_WITH_") or not value.strip()
    )


def validate_plist(path, required_fields):
    data, error = read_plist(path)
    if error:
        return [error]
    errors = []
    for field in required_fields:
        if field not in data:
            errors.append(f"{path.name} is missing required key {field}")
        elif is_placeholder(data[field]):
            errors.append(f"{path.name} contains a placeholder for {field}")
    return errors


def validate_local_configs(root):
    errors = []
    firebase = root / FIREBASE_PATH
    twitter = root / TWITTER_PATH
    if not firebase.is_file():
        errors.append(
            "missing EmojiThrower/GoogleService-Info.plist; copy the sanitized example and download your own Firebase configuration"
        )
    else:
        errors.extend(validate_plist(firebase, FIREBASE_FIELDS))
        firebase_data, firebase_error = read_plist(firebase)
        project_path = root / "EmojiThrower.xcodeproj/project.pbxproj"
        if not firebase_error and project_path.is_file():
            identifiers = set(
                re.findall(
                    r"PRODUCT_BUNDLE_IDENTIFIER\s*=\s*([^;]+);",
                    project_path.read_text(),
                )
            )
            if identifiers and firebase_data.get("BUNDLE_ID") not in identifiers:
                errors.append(
                    "GoogleService-Info.plist BUNDLE_ID does not match the Xcode product bundle identifier"
                )
    if not twitter.is_file():
        errors.append(
            "missing EmojiThrower/Config.plist; copy the sanitized example and add your own Twitter consumer credentials"
        )
    else:
        errors.extend(validate_plist(twitter, TWITTER_FIELDS))
    return errors


def tracked_config_errors(root):
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", str(FIREBASE_PATH), str(TWITTER_PATH)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        f"tracked runtime configuration is forbidden: {path}"
        for path in result.stdout.splitlines()
        if path
    ]


def audit_repository(root):
    errors = tracked_config_errors(root)
    ignore = (root / ".gitignore").read_text()
    for path in (FIREBASE_PATH, TWITTER_PATH):
        if str(path) not in ignore.splitlines():
            errors.append(f".gitignore must contain the exact runtime path: {path}")

    examples = (
        (root / FIREBASE_EXAMPLE_PATH, FIREBASE_FIELDS),
        (root / TWITTER_EXAMPLE_PATH, TWITTER_FIELDS),
    )
    for path, required_fields in examples:
        data, error = read_plist(path)
        if error:
            errors.append(error)
            continue
        if set(data) != set(required_fields):
            errors.append(f"sanitized example schema drifted: {path.name}")
        for field, value in data.items():
            if isinstance(value, str) and field != "PLIST_VERSION" and not is_placeholder(value):
                errors.append(f"sanitized example contains a non-placeholder value for {field}")

    project = (root / "EmojiThrower.xcodeproj/project.pbxproj").read_text()
    for name in (FIREBASE_PATH.name, TWITTER_PATH.name):
        if project.count(f"{name} in Resources") != 2:
            errors.append(f"Xcode resources must include exactly one build entry for {name}")
    phase = "Validate local provider configuration"
    if project.count(phase) != 3:
        errors.append("Xcode target must contain exactly one provider-configuration validation phase")
    build_phases = project.split("buildPhases = (", 1)[1].split(");", 1)[0]
    phase_position = build_phases.find(f"/* {phase} */,")
    resources_position = build_phases.find("/* Resources */,")
    if phase_position < 0 or resources_position < 0 or phase_position > resources_position:
        errors.append("provider-configuration validation must run before the Resources phase")
    first_phase = next((line for line in build_phases.splitlines() if "/*" in line), "")
    if phase not in first_phase:
        errors.append("provider-configuration validation must be the first Xcode build phase")
    validation_block = project.split(
        "A3F0C1112C00000100000001 /* Validate local provider configuration */ = {",
        1,
    )[1].split("\n\t\t};", 1)[0]
    if str(FIREBASE_PATH) in validation_block or str(TWITTER_PATH) in validation_block:
        errors.append("missing local configuration files must not be declared as Xcode phase inputs")
    if "scripts/config_security.py" not in project or "validate-local --root" not in project:
        errors.append("Xcode validation phase must call the canonical local-config validator")

    app_delegate = (root / "EmojiThrower/AppDelegate.swift").read_text()
    settings = (root / "EmojiThrower/SettingsHelper.swift").read_text()
    if "FIRApp.configure()" not in app_delegate:
        errors.append("Firebase initialization must remain explicit in AppDelegate")
    if 'path(forResource: "Config", ofType: "plist")' not in settings:
        errors.append("Twitter setup must continue loading the local Config.plist resource")

    makefile = (root / "Makefile").read_text()
    workflow = (root / ".github/workflows/check.yml").read_text()
    if "config_security.py audit" not in makefile or "unittest discover" not in makefile:
        errors.append("Makefile must run the security audit and regression tests")
    if "make check" not in workflow or "persist-credentials: false" not in workflow:
        errors.append("hosted baseline must run the canonical check with checkout credentials disabled")
    return errors


def print_errors(errors):
    for error in errors:
        print(f"error: {error}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("audit", "validate-local"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = (
        audit_repository(args.root.resolve())
        if args.command == "audit"
        else validate_local_configs(args.root.resolve())
    )
    if errors:
        print_errors(errors)
        return 1
    print("configuration security checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
