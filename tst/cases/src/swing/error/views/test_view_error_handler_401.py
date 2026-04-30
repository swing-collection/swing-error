from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http401Response
from swing.error.views.view_error_handler_401 import Handler401View


class TestHandler401View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_401_status(self) -> None:
        assert (
            Handler401View.as_view()(self.factory.get("/")).status_code == 401
        )

    def test_view_returns_json_for_json_accept_header(self) -> None:
        response = Handler401View.as_view()(
            self.factory.get("/", HTTP_ACCEPT="application/json")
        )
        assert "application/json" in response.get("Content-Type", "")

    def test_view_uses_http401_response(self) -> None:
        assert Handler401View.response_class is Http401Response
