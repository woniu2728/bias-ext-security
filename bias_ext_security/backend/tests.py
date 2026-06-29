import json

from django.test import TestCase

from bias_core.extensions.runtime import get_runtime_human_verification_handlers
from bias_core.extensions.testing import (
    Setting,
    bootstrap_enabled_extension_application,
    clear_runtime_setting_caches,
    get_extension_settings_definition,
)
from bias_ext_security.backend.human_verification import verify_human_verification


class SecurityExtensionTests(TestCase):
    def setUp(self):
        clear_runtime_setting_caches()

    def tearDown(self):
        clear_runtime_setting_caches()
        super().tearDown()

    def test_security_extension_registers_human_verification_handler(self):
        bootstrap_enabled_extension_application("security")

        handlers = get_runtime_human_verification_handlers()

        self.assertIs(handlers["turnstile"], verify_human_verification)

    def test_security_settings_definition_keeps_secret_server_side(self):
        bootstrap_enabled_extension_application("security")

        definition = get_extension_settings_definition("security")

        self.assertEqual(definition["defaults"]["auth_human_verification_provider"], "off")
        self.assertEqual(definition["defaults"]["auth_human_verification_login_enabled"], True)
        self.assertEqual(definition["defaults"]["auth_human_verification_register_enabled"], True)
        self.assertIn("auth_turnstile_secret_key", definition["defaults"])
        self.assertNotIn("auth_turnstile_secret_key", definition["forum_settings_keys"])

    def test_public_forum_settings_expose_only_public_turnstile_config(self):
        bootstrap_enabled_extension_application("security")
        values = {
            "auth_human_verification_provider": "turnstile",
            "auth_turnstile_site_key": "site-key",
            "auth_turnstile_secret_key": "secret-key",
            "auth_human_verification_login_enabled": True,
            "auth_human_verification_register_enabled": False,
        }
        for key, value in values.items():
            Setting.objects.update_or_create(
                key=f"extensions.security.{key}",
                defaults={"value": json.dumps(value)},
            )
        clear_runtime_setting_caches()

        response = self.client.get("/api/forum")

        self.assertEqual(response.status_code, 200, response.content)
        payload = response.json()
        security_extension = next(item for item in payload["enabled_extensions"] if item["id"] == "security")
        self.assertEqual(security_extension["frontend_forum_entry"], "extensions/security/frontend/forum/index.js")
        self.assertEqual(
            security_extension["forum_settings"],
            {
                "auth_human_verification_provider": "turnstile",
                "auth_turnstile_site_key": "site-key",
                "auth_human_verification_login_enabled": True,
                "auth_human_verification_register_enabled": False,
            },
        )
        self.assertNotIn("auth_turnstile_secret_key", security_extension["forum_settings"])
