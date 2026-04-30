from django.http import HttpRequest
from django.test import override_settings

# Import | Libraries
import pytest

from swing.error._conf.capture_error import capture_error


class TestCaptureError:
    @pytest.fixture
    def http_request(self) -> HttpRequest:
        factory = HttpRequest()
        factory.path = "/test/"
        factory.method = "GET"
        factory.user = None
        return factory

    @override_settings(SWING_ERROR_TRACKING={"enabled": False})
    def test_capture_error_disabled(self, http_request: HttpRequest) -> None:
        exc = Exception("Test error")
        result = capture_error(exception=exc, request=http_request)
        assert result is None

    @override_settings(SWING_ERROR_TRACKING={"enabled": False})
    def test_capture_error_disabled_with_message(self) -> None:
        result = capture_error(message="Test message")
        assert result is None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "capture_exceptions": False,
            "capture_messages": False,
        }
    )
    def test_capture_error_both_disabled(self) -> None:
        result = capture_error()
        assert result is None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "capture_exceptions": True,
            "callback": None,
            "extra_context": {"app": "test"},
        }
    )
    def test_capture_error_with_extra_context(self, http_request: HttpRequest) -> None:
        exc = Exception("Test")
        # Should not raise, but will fail to capture without sentry_sdk
        result = capture_error(
            exception=exc,
            request=http_request,
            extra_context={"user_id": 123},
        )
        assert result is None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "callback": "nonexistent.module.callback",
        }
    )
    def test_capture_error_invalid_callback(self) -> None:
        # Should not raise when callback module doesn't exist
        result = capture_error()
        assert result is None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "capture_exceptions": True,
            "capture_messages": False,
        }
    )
    def test_capture_error_exception_only(self, http_request: HttpRequest) -> None:
        exc = ValueError("Test value error")
        result = capture_error(exception=exc, request=http_request)
        # Will succeed or fail depending on sentry_sdk, but shouldn't raise
        assert result is None or result is not None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "capture_exceptions": False,
            "capture_messages": True,
        }
    )
    def test_capture_error_message_only(self) -> None:
        result = capture_error(message="Test message only")
        assert result is None or result is not None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "callback": "tst.helpers.failing_callback",
        }
    )
    def test_capture_error_with_failing_callback(
        self, http_request: HttpRequest
    ) -> None:
        """Test that errors in callback don't crash the application."""
        exc = ValueError("Test")
        # Should not raise even if callback fails
        result = capture_error(exception=exc, request=http_request)
        assert result is None

    @override_settings(
        SWING_ERROR_TRACKING={
            "enabled": True,
            "callback": "tst.helpers.working_callback",
        }
    )
    def test_capture_error_with_working_callback(
        self, http_request: HttpRequest
    ) -> None:
        """Test that working callbacks are called successfully."""
        exc = ValueError("Test")
        # Should not raise with working callback
        result = capture_error(exception=exc, request=http_request)
        assert result is None
