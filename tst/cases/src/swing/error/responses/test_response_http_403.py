# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http403Response


class TestHttp403Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http403Response().status_code == 403

    def test_default_message(self) -> None:
        assert json.loads(Http403Response().content)["error"] == "Forbidden"
