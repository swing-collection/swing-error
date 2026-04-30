from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http500Response
from swing.error.views.view_error_handler_500 import Handler500View


class TestHandler500View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_500_status(self) -> None:
        assert Handler500View.as_view()(self.factory.get("/")).status_code == 500

    def test_view_uses_http500_response(self) -> None:
        assert Handler500View.response_class is Http500Response
