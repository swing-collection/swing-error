from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http405Response
from swing.error.views.view_error_handler_405 import Handler405View


class TestHandler405View(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_view_returns_405_status(self) -> None:
        assert Handler405View.as_view()(self.factory.get("/")).status_code == 405

    def test_view_uses_http405_response(self) -> None:
        assert Handler405View.response_class is Http405Response
