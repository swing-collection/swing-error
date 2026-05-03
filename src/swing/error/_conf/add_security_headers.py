from django.http import HttpResponse


def add_security_headers(response: HttpResponse) -> HttpResponse:
    """Apply the default security headers to an HTTP response."""
    response.setdefault("X-Content-Type-Options", "nosniff")
    response.setdefault("X-Frame-Options", "DENY")
    response.setdefault("Referrer-Policy", "same-origin")
    return response
