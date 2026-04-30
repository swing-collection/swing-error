# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http500Response


class TestHttp500Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http500Response().status_code == 500

    def test_default_message(self) -> None:
        assert (
            json.loads(Http500Response().content)["error"]
            == "Internal Server Error"
        )
