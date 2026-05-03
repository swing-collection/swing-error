from django.http import HttpRequest

# Import | Local
from ..responses.renderers import negotiate_renderer
from .get_accept_header import get_accept_header


def get_preferred_content_type(
    request: HttpRequest,
) -> str:
    """Return the preferred error response format for the request."""
    accept_header = get_accept_header(request)
    if "text/html" in accept_header.lower():
        return "html"
    return negotiate_renderer(accept_header)
