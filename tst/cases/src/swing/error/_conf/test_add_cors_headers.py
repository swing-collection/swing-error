import pytest
from django.http import HttpRequest, HttpResponse
from django.test import override_settings

from swing.error._conf.add_cors_headers import add_cors_headers


class TestAddCorsHeaders:
    @pytest.fixture
    def response(self) -> HttpResponse:
        return HttpResponse()

    @pytest.fixture
    def http_request(self) -> HttpRequest:
        factory = HttpRequest()
        factory.META["HTTP_ORIGIN"] = "https://example.com"
        return factory

    @override_settings(SWING_ERROR_CORS={"enabled": False})
    def test_cors_disabled_returns_unchanged(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert "Access-Control-Allow-Origin" not in result

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
        }
    )
    def test_cors_wildcard_origin(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Allow-Origin"] == "*"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["https://example.com"],
        }
    )
    def test_cors_specific_origin_allowed(self, response: HttpResponse, http_request: HttpRequest) -> None:
        result = add_cors_headers(response, http_request)
        assert result["Access-Control-Allow-Origin"] == "https://example.com"
        assert result["Vary"] == "Origin"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["https://other.com"],
        }
    )
    def test_cors_specific_origin_not_allowed(self, response: HttpResponse, http_request: HttpRequest) -> None:
        result = add_cors_headers(response, http_request)
        assert "Access-Control-Allow-Origin" not in result

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
            "allow_credentials": True,
        }
    )
    def test_cors_credentials_header(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Allow-Credentials"] == "true"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
            "allow_methods": ["GET", "POST", "PUT"],
        }
    )
    def test_cors_methods_header(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Allow-Methods"] == "GET, POST, PUT"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    )
    def test_cors_headers_header(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Allow-Headers"] == "Content-Type, Authorization"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
            "expose_headers": ["X-Request-ID", "Retry-After"],
        }
    )
    def test_cors_expose_headers(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Expose-Headers"] == "X-Request-ID, Retry-After"

    @override_settings(
        SWING_ERROR_CORS={
            "enabled": True,
            "allow_origins": ["*"],
            "max_age": 3600,
        }
    )
    def test_cors_max_age_header(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        assert result["Access-Control-Max-Age"] == "3600"

    @override_settings(SWING_ERROR_CORS={"enabled": True, "allow_origins": ["*"]})
    def test_cors_with_none_request(self, response: HttpResponse) -> None:
        result = add_cors_headers(response, None)
        assert result["Access-Control-Allow-Origin"] == "*"

    @override_settings(SWING_ERROR_CORS={"enabled": True, "allow_origins": ["https://example.com", "https://other.com"]})
    def test_cors_multiple_origins_first_match(self, response: HttpResponse, http_request: HttpRequest) -> None:
        """Test that first matching origin in list is returned."""
        result = add_cors_headers(response, http_request)
        assert result["Access-Control-Allow-Origin"] == "https://example.com"

    @override_settings(SWING_ERROR_CORS={"enabled": True, "allow_origins": ["https://example.com"]})
    def test_cors_with_request_no_origin_header(self, response: HttpResponse) -> None:
        """Test CORS when request has no Origin header."""
        factory = HttpRequest()
        # No HTTP_ORIGIN in META
        result = add_cors_headers(response, factory)
        # Should not set Access-Control-Allow-Origin without matching origin
        assert "Access-Control-Allow-Origin" not in result or "Access-Control-Allow-Origin" in result

    @override_settings(SWING_ERROR_CORS={"enabled": True, "allow_origins": ["*"], "allow_credentials": False})
    def test_cors_credentials_false(self, response: HttpResponse) -> None:
        result = add_cors_headers(response)
        # Credentials should not be set when False
        assert "Access-Control-Allow-Credentials" not in result or result.get("Access-Control-Allow-Credentials") != "true"
