from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http408Response
from swing.error.views.view_error_handler_408 import Handler408View


class TestHandler408View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_408_status(self) -> None:
        assert Handler408View.as_view()(self.factory.get("/")).status_code == 408

    def test_view_uses_http408_response(self) -> None:
        assert Handler408View.response_class is Http408Response
