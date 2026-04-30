from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http403Response
from swing.error.views.view_error_handler_403 import Handler403View


class TestHandler403View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_403_status(self) -> None:
        assert Handler403View.as_view()(self.factory.get("/")).status_code == 403

    def test_view_uses_http403_response(self) -> None:
        assert Handler403View.response_class is Http403Response
