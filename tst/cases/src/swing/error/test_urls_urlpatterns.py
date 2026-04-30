from swing.error import urls


def test_urlpatterns_is_a_list() -> None:
    assert isinstance(urls.urlpatterns, list)
