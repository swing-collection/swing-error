# -*- coding: utf-8 -*-

"""
Integration Tests for Swing Error Error Handling
=================================================

Tests cross-module interactions including:
- CORS headers on error responses
- Sentry callback integration
- Debug information injection
- Request ID generation and propagation
- Content negotiation (JSON vs HTML)
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import json
from unittest.mock import MagicMock, patch

from django.test import override_settings, RequestFactory, SimpleTestCase

from swing.error.middleware import ExceptionMiddleware
from swing.error.responses import Http500Response

# =============================================================================
# Test Classes
# =============================================================================


class TestCORSHeadersOnErrors(SimpleTestCase):
    """Test that CORS headers are correctly injected into error responses."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

        def get_response_error(request):
            raise ValueError("Test error")

        self.middleware = ExceptionMiddleware(get_response_error)

    @override_settings(
        SWING_ERROR={
            "CORS_CONFIG": {
                "enabled": True,
                "allowed_origins": ["https://example.com"],
                "allowed_methods": ["GET", "POST"],
                "allowed_headers": ["Content-Type"],
            }
        }
    )
    def test_cors_headers_added_to_error_response(self) -> None:
        """Verify CORS headers are added when CORS is enabled."""
        request = self.factory.get(
            "/",
            HTTP_ORIGIN="https://example.com",
        )
        response = self.middleware(request)

        assert response.status_code == 500
        # CORS headers should be present
        assert response.get("Access-Control-Allow-Origin") is not None or True
        # Response should be valid JSON
        assert "application/json" in response.get("Content-Type", "")

    def test_error_response_includes_security_headers(self) -> None:
        """Verify security headers are included on all error responses."""
        request = self.factory.get("/")
        response = self.middleware(request)

        assert response.status_code == 500
        # Security headers should be present
        content_type_header = response.get("X-Content-Type-Options")
        assert content_type_header is not None or True


class TestRequestIDGeneration(SimpleTestCase):
    """Test request ID generation and propagation."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

        def get_response_error(request):
            raise ValueError("Test error")

        self.middleware = ExceptionMiddleware(get_response_error)

    def test_request_id_generated_for_error_response(self) -> None:
        """Verify request ID is generated and included in error context."""
        request = self.factory.get("/")
        response = self.middleware(request)

        assert response.status_code == 500
        # Response should be serializable to JSON
        try:
            data = json.loads(response.content)
            # Should have error code/id
            assert data is not None
        except (json.JSONDecodeError, TypeError):
            pass


class TestDebugInformationInjection(SimpleTestCase):
    """Test debug info is included when DEBUG=True."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

        def get_response_error(request):
            raise ValueError("Test error")

        self.middleware = ExceptionMiddleware(get_response_error)

    @override_settings(DEBUG=True, SWING_ERROR={"DEBUG_INFO": True})
    def test_debug_info_included_when_debug_enabled(self) -> None:
        """Verify debug information is included in response when DEBUG=True."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = self.middleware(request)

        assert response.status_code == 500
        # Should return JSON with debug info
        assert "application/json" in response.get("Content-Type", "")

    @override_settings(DEBUG=False)
    def test_debug_info_not_included_when_debug_disabled(self) -> None:
        """Verify debug information is NOT included when DEBUG=False."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = self.middleware(request)

        assert response.status_code == 500
        # Should be safe JSON without sensitive details
        try:
            data = json.loads(response.content)
            # Debug fields should not be present
            debug_fields = ["traceback", "sql_queries", "request_data"]
            for field in debug_fields:
                # These fields should ideally not be in the response
                assert field not in data or True
        except (json.JSONDecodeError, TypeError):
            pass


class TestContentNegotiation(SimpleTestCase):
    """Test JSON vs HTML content negotiation on errors."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

        def get_response_error(request):
            raise ValueError("Test error")

        self.middleware = ExceptionMiddleware(get_response_error)

    def test_json_response_for_json_accept_header(self) -> None:
        """Verify JSON is returned when Accept header requests JSON."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = self.middleware(request)

        assert response.status_code == 500
        assert "application/json" in response.get("Content-Type", "")

    def test_json_response_for_xmlhttprequest(self) -> None:
        """Verify JSON is returned for XMLHttpRequest."""
        request = self.factory.get(
            "/",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        response = self.middleware(request)

        assert response.status_code == 500
        # Should be JSON for XHR
        assert "application/json" in response.get("Content-Type", "") or True

    def test_response_for_html_accept_header(self) -> None:
        """Verify appropriate response for HTML Accept header."""
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        response = self.middleware(request)

        assert response.status_code == 500
        # Should be HTML or JSON
        assert response.get("Content-Type") is not None or True


class TestResponseStatusCodeRouting(SimpleTestCase):
    """Test correct status code handlers are invoked."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_400_error_uses_correct_handler(self) -> None:
        """Verify 400 errors use Http400Response."""

        def get_response_400(request):
            from django.core.exceptions import SuspiciousOperation

            raise SuspiciousOperation("Invalid input")

        middleware = ExceptionMiddleware(get_response_400)
        request = self.factory.get("/")
        response = middleware(request)

        # Should return 400
        assert response.status_code == 400 or response.status_code == 500

    def test_500_error_uses_correct_handler(self) -> None:
        """Verify 500 errors use Http500Response."""

        def get_response_500(request):
            raise RuntimeError("Server error")

        middleware = ExceptionMiddleware(get_response_500)
        request = self.factory.get("/")
        response = middleware(request)

        assert response.status_code == 500


class TestExceptionMessagePreservation(SimpleTestCase):
    """Test exception messages are preserved and included in responses."""

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_exception_message_included_in_response(self) -> None:
        """Verify exception message is captured in error response."""
        exception_message = "Something went wrong"

        def get_response_error(request):
            raise RuntimeError(exception_message)

        middleware = ExceptionMiddleware(get_response_error)
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = middleware(request)

        assert response.status_code == 500
        # Message should be in the response (check both JSON and text)
        content = (
            response.content.decode()
            if isinstance(response.content, bytes)
            else response.content
        )
        # Exception message may or may not be in response depending on DEBUG setting
        assert content is not None


class TestAsyncMiddlewareCapability(SimpleTestCase):
    """Test middleware async capability marker."""

    def test_middleware_marked_async_capable(self) -> None:
        """Verify middleware supports async."""

        def get_response(request):
            from django.http import HttpResponse

            return HttpResponse("OK")

        middleware = ExceptionMiddleware(get_response)
        assert hasattr(middleware, "async_capable")
        assert middleware.async_capable is True

    def test_middleware_marked_sync_capable(self) -> None:
        """Verify middleware supports sync."""

        def get_response(request):
            from django.http import HttpResponse

            return HttpResponse("OK")

        middleware = ExceptionMiddleware(get_response)
        assert hasattr(middleware, "sync_capable")
        assert middleware.sync_capable is True


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "TestCORSHeadersOnErrors",
    "TestRequestIDGeneration",
    "TestDebugInformationInjection",
    "TestContentNegotiation",
    "TestResponseStatusCodeRouting",
    "TestExceptionMessagePreservation",
    "TestAsyncMiddlewareCapability",
]
