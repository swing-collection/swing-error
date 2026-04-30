# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http404Response


class TestHttp404Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http404Response().status_code == 404

    def test_default_message(self) -> None:
        assert json.loads(Http404Response().content)["error"] == "Not Found"
