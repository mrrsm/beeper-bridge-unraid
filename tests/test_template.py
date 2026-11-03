import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TemplateTest(unittest.TestCase):
    def setUp(self):
        self.root = ET.parse(ROOT / "beeper-bridge.xml").getroot()

    def text(self, tag):
        element = self.root.find(tag)
        self.assertIsNotNone(element, tag)
        return (element.text or "").strip()

    def test_gitignore_ignores_superpowers(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("docs/superpowers", gitignore)

    def test_container_settings(self):
        self.assertEqual(self.text("Name"), "beeper-bridge")
        self.assertEqual(self.text("Repository"), "ghcr.io/beeper/bridge-manager:latest")
        self.assertEqual(self.text("Registry"), "https://github.com/beeper/bridge-manager")
        self.assertEqual(self.text("Network"), "bridge")
        self.assertEqual(self.text("Shell"), "bash")
        self.assertEqual(self.text("Privileged"), "false")
        self.assertEqual(self.text("Category"), "Productivity:")
        self.assertEqual(self.text("Support"), "https://developers.beeper.com/bridges/self-hosting/")
        self.assertEqual(self.text("Project"), "https://github.com/beeper/bridge-manager")

    def test_empty_fields(self):
        for tag in ("WebUI", "TemplateURL", "Icon", "ExtraParams", "PostArgs"):
            self.assertEqual(self.text(tag), "")

    def test_only_three_configs_and_no_ports(self):
        targets = [element.get("Target") for element in self.root.findall("Config")]
        self.assertEqual(targets, ["BRIDGE_NAME", "MATRIX_ACCESS_TOKEN", "/data"])
        self.assertEqual(self.root.findall("Config[@Type='Port']"), [])

    def test_bridge_name(self):
        field = self.root.find("Config[@Target='BRIDGE_NAME']")
        self.assertEqual(field.get("Type"), "Variable")
        self.assertEqual(field.get("Default"), "sh-whatsapp")
        self.assertEqual(field.get("Required"), "true")
        self.assertEqual(field.get("Mask"), "false")
        self.assertEqual(field.get("Display"), "always")
        self.assertEqual((field.text or "").strip(), "sh-whatsapp")

    def test_token_is_masked_and_empty(self):
        field = self.root.find("Config[@Target='MATRIX_ACCESS_TOKEN']")
        self.assertEqual(field.get("Type"), "Variable")
        self.assertEqual(field.get("Required"), "true")
        self.assertEqual(field.get("Mask"), "true")
        self.assertEqual(field.get("Display"), "always")
        self.assertEqual((field.text or "").strip(), "")

    def test_shared_appdata(self):
        field = self.root.find("Config[@Target='/data']")
        self.assertEqual(field.get("Type"), "Path")
        self.assertEqual(field.get("Mode"), "rw")
        self.assertEqual(field.get("Required"), "true")
        self.assertEqual(field.get("Display"), "always")
        self.assertEqual(field.get("Default"), "/mnt/user/appdata/beeper-bridge")
        self.assertEqual((field.text or "").strip(), "/mnt/user/appdata/beeper-bridge")
        description = field.get("Description")
        self.assertIn("same folder", description)
        self.assertIn("bridge names differ", description)

    def test_overview(self):
        overview = self.text("Overview")
        self.assertIn("same appdata folder", overview)
        self.assertIn("new container name", overview)
        self.assertIn("new bridge name", overview)
        self.assertIn("#self-hosting:beeper.com", overview)
        self.assertIn("https://developers.beeper.com/bridges/self-hosting/", overview)
