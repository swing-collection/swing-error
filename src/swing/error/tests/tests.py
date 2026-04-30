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
]
