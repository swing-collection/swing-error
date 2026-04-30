# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http408Response


class TestHttp408Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http408Response().status_code == 408

    def test_default_message(self) -> None:
        assert (
            json.loads(Http408Response().content)["error"] == "Request Timeout"
        )
