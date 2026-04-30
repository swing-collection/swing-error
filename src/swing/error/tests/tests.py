# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error Tests
=================

Comprehensive test suite for the swing.error Django application.

This module tests:
- Response classes (Http400Response, Http401Response, etc.)
- Configuration system (conf.py)
- Utility functions (utils.py)
- Content negotiation

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import json
from unittest.mock import MagicMock, patch

from django.http import HttpRequest
from django.test import RequestFactory, TestCase

# Import | Local
from ..conf import (
    DEFAULT_ERROR_SETTINGS,
    get_all_error_types,
    get_error_config,
)
from ..responses import (
    Http400Response,
    Http401Response,
    Http403Response,
    Http404Response,
    Http405Response,
    Http408Response,
    Http410Response,
    Http429Response,
    Http500Response,
)
from ..utils import (
    generate_request_id,
    get_client_ip,
    get_preferred_content_type,
    get_request_id,
    wants_html,
    wants_json,
)

# =============================================================================
# Test Response Classes
# =============================================================================


class TestHttp400Response(TestCase):
    """Tests for Http400Response class."""

    def test_default_status_code(self):
        """Test that default status code is 400."""
        response = Http400Response()
        self.assertEqual(response.status_code, 400)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http400Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Bad Request")

    def test_custom_message(self):
        """Test custom message is used."""
        response = Http400Response(message="Custom error message")
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Custom error message")

    def test_with_details(self):
        """Test response with details."""
        details = {"field": "email", "error": "Invalid format"}
        response = Http400Response(details=details)
        content = json.loads(response.content)
        self.assertEqual(content["details"], details)

    def test_json_content_type(self):
        """Test that content type is JSON."""
        response = Http400Response()
        self.assertEqual(response["Content-Type"], "application/json")


class TestHttp401Response(TestCase):
    """Tests for Http401Response class."""

    def test_default_status_code(self):
        """Test that default status code is 401."""
        response = Http401Response()
        self.assertEqual(response.status_code, 401)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http401Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Unauthorized")


class TestHttp403Response(TestCase):
    """Tests for Http403Response class."""

    def test_default_status_code(self):
        """Test that default status code is 403."""
        response = Http403Response()
        self.assertEqual(response.status_code, 403)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http403Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Forbidden")


class TestHttp404Response(TestCase):
    """Tests for Http404Response class."""

    def test_default_status_code(self):
        """Test that default status code is 404."""
        response = Http404Response()
        self.assertEqual(response.status_code, 404)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http404Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Not Found")


class TestHttp405Response(TestCase):
    """Tests for Http405Response class."""

    def test_default_status_code(self):
        """Test that default status code is 405."""
        response = Http405Response()
        self.assertEqual(response.status_code, 405)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http405Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Method Not Allowed")


class TestHttp408Response(TestCase):
    """Tests for Http408Response class."""

    def test_default_status_code(self):
        """Test that default status code is 408."""
        response = Http408Response()
        self.assertEqual(response.status_code, 408)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http408Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Request Timeout")


class TestHttp410Response(TestCase):
    """Tests for Http410Response class."""

    def test_default_status_code(self):
        """Test that default status code is 410."""
        response = Http410Response()
        self.assertEqual(response.status_code, 410)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http410Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Gone")


class TestHttp429Response(TestCase):
    """Tests for Http429Response class."""

    def test_default_status_code(self):
        """Test that default status code is 429."""
        response = Http429Response()
        self.assertEqual(response.status_code, 429)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http429Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Too Many Requests")

    def test_retry_after_header(self):
        """Test Retry-After header is set."""
        response = Http429Response(retry_after=60)
        self.assertEqual(response["Retry-After"], "60")

    def test_no_retry_after_header_by_default(self):
        """Test Retry-After header is not set by default."""
        response = Http429Response()
        self.assertNotIn("Retry-After", response)


class TestHttp500Response(TestCase):
    """Tests for Http500Response class."""

    def test_default_status_code(self):
        """Test that default status code is 500."""
        response = Http500Response()
        self.assertEqual(response.status_code, 500)

    def test_default_message(self):
        """Test that default message is set."""
        response = Http500Response()
        content = json.loads(response.content)
        self.assertEqual(content["error"], "Internal Server Error")


# =============================================================================
# Test Configuration
# =============================================================================


