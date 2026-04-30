from swing.error import urls
from swing.error.views import (
    HANDLER400,
    HANDLER401,
    HANDLER403,
    HANDLER404,
    HANDLER405,
    HANDLER408,
    HANDLER410,
    HANDLER429,
    HANDLER500,
)


def test_url_module_exports_handler_aliases() -> None:
    assert urls.handler400 == HANDLER400
    assert urls.handler401 == HANDLER401
    assert urls.handler403 == HANDLER403
    assert urls.handler404 == HANDLER404
    assert urls.handler405 == HANDLER405
    assert urls.handler408 == HANDLER408
    assert urls.handler410 == HANDLER410
    assert urls.handler429 == HANDLER429
    assert urls.handler500 == HANDLER500
