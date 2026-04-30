from django.test import RequestFactory

# Import | Libraries
import pytest

from swing.error._utils.wants_html import wants_html
from swing.error._utils.wants_json import wants_json


class TestWantsJson:
    def test_wants_json_with_json_accept(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="application/json")
        assert wants_json(request) is True

    def test_wants_json_with_html_accept(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="text/html")
        assert wants_json(request) is False

    def test_wants_json_returns_false_for_plain_text(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="text/plain")
        assert wants_json(request) is False

    def test_wants_json_with_multiple_types(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="application/json, text/html;q=0.9")
        assert wants_json(request) is True

    def test_wants_json_prefers_first_match(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="application/json;q=0.9, text/html")
        assert wants_json(request) is True


class TestWantsHtml:
    def test_wants_html_with_html_accept(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="text/html")
        assert wants_html(request) is True

    def test_wants_html_with_wildcard_accept(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="*/*")
        assert wants_html(request) is True

    def test_wants_html_with_json_accept(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="application/json")
        assert wants_html(request) is False

    def test_wants_html_with_multiple_types(self) -> None:
        factory = RequestFactory()
        request = factory.get("/", HTTP_ACCEPT="text/html, application/json;q=0.9")
        assert wants_html(request) is True
