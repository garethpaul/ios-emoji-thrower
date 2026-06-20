import importlib.util
import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "config_security.py"


def load_module():
    spec = importlib.util.spec_from_file_location("config_security", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConfigSecurityTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_repository_contract_passes(self):
        self.assertEqual([], self.module.audit_repository(ROOT))

    def test_local_validation_rejects_missing_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.module.validate_local_configs(Path(directory))

        self.assertEqual(
            [
                "missing EmojiThrower/GoogleService-Info.plist; copy the sanitized example and download your own Firebase configuration",
                "missing EmojiThrower/Config.plist; copy the sanitized example and add your own Twitter consumer credentials",
            ],
            errors,
        )

    def test_local_validation_rejects_placeholders(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_plist(
                root / "EmojiThrower" / "GoogleService-Info.plist",
                self.module.firebase_example(),
            )
            self.write_plist(
                root / "EmojiThrower" / "Config.plist",
                self.module.twitter_example(),
            )

            errors = self.module.validate_local_configs(root)

        self.assertTrue(any("placeholder" in error for error in errors))
        self.assertFalse(any("REPLACE_WITH" in error for error in errors))

    def test_local_validation_accepts_complete_non_placeholder_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            firebase = self.module.firebase_example()
            twitter = self.module.twitter_example()
            firebase = {
                key: self.non_placeholder(value, key)
                for key, value in firebase.items()
            }
            twitter = {
                key: self.non_placeholder(value, key)
                for key, value in twitter.items()
            }
            firebase["BUNDLE_ID"] = "fixture.example.app"
            self.write_plist(root / "EmojiThrower" / "GoogleService-Info.plist", firebase)
            self.write_plist(root / "EmojiThrower" / "Config.plist", twitter)
            self.write_project(root, "fixture.example.app")

            errors = self.module.validate_local_configs(root)

        self.assertEqual([], errors)

    def test_local_validation_rejects_mismatched_bundle_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            firebase = {
                key: self.non_placeholder(value, key)
                for key, value in self.module.firebase_example().items()
            }
            twitter = {
                key: self.non_placeholder(value, key)
                for key, value in self.module.twitter_example().items()
            }
            firebase["BUNDLE_ID"] = "fixture.wrong.app"
            self.write_plist(root / "EmojiThrower" / "GoogleService-Info.plist", firebase)
            self.write_plist(root / "EmojiThrower" / "Config.plist", twitter)
            self.write_project(root, "fixture.expected.app")

            errors = self.module.validate_local_configs(root)

        self.assertEqual(
            ["GoogleService-Info.plist BUNDLE_ID does not match the Xcode product bundle identifier"],
            errors,
        )

    def test_project_validation_phase_is_first_and_has_no_missing_config_inputs(self):
        project = (ROOT / "EmojiThrower.xcodeproj/project.pbxproj").read_text()
        build_phases = project.split("buildPhases = (", 1)[1].split(");", 1)[0]
        first_phase = next(line.strip() for line in build_phases.splitlines() if "/*" in line)
        validation_block = project.split(
            "A3F0C1112C00000100000001 /* Validate local provider configuration */ = {",
            1,
        )[1].split("\n\t\t};", 1)[0]

        self.assertIn("Validate local provider configuration", first_phase)
        self.assertNotIn("GoogleService-Info.plist", validation_block)
        self.assertNotIn("EmojiThrower/Config.plist", validation_block)

    def test_audit_rejects_tracked_runtime_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            tracked = root / "EmojiThrower" / "GoogleService-Info.plist"
            self.write_plist(tracked, {"API_KEY": "fixture-value"})
            subprocess.run(["git", "-C", root, "add", tracked], check=True)

            errors = self.module.tracked_config_errors(root)

        self.assertEqual(
            ["tracked runtime configuration is forbidden: EmojiThrower/GoogleService-Info.plist"],
            errors,
        )

    @staticmethod
    def write_plist(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            plistlib.dump(value, handle)

    @staticmethod
    def write_project(root, bundle_id):
        path = root / "EmojiThrower.xcodeproj" / "project.pbxproj"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"PRODUCT_BUNDLE_IDENTIFIER = {bundle_id};\n")

    @staticmethod
    def non_placeholder(value, key):
        if isinstance(value, bool):
            return value
        return f"fixture-{key.lower()}"


if __name__ == "__main__":
    unittest.main()
