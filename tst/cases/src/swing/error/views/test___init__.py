from swing.error import views


def test_views_package_exports_handler_constants() -> None:
    # HANDLERxxx are callable views produced by ``HandlerXXXView.as_view()``,
    # not dotted-path strings, so we check the underlying view class instead.
    assert views.HANDLER400.view_class is views.Handler400View
    assert views.HANDLER500.view_class is views.Handler500View
