# Import | Standard Library
from collections.abc import Callable
from importlib import import_module
from typing import Any, cast


def import_callback(callback_path: str) -> Callable[..., Any]:
    """Import and return a callback from a dotted module path."""
    module_path, func_name = callback_path.rsplit(".", 1)
    module = import_module(module_path)
    return cast(Callable[..., Any], getattr(module, func_name))
