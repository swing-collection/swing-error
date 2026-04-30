from swing.error import views


def test_views_package_exports_handler_constants() -> None:
    assert views.HANDLER400.endswith("Handler400View")
    assert views.HANDLER500.endswith("Handler500View")
