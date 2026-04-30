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

# Import | Local
from ._utils.constants import (
    HTML_CONTENT_TYPES,
    JSON_CONTENT_TYPES,
    MIME_ANY,
    MIME_HTML,
    MIME_JSON,
)
from ._utils.generate_request_id import generate_request_id
from ._utils.get_accept_header import get_accept_header
from ._utils.get_client_ip import get_client_ip
from ._utils.get_preferred_content_type import get_preferred_content_type
from ._utils.get_request_id import get_request_id
from ._utils.wants_html import wants_html
from ._utils.wants_json import wants_json

# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "MIME_JSON",
    "MIME_HTML",
    "MIME_ANY",
    "JSON_CONTENT_TYPES",
    "HTML_CONTENT_TYPES",
    "get_accept_header",
    "wants_json",
    "wants_html",
    "get_preferred_content_type",
    "generate_request_id",
    "get_request_id",
    "get_client_ip",
]
