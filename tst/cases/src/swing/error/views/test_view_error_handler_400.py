from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http400Response
from swing.error.views.view_error_handler_400 import Handler400View


class TestHandler400View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_400_status(self) -> None:
        assert Handler400View.as_view()(self.factory.get("/")).status_code == 400

    def test_view_uses_http400_response(self) -> None:
        assert Handler400View.response_class is Http400Response
