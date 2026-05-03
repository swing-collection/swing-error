# Import | Standard Library
import json
from types import SimpleNamespace

from django.test import SimpleTestCase

from swing.error.responses import Http429Response


class TestHttp429Response(SimpleTestCase):
    def test_default_status_code(self) -> None:
        assert Http429Response().status_code == 429

    def test_default_message(self) -> None:
        assert (
            json.loads(Http429Response().content)["error"]
            == "Too Many Requests"
        )

    def test_retry_after_header(self) -> None:
        assert Http429Response(retry_after=60)["Retry-After"] == "60"

    def test_retry_after_detected_from_exception_headers(self) -> None:
        exception = SimpleNamespace(headers={"Retry-After": "120"})
        assert Http429Response(exception=exception)["Retry-After"] == "120"  # type: ignore[arg-type]

    def test_no_retry_after_header_by_default(self) -> None:
        assert "Retry-After" not in Http429Response()
