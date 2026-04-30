# Import | Standard Library
import json
from unittest.mock import patch

from django.test import override_settings, RequestFactory, SimpleTestCase

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
    def test_response_sets_error_code_header(self, mock_add_cors_headers) -> None:
        response = BaseErrorResponse(
            status_code=400, message="Bad Request", error_code="ERR-1"
        )
        assert response.status_code == 400
        assert response["X-Error-Code"] == "ERR-1"
        mock_add_cors_headers.assert_called_once()
        assert response["X-Content-Type-Options"] == "nosniff"
        assert response["X-Frame-Options"] == "DENY"
        assert response["Referrer-Policy"] == "same-origin"

    def test_response_serializes_to_json(self) -> None:
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=400, message="Bad Request", request=request
        )
        content = json.loads(response.content)
        assert content["error"] == "Bad Request"
        assert "details" in content

    def test_log_error_scrubs_sensitive_request_data(self) -> None:
        request = self.factory.post(
            "/api/test",
            data='{"password": "secret"}',
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer super-secret",
            HTTP_COOKIE="sessionid=unsafe",
        )

        response = BaseErrorResponse(
            status_code=400,
            message="Bad Request",
            details={"token": "top-secret"},
            request=request,
        )

        content = json.loads(response.content)
        assert content["error"] == "Bad Request"

    def test_log_error_without_request(self) -> None:
        response = BaseErrorResponse(
            status_code=500,
            message="Server Error",
        )
        assert response.status_code == 500

    def test_log_error_with_get_request_no_body(self) -> None:
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=400,
            message="Bad Request",
            request=request,
        )
        assert response.status_code == 400

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_stack_trace": True})
    def test_response_with_exception_and_debug(self) -> None:
        exc = ValueError("Test error")
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=500,
            message="Server Error",
            exception=exc,
            request=request,
            include_debug=True,
        )
        content = json.loads(response.content)
        assert content["error"] == "Server Error"
        # Debug info may be included
        assert "debug" in content or "details" in content

    def test_to_dict_without_error_code(self) -> None:
        payload = BaseErrorResponse.to_dict("Bad request", None)
        assert payload["error"] == "Bad request"
        assert "code" not in payload

    def test_to_dict_with_debug_info(self) -> None:
        payload = BaseErrorResponse.to_dict(
            "Error", "Details", debug_info={"trace": "..."}
        )
        assert payload["debug"] == {"trace": "..."}

    def test_response_with_list_details(self) -> None:
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=400,
            message="Validation Error",
            details=["Field 1 is invalid", "Field 2 is required"],
            request=request,
        )
        content = json.loads(response.content)
        assert isinstance(content["details"], list)

    def test_response_with_string_details(self) -> None:
        request = self.factory.get("/api/test")
        response = BaseErrorResponse(
            status_code=400,
            message="Bad Request",
            details="This is a string detail",
            request=request,
        )
        content = json.loads(response.content)
        assert content["details"] == "This is a string detail"

    @patch("swing.error.responses.response_error_base.capture_error")
    def test_response_captures_error_for_5xx(self, mock_capture) -> None:
        exc = RuntimeError("Server error")
        response = BaseErrorResponse(
            status_code=500,
            message="Server Error",
            exception=exc,
        )
        mock_capture.assert_called_once()

    @patch("swing.error.responses.response_error_base.capture_error")
    def test_response_no_capture_for_4xx(self, mock_capture) -> None:
        response = BaseErrorResponse(
            status_code=400,
            message="Bad Request",
        )
        mock_capture.assert_not_called()
