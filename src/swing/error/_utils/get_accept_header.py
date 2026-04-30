from django.http import HttpRequest

# Import | Local
from .constants import MIME_ANY


def get_accept_header(request: HttpRequest) -> str:
    value = request.META.get("HTTP_ACCEPT", MIME_ANY)
    return str(value)
