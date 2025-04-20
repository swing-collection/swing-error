# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Swing Error Config Class
=================================


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Dict, List, Union

# Import | Libraries
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================


class SwingErrorConfig(AppConfig):
    """
    Swing Error Config Class
    ========================
    """

    # Full Python path to the application
    name = "swing.error"

    # Short name for the application
    label = "swing_error"

    # Human-readable name for the application
    verbose_name: str = _("Swing Errors")

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
