from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http429Response
from swing.error.views.view_error_handler_429 import Handler429View


class TestHandler429View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_429_status(self) -> None:
        assert Handler429View.as_view()(self.factory.get("/")).status_code == 429

    def test_view_uses_http429_response(self) -> None:
        assert Handler429View.response_class is Http429Response
