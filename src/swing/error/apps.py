# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Register the swing.error Django application.

This module declares the reusable app config that Django uses when the
package is installed in a project.
"""

# =============================================================================
# Import
# =============================================================================

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================


class SwingErrorConfig(AppConfig):
    """Configure the reusable swing.error Django application."""

    # Full Python path to the application
    name = "swing.error"

    # Short name for the application
    label = "swing_error"

    # Human-readable name for the application
    verbose_name = _("Swing Errors")

    # Filesystem path to the application directory,
    # path = "/usr/lib/pythonX.Y/dist-packages/django/contrib/admin"

    # default = True

    # The implicit primary key type to add to models within this app.
    default_auto_field: str = "django.db.models.BigAutoField"

    # def ready(self):
    #     """
    #     Apps Config Ready Function
    #     """

    # Implicitly connect signal handlers decorated with @receiver.
    # from .. import signals

    # Explicitly connect a signal handler.
    # request_finished.connect(signals.my_callback)
