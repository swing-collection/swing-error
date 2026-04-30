# Import | Standard Library
import json
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from swing.error.responses.response_error_base import BaseErrorResponse


class TestBaseErrorResponse(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_to_dict_includes_error_and_details(self) -> None:
        payload = BaseErrorResponse.to_dict(
            "Oops", {"field": "email"}, error_code="E001"
        )
        assert payload["error"] == "Oops"
        assert payload["details"] == {"field": "email"}
        assert payload["code"] == "E001"

    @patch("swing.error.responses.response_error_base.add_cors_headers")
    def test_response_sets_error_code_header(
        self, mock_add_cors_headers
    ) -> None:
        response = BaseErrorResponse(
            status_code=400, message="Bad Request", error_code="ERR-1"
        )
        assert response.status_code == 400
        assert response["X-Error-Code"] == "ERR-1"
        mock_add_cors_headers.assert_called_once()

    def test_response_serializes_to_json(self) -> None:
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=400, message="Bad Request", request=request
        )
        content = json.loads(response.content)
        assert content["error"] == "Bad Request"
        assert "details" in content
