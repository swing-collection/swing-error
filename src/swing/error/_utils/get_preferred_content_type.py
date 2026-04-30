# Import | Standard Library
from typing import Literal

from django.http import HttpRequest

# Import | Local
from .wants_json import wants_json


def get_preferred_content_type(
    request: HttpRequest,
) -> Literal["json", "html"]:
    if wants_json(request):
        return "json"
    return "html"
