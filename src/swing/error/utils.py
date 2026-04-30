# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error Utilities Module
============================

This module provides utility functions for the swing.error app, including
content negotiation helpers for determining response format based on
Accept headers.

Usage:
------
    from swing.error.utils import wants_json, get_preferred_content_type

    if wants_json(request):
        return JsonResponse(...)
    else:
        return render(request, 'error.html', ...)

"""

# =============================================================================
# Imports
# =============================================================================

import uuid
from typing import Literal

from django.http import HttpRequest


# =============================================================================
# Constants
# =============================================================================

# Common MIME types
MIME_JSON = "application/json"
MIME_HTML = "text/html"
MIME_ANY = "*/*"

# Content types that indicate JSON preference
JSON_CONTENT_TYPES = frozenset([
    "application/json",
    "application/vnd.api+json",
    "application/hal+json",
    "application/ld+json",
])

# Content types that indicate HTML preference
HTML_CONTENT_TYPES = frozenset([
    "text/html",
    "application/xhtml+xml",
])


# =============================================================================
# Functions
# =============================================================================


def get_accept_header(request: HttpRequest) -> str:
    """
    Get the Accept header from a request.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        str: The Accept header value, or "*/*" if not present.
    """
    return request.META.get("HTTP_ACCEPT", MIME_ANY)


def wants_json(request: HttpRequest) -> bool:
    """
    Determine if the client prefers JSON response based on Accept header.

    This function checks the Accept header to determine if the client
    is expecting a JSON response (e.g., API clients, AJAX requests).

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        bool: True if client prefers JSON, False otherwise.

    Example:
        >>> # curl -H "Accept: application/json" ...
        >>> wants_json(request)
        True

        >>> # Browser request with "text/html,application/xhtml+xml,..."
        >>> wants_json(request)
        False
    """
    accept = get_accept_header(request).lower()

    # Check for explicit JSON content types
    for json_type in JSON_CONTENT_TYPES:
        if json_type in accept:
            return True

    # Check for XHR requests (usually want JSON)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return True

    # Check content type of the request body
    content_type = request.content_type
    if content_type and any(t in content_type for t in JSON_CONTENT_TYPES):
        return True

    return False


def wants_html(request: HttpRequest) -> bool:
    """
    Determine if the client prefers HTML response based on Accept header.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        bool: True if client prefers HTML, False otherwise.
    """
    accept = get_accept_header(request).lower()

    for html_type in HTML_CONTENT_TYPES:
        if html_type in accept:
            return True

    # Browsers typically send */* at the end
    if MIME_ANY in accept and not wants_json(request):
        return True

    return False


def get_preferred_content_type(
    request: HttpRequest,
) -> Literal["json", "html"]:
    """
    Determine the preferred content type for the response.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        Literal["json", "html"]: The preferred content type.
    """
    if wants_json(request):
        return "json"
    return "html"


def generate_request_id() -> str:
    """
    Generate a unique request ID for error tracking.

    Returns:
        str: A unique UUID string.
    """
    return str(uuid.uuid4())


def get_request_id(request: HttpRequest) -> str:
    """
    Get or generate a request ID for the given request.

    This checks for existing request ID headers commonly used by
    load balancers and API gateways, or generates a new one.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        str: The request ID.
    """
    # Check common request ID headers
    for header in [
        "HTTP_X_REQUEST_ID",
        "HTTP_X_CORRELATION_ID",
        "HTTP_X_TRACE_ID",
    ]:
        if request_id := request.META.get(header):
            return request_id

    return generate_request_id()


def get_client_ip(request: HttpRequest) -> str:
    """
    Get the client's IP address from the request.

    Handles common proxy headers for load balancers.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        str: The client's IP address.
    """
    # Check for forwarded headers (common with proxies/load balancers)
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Take the first IP in the chain
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.META.get("HTTP_X_REAL_IP")
    if x_real_ip:
        return x_real_ip

    return request.META.get("REMOTE_ADDR", "unknown")


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "MIME_JSON",
    "MIME_HTML",
    "wants_json",
    "wants_html",
    "get_preferred_content_type",
    "generate_request_id",
    "get_request_id",
    "get_client_ip",
]
