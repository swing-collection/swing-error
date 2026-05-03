# Import | Standard Library
import traceback
from typing import Any

from django.http import HttpRequest

# Import | Local
from .get_debug_config import get_debug_config


def get_debug_info(
    exception: Exception | None = None,
    request: HttpRequest | None = None,
) -> dict[str, Any]:
    """Collect configured debug details for an exception response payload."""
    config = get_debug_config()
    debug_info: dict[str, Any] = {}

    if not any(config.values()):
        return debug_info

    if config.get("show_stack_trace") and exception:
        debug_info["stack_trace"] = traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__,
        )
        debug_info["exception_type"] = type(exception).__name__
        debug_info["exception_message"] = str(exception)

    if config.get("show_request_info") and request:
        debug_info["request"] = {
            "path": request.path,
            "method": request.method,
            "content_type": request.content_type,
            "headers": {
                key: value
                for key, value in request.headers.items()
                if key.lower() not in ("authorization", "cookie", "x-api-key")
            },
            "GET": dict(request.GET),
            "POST": dict(request.POST) if request.method == "POST" else {},
        }

    if config.get("show_environment"):
        # Import | Standard Library
        import os

        safe_vars = ["DJANGO_SETTINGS_MODULE", "DEBUG", "PYTHONPATH"]
        debug_info["environment"] = {
            key: value for key, value in os.environ.items() if key in safe_vars
        }

    if config.get("include_sql_queries"):
        try:
            from django.db import connection

            debug_info["sql_queries"] = [
                {"sql": query["sql"], "time": query["time"]}
                for query in connection.queries[-10:]
            ]
        except Exception:
            pass

    return debug_info
