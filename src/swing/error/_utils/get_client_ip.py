from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """Resolve the client IP using forwarded headers before REMOTE_ADDR."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return str(x_forwarded_for).split(",")[0].strip()

    x_real_ip = request.META.get("HTTP_X_REAL_IP")
    if x_real_ip:
        return str(x_real_ip)

    return str(request.META.get("REMOTE_ADDR", "unknown"))
