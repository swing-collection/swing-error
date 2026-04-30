from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http410Response
from swing.error.views.view_error_handler_410 import Handler410View


class TestHandler410View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_410_status(self) -> None:
        assert Handler410View.as_view()(self.factory.get("/")).status_code == 410

    def test_view_uses_http410_response(self) -> None:
        assert Handler410View.response_class is Http410Response
