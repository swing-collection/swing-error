# Import | Standard Library
import json

from django.test import SimpleTestCase

from swing.error.responses import Http400Response


class TestHttp400Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http400Response().status_code == 400

    def test_default_message(self) -> None:
        assert json.loads(Http400Response().content)["error"] == "Bad Request"

    def test_custom_message(self) -> None:
        assert (
            json.loads(Http400Response(message="Custom error message").content)["error"]
            == "Custom error message"
        )

    def test_with_details(self) -> None:
        details = {"field": "email", "error": "Invalid format"}
        assert (
            json.loads(Http400Response(details=details).content)["details"] == details
        )

    def test_json_content_type(self) -> None:
        assert Http400Response()["Content-Type"] == "application/json"
