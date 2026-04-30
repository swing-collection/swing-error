# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Swing Error Middleware Module
=============================

This module provides middleware classes for global exception handling in Django
applications.

"""


# =============================================================================
# Imports
# =============================================================================

from .middleware_exception import ExceptionMiddleware
from .middleware_exception_logger import ExceptionLoggerMiddleware


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "ExceptionMiddleware",
    "ExceptionLoggerMiddleware",
]
# Exports
# =============================================================================
