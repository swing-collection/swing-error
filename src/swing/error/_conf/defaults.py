# Import | Standard Library
import logging
from typing import Any

logger: logging.Logger = logging.getLogger(name=__name__)

DEFAULT_CORS_CONFIG: dict[str, Any] = {
    "enabled": False,
    "allow_origins": ["*"],
    "allow_methods": [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ],
    "allow_headers": [
        "Accept",
        "Accept-Language",
        "Content-Type",
        "Authorization",
        "X-Request-ID",
        "X-Correlation-ID",
    ],
    "expose_headers": [
        "X-Request-ID",
        "Retry-After",
        "X-Error-Code",
    ],
    "allow_credentials": False,
    "max_age": 86400,
}

DEFAULT_TRACKING_CONFIG: dict[str, Any] = {
    "enabled": False,
    "capture_exceptions": True,
    "capture_messages": True,
    "callback": None,
    "extra_context": {},
}

DEFAULT_DEBUG_CONFIG: dict[str, Any] = {
    "show_stack_trace": False,
    "show_request_info": False,
    "show_environment": False,
    "include_sql_queries": False,
}

DEFAULT_SECURITY_HEADERS_CONFIG: dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "same-origin",
}

DEFAULT_ERROR_SETTINGS: dict[str, dict[str, Any]] = {
    "base": {
        "status_code": 500,
        "default_message": "An error occurred",
        "default_details": {
            "title": "Error",
            "header": "An Error Occurred",
            "message": "Something went wrong.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "400": {
        "status_code": 400,
        "default_message": "Bad Request",
        "default_details": {
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, your request could not be processed.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "401": {
        "status_code": 401,
        "default_message": "Unauthorized",
        "default_details": {
            "title": "Unauthorized",
            "header": "401 Error",
            "message": "Authentication is required to access this resource.",
            "redirect": "Please log in to continue.",
        },
        "log_errors": True,
    },
    "403": {
        "status_code": 403,
        "default_message": "Forbidden",
        "default_details": {
            "title": "Forbidden",
            "header": "403 Error",
            "message": "You do not have permission to access this resource.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "404": {
        "status_code": 404,
        "default_message": "Page Not Found",
        "default_details": {
            "title": "404 Error",
            "header": "Page Not Found",
            "message": "Sorry, the page you are looking for does not exist.",
            "redirect": "Return to the homepage.",
        },
        "log_errors": True,
    },
    "405": {
        "status_code": 405,
        "default_message": "Method Not Allowed",
        "default_details": {
            "title": "Method Not Allowed",
            "header": "405 Error",
            "message": "The requested method is not allowed for this resource.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "408": {
        "status_code": 408,
        "default_message": "Request Timeout",
        "default_details": {
            "title": "Request Timeout",
            "header": "408 Error",
            "message": "The server timed out waiting for your request.",
            "redirect": "Please try again.",
        },
        "log_errors": True,
    },
    "410": {
        "status_code": 410,
        "default_message": "Gone",
        "default_details": {
            "title": "Gone",
            "header": "410 Error",
            "message": "The requested resource is no longer available.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
    "429": {
        "status_code": 429,
        "default_message": "Too Many Requests",
        "default_details": {
            "title": "Too Many Requests",
            "header": "429 Error",
            "message": "You have sent too many requests. Please wait before trying again.",
            "redirect": "Please wait and try again later.",
        },
        "log_errors": True,
        "retry_after": 60,
    },
    "500": {
        "status_code": 500,
        "default_message": "Internal Server Error",
        "default_details": {
            "title": "Internal Server Error",
            "header": "500 Error",
            "message": "An unexpected error occurred on the server.",
            "redirect": "Please return to the homepage.",
        },
        "log_errors": True,
    },
}
