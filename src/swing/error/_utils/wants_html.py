from django.http import HttpRequest

# Import | Local
from .constants import HTML_CONTENT_TYPES, MIME_ANY
from .get_accept_header import get_accept_header
from .wants_json import wants_json


def wants_html(request: HttpRequest) -> bool:
    accept = get_accept_header(request).lower()

    for html_type in HTML_CONTENT_TYPES:
        if html_type in accept:
            return True

    if MIME_ANY in accept and not wants_json(request):
        return True

    return False
