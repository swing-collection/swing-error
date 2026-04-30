from swing.error.views.test import test as test_module


def test_embedded_view_test_module_exposes_custom_handler_fixture() -> None:
    assert callable(test_module.handler403)
    assert isinstance(test_module.urlpatterns, list)
