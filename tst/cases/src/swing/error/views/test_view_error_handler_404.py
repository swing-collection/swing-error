from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http404Response
from swing.error.views.view_error_handler_404 import Handler404View


class TestHandler404View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_404_status(self) -> None:
        assert Handler404View.as_view()(self.factory.get("/")).status_code == 404

    def test_view_uses_http404_response(self) -> None:
        assert Handler404View.response_class is Http404Response