class TestConfiguration(TestCase):
    """Tests for configuration module."""

    def test_default_error_settings_has_all_codes(self):
        """Test that all error codes have default settings."""
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
            self.assertIn(code, DEFAULT_ERROR_SETTINGS)

    def test_get_error_config_returns_default(self):
        """Test get_error_config returns default values."""
        message = get_error_config("404", "default_message")
        self.assertEqual(message, "Page Not Found")

    def test_get_error_config_falls_back_to_base(self):
        """Test get_error_config falls back to base for unknown types."""
        message = get_error_config("999", "default_message")
        self.assertEqual(message, "An error occurred")

    def test_get_error_config_returns_default_on_missing_key(self):
        """Test get_error_config returns default for missing keys."""
        value = get_error_config("404", "nonexistent_key", default="fallback")
        self.assertEqual(value, "fallback")

    def test_get_all_error_types(self):
        """Test get_all_error_types returns all codes except base."""
        types = get_all_error_types()
        self.assertIn("400", types)
        self.assertIn("500", types)
        self.assertNotIn("base", types)

    def test_get_error_config_uses_user_settings(self):
        """Test get_error_config uses user settings override."""
        with self.settings(
            ERROR_HANDLER_CONFIG={
                "404": {"default_message": "Custom Not Found"}
            }
        ):
            message = get_error_config("404", "default_message")
            self.assertEqual(message, "Custom Not Found")


# =============================================================================
# Test Utilities
# =============================================================================


