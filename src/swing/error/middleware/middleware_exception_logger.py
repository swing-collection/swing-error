# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Exception Logger Middleware Class
==========================================


"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging


# Import | Libraries

# Import | Local Modules


# =============================================================================
# Logger
# =============================================================================

logger: logging.Logger = logging.getLogger(name=__name__)

# =============================================================================
# Class
# =============================================================================


class ExceptionLoggerMiddleware:
    """ """

    def __init__(self, get_response) -> None:
        """ """
        self.get_response = get_response
        self.logger: logging.Logger = logging.getLogger("django")

    def __call__(self, request):
        """ """
        response = self.get_response(request)
        return response

    def process_exception(
        self,
        request,
        exception,
    ) -> None:
        """ """
        self.logger.exception(str(object=exception))


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionLoggerMiddleware",
]
