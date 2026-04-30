from django.http import HttpRequest, HttpResponse

# Import | Local
from .get_cors_config import get_cors_config


def add_cors_headers(
    response: HttpResponse,
    request: HttpRequest | None = None,
) -> HttpResponse:
    config = get_cors_config()

    if not config.get("enabled", False):
        return response

    origin = request.META.get("HTTP_ORIGIN") if request else None
    allow_origins = config.get("allow_origins", ["*"])
    if "*" in allow_origins:
        response["Access-Control-Allow-Origin"] = "*"
    elif origin and origin in allow_origins:
        response["Access-Control-Allow-Origin"] = origin
        response["Vary"] = "Origin"

    if config.get("allow_credentials", False):
        response["Access-Control-Allow-Credentials"] = "true"

    allow_methods = config.get("allow_methods", [])
    if allow_methods:
        response["Access-Control-Allow-Methods"] = ", ".join(allow_methods)

    allow_headers = config.get("allow_headers", [])
    if allow_headers:
        response["Access-Control-Allow-Headers"] = ", ".join(allow_headers)

    expose_headers = config.get("expose_headers", [])
    if expose_headers:
        response["Access-Control-Expose-Headers"] = ", ".join(expose_headers)

    max_age = config.get("max_age")
    if max_age:
        response["Access-Control-Max-Age"] = str(max_age)

    return response
