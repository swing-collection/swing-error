from swing.error.middleware import ExceptionMiddleware


def test_middleware_package_exports_exception_middleware() -> None:
    assert ExceptionMiddleware.__name__ == "ExceptionMiddleware"
