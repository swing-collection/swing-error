from django.http import HttpRequest

# Import | Local
from .generate_request_id import generate_request_id


def get_request_id(request: HttpRequest) -> str:
    for header in [
        "HTTP_X_REQUEST_ID",
        "HTTP_X_CORRELATION_ID",
        "HTTP_X_TRACE_ID",
    ]:
        if request_id := request.META.get(header):
            return request_id

    return generate_request_id()
