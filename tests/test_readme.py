import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUPPORTED_IDS = (
    "telegram",
    "whatsapp",
    "signal",
    "discord",
    "slack",
    "gmessages",
    "googlemessages",
    "rcs",
    "sms",
    "gvoice",
    "googlevoice",
    "meta",
    "instagram",
    "facebook",
    "googlechat",
    "gchat",
    "twitter",
    "bluesky",
    "bsky",
    "linkedin",
    "heisenbridge",
    "irc",
)


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_token_sources(self):
        self.assertIn("Help", self.readme)
        self.assertIn("~/.config/bbctl/config.json", self.readme)
        self.assertIn("access_token", self.readme)

    def test_install_and_second_bridge(self):
        self.assertIn("/boot/config/plugins/dockerMan/templates-user/", self.readme)
        self.assertIn("beeper-bridge.xml", self.readme)
        self.assertIn("/mnt/user/appdata/beeper-bridge", self.readme)
        self.assertIn("new container name", self.readme)
        self.assertIn("new bridge name", self.readme)
        self.assertIn("bridge names differ", self.readme)
        self.assertIn("autostart", self.readme.lower())

    def test_supported_identifiers(self):
        for bridge_id in SUPPORTED_IDS:
            self.assertIn(f"`{bridge_id}`", self.readme)

    def test_imessage_is_unsupported(self):
        self.assertIn("iMessage Go", self.readme)
        self.assertIn("not supported", self.readme)
        supported = self.readme.split("## Supported bridges", 1)[1].split("## ", 1)[0]
        self.assertNotIn("`imessage`", supported)
        self.assertNotIn("`imessagego`", supported)

    def test_login_and_layout(self):
        self.assertIn("@sh-whatsappbot:beeper.local", self.readme)
        self.assertIn("`/data/sh-whatsapp`", self.readme)
        self.assertIn("/data/db/", self.readme)
        self.assertIn("`/data/binaries`", self.readme)

    def test_removal(self):
        self.assertIn("bbctl delete sh-<name>", self.readme)
        self.assertIn("`/data/db/<bridge name>-<program>.db`", self.readme)
        self.assertIn(
            "/mnt/user/appdata/beeper-bridge/db/sh-whatsapp-mautrix-whatsapp.db",
            self.readme,
        )
        self.assertIn(
            "/mnt/user/appdata/beeper-bridge/db/sh-whatsapp-mautrix-whatsapp.db-wal",
            self.readme,
        )
        self.assertIn(
            "/mnt/user/appdata/beeper-bridge/db/sh-whatsapp-mautrix-whatsapp.db-shm",
            self.readme,
        )
        self.assertIn("`sh-whatsapp-work-mautrix-whatsapp.db`", self.readme)
        self.assertIn("`mautrix-telegram`", self.readme)
        self.assertIn("`mautrix-googlechat`", self.readme)
        self.assertIn("`mautrix-meta`", self.readme)

    def test_log_messages(self):
        self.assertIn("BRIDGE_NAME not set", self.readme)
        self.assertIn("MATRIX_ACCESS_TOKEN not set", self.readme)
