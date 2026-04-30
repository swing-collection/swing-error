from django.http import HttpRequest

# Import | Local
from .constants import JSON_CONTENT_TYPES
from .get_accept_header import get_accept_header


def wants_json(request: HttpRequest) -> bool:
    accept = get_accept_header(request).lower()

    for json_type in JSON_CONTENT_TYPES:
        if json_type in accept:
            return True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return True

    content_type = request.content_type
    if content_type and any(
        content in content_type for content in JSON_CONTENT_TYPES
    ):
        return True

    return False
