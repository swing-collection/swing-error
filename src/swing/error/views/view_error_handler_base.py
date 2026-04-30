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
- https://docs.djangoproject.com/en/stable/ref/urls/#django.conf.urls.handler400
- https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseBadRequest

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import logging
from typing import Any

from django.http import HttpRequest
from django.views.generic import TemplateView

# Import | Local
from ..conf import get_error_config

# Import | Local Modules
from ..responses.response_error_base import BaseErrorResponse

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
        error_type (str): The error type code (e.g., "400", "404", "500").
        response_class (type[BaseErrorResponse]): The response class to use.
        status_code (int): The HTTP status code for the error response.
        logger (logging.Logger): Logger instance for logging errors.
        default_message (str): Default error message for the view.
        default_details (dict[str, Any]): Default structured details for
            the response.

    """

    error_type: str = "base"  # Override in subclasses for specific errors
    response_class: type[BaseErrorResponse] = BaseErrorResponse
    logger: logging.Logger = logging.getLogger(name=__name__)

    @property
    def status_code(self) -> int:
        """
        Retrieve the status code from the configuration.

        Returns:
            int: The HTTP status code.
        """
        return get_error_config(
            error_type=self.error_type,
            key="status_code",
            default=500,
        )

    @property
    def template_name(self) -> str:
        """
        Retrieve the template name from the configuration.
        """
        return get_error_config(
            error_type=self.error_type,
            key="template_name",
            default="errors/default.html",
        )

    @property
    def default_message(self) -> str:
        """
        Retrieve the default error message from the configuration.

        Returns:
            str: The default error message.
        """
        return get_error_config(
            error_type=self.error_type,
            key="default_message",
            default="An error occurred",
        )

    @property
    def default_details(self) -> dict[str, Any]:
        """
        Retrieve the default error details from the configuration.

        Returns:
            dict[str, Any]: A dictionary with error details.
        """
        return get_error_config(
            error_type=self.error_type,
            key="default_details",
            default={},
        )

    @property
    def default_context(self) -> dict[str, Any]:
        """
        Retrieve the default context for rendering the template.
        """
        return get_error_config(
            error_type=self.error_type,
            key="default_details",
            default={
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
            error_type=self.error_type,
            key="log_errors",
            default=True,
        )

    def get_context_data(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Extend the base context data with custom error information.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            dict[str, Any]: Context data for the template.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update(self.default_context)
        return context

    def get(
        self,
        request: HttpRequest,
        # *args: Any,
        # **kwargs: dict[str, Any]
    ) -> BaseErrorResponse:
        """
        Handle GET requests by logging the error and returning a structured
        response.

        Args:
            request (HttpRequest): The request object.

        Returns:
            BaseErrorResponse: A structured error response.
        """
        if self.log_errors:
            self.log_error(request=request)

        return self.response_class(
            status_code=self.status_code,
            message=self.default_message,
            details=self.default_details,
            request=request,
        )

    def log_error(
        self,
        request: HttpRequest,
    ) -> None:
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
