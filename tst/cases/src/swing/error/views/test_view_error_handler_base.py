from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import Http400Response
from swing.error.views.view_error_handler_base import BaseErrorView


class TestBaseErrorView(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        class InlineBaseView(BaseErrorView):
            error_type = "400"
            response_class = Http400Response

        self.view_class = InlineBaseView

    def test_get_returns_response_instance(self) -> None:
        response = self.view_class.as_view()(self.factory.get("/"))
        assert response.status_code == 400

    def test_default_message_comes_from_config(self) -> None:
        assert self.view_class().default_message == "Bad Request"
