from django.conf import settings

# Default configuration for the error handling
DEFAULT_ERROR_SETTINGS = {
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
    },
    # Add additional error-specific configurations as needed
}

def get_error_config(error_type: str, key: str, default=None):
    """
    Retrieve error handler configuration for a specific error type
    from Django settings with fallback to defaults.

    Args:
        error_type (str): The error type (e.g., "400", "404", "base").
        key (str): The key to retrieve from the error configuration.
        default (Any): Default value if the key or type is not set.

    Returns:
        Any: The configuration value.
    """
    return (
        getattr(settings, "ERROR_HANDLER_CONFIG", {})
        .get(error_type, {})
        .get(key, DEFAULT_ERROR_SETTINGS.get(error_type, DEFAULT_ERROR_SETTINGS["base"]).get(key, default))
    )
