# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http401Response


class TestHttp401Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http401Response().status_code == 401

    def test_default_message(self) -> None:
        assert json.loads(Http401Response().content)["error"] == "Unauthorized"
