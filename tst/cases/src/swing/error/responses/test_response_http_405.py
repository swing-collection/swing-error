# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http405Response


class TestHttp405Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http405Response().status_code == 405

    def test_default_message(self) -> None:
        assert (
            json.loads(Http405Response().content)["error"]
            == "Method Not Allowed"
        )
