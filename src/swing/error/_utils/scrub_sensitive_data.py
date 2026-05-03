# Import | Standard Library
from typing import Any

REDACTED = "[REDACTED]"
SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "cookie",
        "csrfmiddlewaretoken",
        "password",
        "secret",
        "token",
        "x-api-key",
    }
)
SENSITIVE_MARKERS = (
    "authorization",
    "bearer ",
    "cookie",
    "password",
    "secret",
    "token",
)


def scrub_sensitive_data(value: Any, key: str | None = None) -> Any:
    """Recursively redact secrets from mappings, sequences, and strings."""
    lowered_key = key.lower() if key is not None else ""
    if any(marker in lowered_key for marker in SENSITIVE_KEYS):
        return REDACTED

    if isinstance(value, dict):
        return {
            nested_key: scrub_sensitive_data(nested_value, nested_key)
            for nested_key, nested_value in value.items()
        }

    if isinstance(value, list):
        return [scrub_sensitive_data(item) for item in value]

    if isinstance(value, tuple):
        return tuple(scrub_sensitive_data(item) for item in value)

    if isinstance(value, str):
        lowered_value = value.lower()
        if any(marker in lowered_value for marker in SENSITIVE_MARKERS):
            return REDACTED

    return value
