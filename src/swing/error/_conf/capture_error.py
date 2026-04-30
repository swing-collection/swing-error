# Import | Standard Library
from importlib import import_module
from typing import Any, cast

from django.http import HttpRequest

# Import | Local
from .defaults import logger
from .get_tracking_config import get_tracking_config
from .import_callback import import_callback


def capture_error(
    exception: Exception | None = None,
    message: str | None = None,
    request: HttpRequest | None = None,
    extra_context: dict[str, Any] | None = None,
) -> None:
    config = get_tracking_config()

    if not config.get("enabled", False):
        return

    context: dict[str, Any] = config.get("extra_context", {}).copy()
    if extra_context:
        context.update(extra_context)

    if request:
        context.update(
            {
                "request_path": request.path,
                "request_method": request.method,
                "request_user": str(getattr(request, "user", "anonymous")),
            }
        )

    if config.get("capture_exceptions", True) or config.get("capture_messages", True):
        try:
            sentry_sdk = cast(Any, import_module("sentry_sdk"))

            if exception and config.get("capture_exceptions", True):
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                    sentry_sdk.capture_exception(exception)
            elif message and config.get("capture_messages", True):
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                    sentry_sdk.capture_message(message)
        except ImportError:
            pass

    callback_path = config.get("callback")
    if callback_path:
        try:
            callback = import_callback(callback_path)
            callback(
                exception=exception,
                message=message,
                request=request,
                context=context,
            )
        except Exception as error:
            logger.warning(f"Error tracking callback failed: {error}")
