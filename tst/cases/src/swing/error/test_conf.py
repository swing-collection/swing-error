from django.test import SimpleTestCase

from swing.error.conf import (
    DEFAULT_ERROR_SETTINGS,
    get_all_error_types,
    get_error_config,
)


class TestConf(SimpleTestCase):
    def test_default_error_settings_has_all_codes(self) -> None:
        expected_codes = [
            "base",
            "400",
            "401",
            "403",
            "404",
            "405",
            "408",
            "410",
            "429",
            "500",
        ]
        for code in expected_codes:
            assert code in DEFAULT_ERROR_SETTINGS

    def test_get_error_config_returns_default_value(self) -> None:
        assert get_error_config("404", "default_message") == "Page Not Found"

    def test_get_error_config_falls_back_to_base(self) -> None:
        assert (
            get_error_config("999", "default_message") == "An error occurred"
        )

    def test_get_error_config_returns_explicit_default(self) -> None:
        assert (
            get_error_config("404", "missing_key", default="fallback")
            == "fallback"
        )

    def test_get_all_error_types_excludes_base(self) -> None:
        error_types = get_all_error_types()
        assert "400" in error_types
        assert "500" in error_types
        assert "base" not in error_types

    def test_get_error_config_uses_user_settings_override(self) -> None:
        with self.settings(
            ERROR_HANDLER_CONFIG={
                "404": {"default_message": "Custom Not Found"}
            }
        ):
            assert (
                get_error_config("404", "default_message")
                == "Custom Not Found"
            )
