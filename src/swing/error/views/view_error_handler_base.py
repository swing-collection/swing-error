# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Base Error View Class
==============================

A reusable base class for error handler views, allowing projects to define
custom error responses through settings overrides.

Links:
------
- https://docs.djangoproject.com/en/5.0/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponseBadRequest

"""  # noqa E501


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict
import logging

# Import | Libraries
from django.views.generic import TemplateView
from django.http import HttpRequest

# Import | Local Modules
from swing_error.responses.response_http_400 import Http400Response
from swing_error.conf import get_error_config


# =============================================================================
# Class
# =============================================================================

class BaseErrorView(TemplateView):
    """
    Base Error View Class
    =====================

    A reusable base class for error handler views.

    This class provides common functionality, such as logging error details
    and returning structured error responses using BaseErrorResponse. Users
    can customize error behavior through the `ERROR_HANDLER_CONFIG` setting
    in their project.

    Attributes:
        status_code (int): The HTTP status code for the error response.
        logger (logging.Logger): Logger instance for logging errors.
        default_message (str): Default error message for the view.
        default_details (Dict[str, Any]): Default structured details for
            the response.

    """

    error_type: str = "base"  # Override in subclasses for specific errors
    logger: logging.Logger = logging.getLogger(__name__)

    @property
    def status_code(self) -> int:
        """
        Retrieve the status code from the configuration.

        Returns:
            int: The HTTP status code.
        """
        return get_error_config(
            self.error_type,
            "status_code",
            500,
        )

    @property
    def template_name(self) -> str:
        """
        Retrieve the template name from the configuration.
        """
        return get_error_config(
            self.error_type,
            "template_name",
            "errors/default.html",
        )

    @property
    def default_message(self) -> str:
        """
        Retrieve the default error message from the configuration.

        Returns:
            str: The default error message.
        """
        return get_error_config(
            self.error_type,
            "default_message",
            "An error occurred",
        )

    @property
    def default_details(self) -> Dict[str, Any]:
        """
        Retrieve the default error details from the configuration.

        Returns:
            Dict[str, Any]: A dictionary with error details.
        """
        return get_error_config(
            self.error_type,
            "default_details",
            {},
        )

    @property
    def default_context(self) -> Dict[str, Any]:
        """Retrieve the default context for rendering the template."""
        return get_error_config(
            self.error_type,
            "default_details",
            {
                "title": "Error",
                "header": "An Error Occurred",
                "message": "Something went wrong.",
                "redirect": "Please return to the homepage.",
            },
        )

    @property
    def log_errors(self) -> bool:
        """
        Retrieve the logging behavior from the configuration.

        Returns:
            bool: Whether to log the error details.
        """
        return get_error_config(
            self.error_type,
            "log_errors",
            True,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Extend the base context data with custom error information.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Dict[str, Any]: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context.update(self.default_context)
        return context

    def get(
        self,
        request: HttpRequest,
        # *args: Any,
        # **kwargs: Dict[str, Any]
    ) -> Http400Response:
        """
        Handle GET requests by logging the error and returning a structured
        response.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Http400Response: A structured error response.
        """
        if self.log_errors:
            self.log_error(request)

        return Http400Response(
            message=self.default_message,
            details=self.default_details,
            request=request,
        )

    def log_error(self, request: HttpRequest) -> None:
        """
        Log the error details for debugging purposes.

        Args:
            request (HttpRequest): The request object.
        """
        self.logger.error(
            "Error %d at %s: %s",
            self.status_code,
            request.path,
            self.default_message,
        )
