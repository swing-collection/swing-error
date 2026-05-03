from django.test import RequestFactory, SimpleTestCase

from swing.error.utils import (
    get_preferred_content_type,
    wants_html,
    wants_json,
)


class TestContentNegotiation(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_wants_json_with_json_accept_header(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        assert wants_json(request) is True

    def test_wants_json_with_html_accept_header(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        assert wants_json(request) is False

    def test_wants_json_with_xhr_header(self) -> None:
        request = self.factory.get(
            "/",
            HTTP_ACCEPT="*/*",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert wants_json(request) is True

    def test_wants_html_with_html_accept_header(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        assert wants_html(request) is True

    def test_wants_html_with_json_accept_header(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        assert wants_html(request) is False

    def test_get_preferred_content_type_json(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        assert get_preferred_content_type(request) == "json"

    def test_get_preferred_content_type_html(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="text/html")
        assert get_preferred_content_type(request) == "html"

    def test_get_preferred_content_type_problem_json(self) -> None:
        request = self.factory.get(
            "/",
            HTTP_ACCEPT="application/problem+json",
        )
        assert get_preferred_content_type(request) == "problem+json"

    def test_get_preferred_content_type_xml(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/xml")
        assert get_preferred_content_type(request) == "xml"

    def test_get_preferred_content_type_yaml(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/yaml")
        assert get_preferred_content_type(request) == "yaml"
