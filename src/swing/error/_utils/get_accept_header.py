from django.http import HttpRequest

# Import | Local
from .constants import MIME_ANY


def get_accept_header(request: HttpRequest) -> str:
    """Return the request Accept header, defaulting to a wildcard value."""
    value = request.META.get("HTTP_ACCEPT", MIME_ANY)
    return str(value)
