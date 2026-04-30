from typing import Any


def detect_retry_after(
    exception: Exception | None = None,
    request: Any | None = None,
) -> int | None:
    candidates: list[Any] = []
    if exception is not None:
        candidates.append(exception)
        response = getattr(exception, "response", None)
        if response is not None:
            candidates.append(response)
        detail = getattr(exception, "detail", None)
        if detail is not None:
            candidates.append(detail)

    if request is not None:
        candidates.append(getattr(request, "rate_limit", None))
        candidates.append(getattr(request, "rate_limit_info", None))

    for candidate in candidates:
        if candidate is None:
            continue

        headers = getattr(candidate, "headers", None)
        if headers is not None and hasattr(headers, "get"):
            header_value = headers.get("Retry-After")
            if header_value is not None:
                try:
                    return int(header_value)
                except (TypeError, ValueError):
                    pass

        for attr_name in ("retry_after", "wait", "remaining", "time_left"):
            attr_value = getattr(candidate, attr_name, None)
            if attr_value is not None:
                try:
                    return int(attr_value)
                except (TypeError, ValueError):
                    pass

        if isinstance(candidate, dict):
            for key in ("retry_after", "wait", "remaining", "time_left"):
                if key in candidate:
                    try:
                        return int(candidate[key])
                    except (TypeError, ValueError):
                        pass

    return None
