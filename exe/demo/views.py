# -*- coding: utf-8 -*-

"""
Demo Views
==========

This module provides demo views to test various error responses and
the swing.error functionality.
"""

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.views.decorators.http import require_http_methods


def home(request: HttpRequest) -> HttpResponse:
    """Home page with links to test various error responses."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Swing Error Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            .container { max-width: 800px; }
            .error-links { display: grid; gap: 10px; }
            a {
                display: inline-block;
                padding: 10px 20px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 5px 0;
            }
            a:hover { background: #0056b3; }
            .status { font-weight: bold; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Swing Error Demo</h1>
            <p>Test various HTTP error responses and error handling:</p>

            <h2>4xx Client Errors</h2>
            <div class="error-links">
                <a href="/test/400/">Test 400 Bad Request</a>
                <a href="/test/401/">Test 401 Unauthorized</a>
                <a href="/test/403/">Test 403 Forbidden</a>
                <a href="/test/404/">Test 404 Not Found</a>
                <a href="/test/405/">Test 405 Method Not Allowed</a>
                <a href="/test/408/">Test 408 Request Timeout</a>
                <a href="/test/410/">Test 410 Gone</a>
                <a href="/test/429/">Test 429 Too Many Requests</a>
            </div>

            <h2>5xx Server Errors</h2>
            <div class="error-links">
                <a href="/test/500/">Test 500 Internal Server Error</a>
                <a href="/test/exception/">Test Unhandled Exception</a>
            </div>

            <h2>API Responses</h2>
            <div class="error-links">
                <a href="/api/json-error/">Test JSON Error Response</a>
                <a href="/api/success/">Test JSON Success Response</a>
            </div>

            <hr style="margin: 40px 0;">
            <p><small>Use your browser's developer tools (F12) to see response headers and JSON payloads.</small></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


# ============================================================================
# 4xx Error Test Views
# ============================================================================


@require_http_methods(["GET"])
def test_400(request: HttpRequest) -> HttpResponse:
    """Test 400 Bad Request response."""
    from swing.error.responses import Http400Response

    return Http400Response(request=request, message="Invalid request parameters")


@require_http_methods(["GET"])
def test_401(request: HttpRequest) -> HttpResponse:
    """Test 401 Unauthorized response."""
    from swing.error.responses import Http401Response

    return Http401Response(request=request, message="Authentication required")


@require_http_methods(["GET"])
def test_403(request: HttpRequest) -> HttpResponse:
    """Test 403 Forbidden response."""
    from swing.error.responses import Http403Response

    return Http403Response(request=request, message="Access denied")


@require_http_methods(["GET"])
def test_404(request: HttpRequest) -> HttpResponse:
    """Test 404 Not Found response."""
    from swing.error.responses import Http404Response

    return Http404Response(request=request, message="Resource not found")


@require_http_methods(["POST"])
def test_405_post_only(request: HttpRequest) -> HttpResponse:
    """POST-only endpoint to test 405 when accessed with GET."""
    return JsonResponse({"status": "ok"})


@require_http_methods(["GET"])
def test_405(request: HttpRequest) -> HttpResponse:
    """Test 405 Method Not Allowed - This will be triggered by middleware."""
    from swing.error.responses import Http405Response

    return Http405Response(request=request, message="Method not allowed")


@require_http_methods(["GET"])
def test_408(request: HttpRequest) -> HttpResponse:
    """Test 408 Request Timeout response."""
    from swing.error.responses import Http408Response

    return Http408Response(request=request, message="Request timeout")


@require_http_methods(["GET"])
def test_410(request: HttpRequest) -> HttpResponse:
    """Test 410 Gone response."""
    from swing.error.responses import Http410Response

    return Http410Response(request=request, message="Resource no longer available")


@require_http_methods(["GET"])
def test_429(request: HttpRequest) -> HttpResponse:
    """Test 429 Too Many Requests response."""
    from swing.error.responses import Http429Response

    return Http429Response(
        request=request, message="Rate limit exceeded", retry_after=60
    )


# ============================================================================
# 5xx Error Test Views
# ============================================================================


@require_http_methods(["GET"])
def test_500(request: HttpRequest) -> HttpResponse:
    """Test 500 Internal Server Error response."""
    from swing.error.responses import Http500Response

    return Http500Response(request=request, message="Internal server error occurred")


@require_http_methods(["GET"])
def test_exception(request: HttpRequest) -> HttpResponse:
    """Trigger an unhandled exception to test error middleware."""
    raise ValueError("This is a test exception to demonstrate error handling")


# ============================================================================
# API Test Views
# ============================================================================


@require_http_methods(["GET"])
def api_json_error(request: HttpRequest) -> JsonResponse:
    """Test JSON error response from API."""
    from swing.error.responses import Http400Response

    return Http400Response(
        request=request,
        message="Invalid API request",
        details={"field": "email", "reason": "Invalid email format"},
    )


@require_http_methods(["GET"])
def api_success(request: HttpRequest) -> JsonResponse:
    """Test successful JSON API response."""
    return JsonResponse(
        {
            "status": "success",
            "message": "API request successful",
            "data": {
                "id": 1,
                "name": "Demo Item",
                "created_at": "2026-04-30T00:00:00Z",
            },
        }
    )
