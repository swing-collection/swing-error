# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http410Response


class TestHttp410Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http410Response().status_code == 410

    def test_default_message(self) -> None:
        assert json.loads(Http410Response().content)["error"] == "Gone"
