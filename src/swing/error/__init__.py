# -*- coding: utf-8 -*-

"""

"""
# Import | Local
from .apps import SwingErrorConfig
from .middleware import ExceptionMiddleware
from .responses import (
    BaseErrorResponse,
    Http400Response,
    Http401Response,
    Http403Response,
    Http404Response,
    Http405Response,
    Http408Response,
    Http410Response,
    Http429Response,
    Http500Response,
)

__author__ = "Lars van Vianen"
__copyright__ = "Copyright (c) 2024 Scape Press"
__credits__ = [
    "Lars van Vianen",
]
__license__ = "Proprietary"
__version__ = "1.0.1"
__maintainer__ = "Lars van Vianen"
__email__ = "lars@scape.press"
__status__ = "Alpha"


__all__ = [
    "BaseErrorResponse",
    "ExceptionMiddleware",
    "Http400Response",
    "Http401Response",
    "Http403Response",
    "Http404Response",
    "Http405Response",
    "Http408Response",
    "Http410Response",
    "Http429Response",
    "Http500Response",
    "SwingErrorConfig",
    "__author__",
    "__copyright__",
    "__credits__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__status__",
    "__version__",
]