class TestContentNegotiation(TestCase):
    """Tests for content negotiation utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_wants_json_with_json_accept_header(self):
        """Test wants_json returns True for JSON Accept header."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        self.assertTrue(wants_json(request))

    def test_wants_json_with_html_accept_header(self):
        """Test wants_json returns False for HTML Accept header."""
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        self.assertFalse(wants_json(request))

    def test_wants_json_with_xhr_header(self):
        """Test wants_json returns True for XHR requests."""
        request = self.factory.get(
            "/", HTTP_ACCEPT="*/*", HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertTrue(wants_json(request))

    def test_wants_html_with_html_accept_header(self):
        """Test wants_html returns True for HTML Accept header."""
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        self.assertTrue(wants_html(request))

    def test_wants_html_with_json_accept_header(self):
        """Test wants_html returns False for JSON Accept header."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        self.assertFalse(wants_html(request))

    def test_get_preferred_content_type_json(self):
        """Test get_preferred_content_type returns 'json' for API requests."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        self.assertEqual(get_preferred_content_type(request), "json")

    def test_get_preferred_content_type_html(self):
        """Test get_preferred_content_type returns 'html' for browser requests."""
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        self.assertEqual(get_preferred_content_type(request), "html")


class TestRequestTracking(TestCase):
    """Tests for request tracking utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_generate_request_id_is_unique(self):
        """Test generate_request_id returns unique IDs."""
        id1 = generate_request_id()
        id2 = generate_request_id()
        self.assertNotEqual(id1, id2)

    def test_get_request_id_uses_existing_header(self):
        """Test get_request_id uses existing X-Request-ID header."""
        request = self.factory.get("/", HTTP_X_REQUEST_ID="existing-id-123")
        self.assertEqual(get_request_id(request), "existing-id-123")

    def test_get_request_id_generates_new_if_missing(self):
        """Test get_request_id generates new ID if header missing."""
        request = self.factory.get("/")
        request_id = get_request_id(request)
        self.assertIsNotNone(request_id)
        self.assertGreater(len(request_id), 0)


class TestClientIP(TestCase):
    """Tests for client IP utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_get_client_ip_from_remote_addr(self):
        """Test get_client_ip uses REMOTE_ADDR."""
        request = self.factory.get("/", REMOTE_ADDR="192.168.1.1")
        self.assertEqual(get_client_ip(request), "192.168.1.1")

    def test_get_client_ip_from_x_forwarded_for(self):
        """Test get_client_ip uses X-Forwarded-For header."""
        request = self.factory.get(
            "/",
            HTTP_X_FORWARDED_FOR="10.0.0.1, 192.168.1.1",
            REMOTE_ADDR="127.0.0.1",
        )
        self.assertEqual(get_client_ip(request), "10.0.0.1")

    def test_get_client_ip_from_x_real_ip(self):
        """Test get_client_ip uses X-Real-IP header."""
        request = self.factory.get(
            "/", HTTP_X_REAL_IP="10.0.0.2", REMOTE_ADDR="127.0.0.1"
        )
        self.assertEqual(get_client_ip(request), "10.0.0.2")


# =============================================================================
# Test View Handlers
# =============================================================================


class TestViewHandlers(TestCase):
    """Tests for error handler views."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_handler_401_view_returns_401_status(self):
        """Test Handler401View returns 401 status code."""
        from ..views.view_error_handler_401 import Handler401View

        view = Handler401View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_handler_401_view_returns_json(self):
        """Test Handler401View returns JSON when Accept header is application/json."""
        from ..views.view_error_handler_401 import Handler401View

        view = Handler401View.as_view()
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = view(request)
        self.assertIn("application/json", response.get("Content-Type", ""))

    def test_handler_403_view_returns_403_status(self):
        """Test Handler403View returns 403 status code."""
        from ..views.view_error_handler_403 import Handler403View

        view = Handler403View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_handler_404_view_returns_404_status(self):
        """Test Handler404View returns 404 status code."""
        from ..views.view_error_handler_404 import Handler404View

        view = Handler404View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 404)

    def test_handler_405_view_returns_405_status(self):
        """Test Handler405View returns 405 status code."""
        from ..views.view_error_handler_405 import Handler405View

        view = Handler405View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 405)

    def test_handler_408_view_returns_408_status(self):
        """Test Handler408View returns 408 status code."""
        from ..views.view_error_handler_408 import Handler408View

        view = Handler408View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 408)

    def test_handler_410_view_returns_410_status(self):
        """Test Handler410View returns 410 status code."""
        from ..views.view_error_handler_410 import Handler410View

        view = Handler410View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 410)

    def test_handler_429_view_returns_429_status(self):
        """Test Handler429View returns 429 status code."""
        from ..views.view_error_handler_429 import Handler429View

        view = Handler429View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 429)

    def test_handler_500_view_returns_500_status(self):
        """Test Handler500View returns 500 status code."""
        from ..views.view_error_handler_500 import Handler500View

        view = Handler500View.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, 500)

    def test_all_handlers_extend_base_error_view(self):
        """Test all handlers are instances of BaseErrorView."""
        from ..views.view_error_handler_base import BaseErrorView
        from ..views.view_error_handler_401 import Handler401View
        from ..views.view_error_handler_403 import Handler403View
        from ..views.view_error_handler_404 import Handler404View
        from ..views.view_error_handler_405 import Handler405View
        from ..views.view_error_handler_408 import Handler408View
        from ..views.view_error_handler_410 import Handler410View
        from ..views.view_error_handler_429 import Handler429View
        from ..views.view_error_handler_500 import Handler500View

        for ViewClass in [
            Handler401View,
            Handler403View,
            Handler404View,
            Handler405View,
            Handler408View,
            Handler410View,
            Handler429View,
            Handler500View,
        ]:
            self.assertTrue(issubclass(ViewClass, BaseErrorView))

    def test_handler_401_uses_http401_response(self):
        """Test Handler401View uses Http401Response class."""
        from ..views.view_error_handler_401 import Handler401View

        self.assertEqual(Handler401View.response_class, Http401Response)

    def test_handler_403_uses_http403_response(self):
        """Test Handler403View uses Http403Response class."""
        from ..views.view_error_handler_403 import Handler403View
        from ..responses.response_http_403 import Http403Response

        self.assertEqual(Handler403View.response_class, Http403Response)

    def test_handler_404_uses_http404_response(self):
        """Test Handler404View uses Http404Response class."""
        from ..views.view_error_handler_404 import Handler404View
        from ..responses.response_http_404 import Http404Response

        self.assertEqual(Handler404View.response_class, Http404Response)

    def test_handler_error_types_set_correctly(self):
        """Test all handlers have error_type attribute set correctly."""
        from ..views.view_error_handler_401 import Handler401View
        from ..views.view_error_handler_403 import Handler403View
        from ..views.view_error_handler_404 import Handler404View
        from ..views.view_error_handler_405 import Handler405View
        from ..views.view_error_handler_408 import Handler408View
        from ..views.view_error_handler_410 import Handler410View
        from ..views.view_error_handler_429 import Handler429View
        from ..views.view_error_handler_500 import Handler500View

        handlers = {
            Handler401View: "401",
            Handler403View: "403",
            Handler404View: "404",
            Handler405View: "405",
            Handler408View: "408",
            Handler410View: "410",
            Handler429View: "429",
            Handler500View: "500",
        }

        for ViewClass, expected_code in handlers.items():
            self.assertEqual(ViewClass.error_type, expected_code)


# =============================================================================
# Test Middleware
# =============================================================================


class TestExceptionMiddleware(TestCase):
    """Tests for ExceptionMiddleware."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
        from ..middleware import ExceptionMiddleware

        # Create a mock get_response that doesn't raise
        def get_response_ok(request):
            from django.http import HttpResponse
            return HttpResponse("OK", status=200)

        self.middleware = ExceptionMiddleware(get_response_ok)

        # Create a mock get_response that raises
        def get_response_error(request):
            raise ValueError("Test exception")

        self.middleware_error = ExceptionMiddleware(get_response_error)

    def test_middleware_returns_200_for_ok_response(self):
        """Test middleware passes through OK responses."""
        request = self.factory.get("/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_middleware_handles_unhandled_exception(self):
        """Test middleware catches unhandled exceptions and returns 500."""
        request = self.factory.get("/")
        response = self.middleware_error(request)
        self.assertEqual(response.status_code, 500)

    def test_middleware_returns_json_for_exception(self):
        """Test middleware returns JSON response for exceptions."""
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = self.middleware_error(request)
        self.assertIn("application/json", response.get("Content-Type", ""))
        content = json.loads(response.content)
        self.assertIn("error", content)

    def test_middleware_with_401_response(self):
        """Test middleware handles 401 responses."""
        from ..middleware import ExceptionMiddleware

        def get_401_response(request):
            return Http401Response()

        middleware = ExceptionMiddleware(get_401_response)
        request = self.factory.get("/")
        response = middleware(request)
        # The middleware should handle the 401 response
        self.assertEqual(response.status_code, 401)

    def test_middleware_with_404_response(self):
        """Test middleware handles 404 responses."""
        from ..middleware import ExceptionMiddleware

        def get_404_response(request):
            return Http404Response()

        middleware = ExceptionMiddleware(get_404_response)
        request = self.factory.get("/")
        response = middleware(request)
        self.assertEqual(response.status_code, 404)

    def test_middleware_with_500_response(self):
        """Test middleware handles 500 responses."""
        from ..middleware import ExceptionMiddleware

        def get_500_response(request):
            return Http500Response()

        middleware = ExceptionMiddleware(get_500_response)
        request = self.factory.get("/")
        response = middleware(request)
        self.assertEqual(response.status_code, 500)


# =============================================================================
# Test Integration
# =============================================================================


class TestIntegration(TestCase):
    """Integration tests for CORS, error tracking, and debug mode."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    @patch("swing.error.conf.get_cors_config")
    def test_cors_headers_on_error_response(self, mock_cors_config):
        """Test CORS headers are added to error responses."""
        # Mock CORS configuration
        mock_cors_config.return_value = {
            "enabled": True,
            "allowed_origins": "*",
            "allowed_methods": ["GET", "POST", "OPTIONS"],
            "allowed_headers": ["Content-Type", "Authorization"],
        }

        # Create a response with CORS
        request = self.factory.options(
            "/api/endpoint",
            HTTP_ORIGIN="http://example.com",
        )
        response = Http401Response(request=request)

        # Verify response has CORS headers
        self.assertIn("Access-Control-Allow-Origin", response)

    def test_error_response_with_request_context(self):
        """Test error response includes request context when provided."""
        request = self.factory.get("/api/test", HTTP_ACCEPT="application/json")
        response = Http400Response(request=request)
        content = json.loads(response.content)

        # Should have error structure
        self.assertIn("error", content)
        self.assertIn("details", content)

    def test_multiple_error_codes_in_middleware_chain(self):
        """Test middleware handles multiple different error codes."""
        from ..middleware import ExceptionMiddleware

        error_codes = [400, 401, 403, 404, 405, 408, 410, 429, 500]

        for code in error_codes:
            # Create a response with the specific code
            def get_response_with_code(status_code):
                def inner(request):
                    from django.http import HttpResponse

                    resp = HttpResponse(f"Error {status_code}", status=status_code)
                    return resp

                return inner

            middleware = ExceptionMiddleware(get_response_with_code(code))
            request = self.factory.get("/")
            response = middleware(request)

            # Middleware should handle all status codes
            self.assertIsNotNone(response)

    def test_view_handler_chain_integration(self):
        """Test all view handlers work in succession."""
        from ..views.view_error_handler_401 import Handler401View
        from ..views.view_error_handler_403 import Handler403View
        from ..views.view_error_handler_404 import Handler404View

        views = [Handler401View, Handler403View, Handler404View]
        expected_codes = [401, 403, 404]

        for view_class, expected_code in zip(views, expected_codes):
            view = view_class.as_view()
            request = self.factory.get("/")
            response = view(request)
            self.assertEqual(response.status_code, expected_code)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "TestHttp400Response",
    "TestHttp401Response",
    "TestHttp403Response",
    "TestHttp404Response",
    "TestHttp405Response",
    "TestHttp408Response",
    "TestHttp410Response",
    "TestHttp429Response",
    "TestHttp500Response",
    "TestConfiguration",
    "TestContentNegotiation",
    "TestRequestTracking",
    "TestClientIP",
    "TestViewHandlers",
    "TestExceptionMiddleware",
    "TestIntegration",
]
