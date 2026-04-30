import pytest

from swing.error._utils.scrub_sensitive_data import scrub_sensitive_data


class TestScrubSensitiveData:
    def test_scrub_password_key(self) -> None:
        assert scrub_sensitive_data("secret", "password") == "[REDACTED]"

    def test_scrub_token_key(self) -> None:
        assert scrub_sensitive_data("abc123", "token") == "[REDACTED]"

    def test_scrub_authorization_value(self) -> None:
        assert scrub_sensitive_data("Bearer token123") == "[REDACTED]"

    def test_scrub_cookie_header_value(self) -> None:
        assert scrub_sensitive_data("sessionid=xyz; path=/", "cookie") == "[REDACTED]"

    def test_scrub_nested_dict_with_secrets(self) -> None:
        data = {
            "user": "john",
            "password": "secret123",
            "nested": {"token": "abc"},
        }
        result = scrub_sensitive_data(data)
        assert result["password"] == "[REDACTED]"
        assert result["nested"]["token"] == "[REDACTED]"
        assert result["user"] == "john"

    def test_scrub_list_with_secrets(self) -> None:
        data = ["public", "Bearer secret", "another"]
        result = scrub_sensitive_data(data)
        assert result[0] == "public"
        assert result[1] == "[REDACTED]"
        assert result[2] == "another"

    def test_scrub_tuple_with_secrets(self) -> None:
        data = ("public", "password:secret")
        result = scrub_sensitive_data(data)
        assert result[0] == "public"
        assert result[1] == "[REDACTED]"

    def test_scrub_mixed_nested_structure(self) -> None:
        data = {
            "auth": {
                "token": "secret",
                "methods": ["password", "oauth"],
            },
            "settings": {"debug": True},
        }
        result = scrub_sensitive_data(data)
        assert result["auth"]["token"] == "[REDACTED]"
        assert result["auth"]["methods"][0] == "[REDACTED]"
        assert result["settings"]["debug"] is True

    def test_scrub_none_key(self) -> None:
        assert scrub_sensitive_data("value", None) == "value"

    def test_scrub_non_string_values(self) -> None:
        assert scrub_sensitive_data(123) == 123
        assert scrub_sensitive_data(45.67) == 45.67
        assert scrub_sensitive_data(True) is True
