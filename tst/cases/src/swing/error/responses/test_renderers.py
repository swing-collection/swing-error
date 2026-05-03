import json

from django.test import RequestFactory, SimpleTestCase

from swing.error.responses import BaseErrorResponse
from swing.error.responses.renderers import get_renderer, register_renderer


class TestErrorRenderers(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_problem_json_renderer_uses_rfc7807_content_type(self) -> None:
        request = self.factory.get("/api/errors/42", HTTP_ACCEPT="application/problem+json")
        response = BaseErrorResponse(
            status_code=422,
            message="Validation failed",
            details={"field": "email"},
            request=request,
            error_code="validation_error",
        )

        assert response["Content-Type"] == "application/problem+json"
        content = json.loads(response.content)
        assert content["title"] == "Validation failed"
        assert content["status"] == 422
        assert content["detail"] == "Validation failed"
        assert content["errors"] == {"field": "email"}
        assert content["instance"] == "/api/errors/42"

    def test_xml_renderer_serializes_xml_response(self) -> None:
        request = self.factory.get("/api/errors/42", HTTP_ACCEPT="application/xml")
        response = BaseErrorResponse(
            status_code=400,
            message="Bad Request",
            details={"field": "email"},
            request=request,
        )

        assert response["Content-Type"] == "application/xml"
        body = response.content.decode()
        assert "<error>" in body
        assert "<status>400</status>" in body
        assert "<field>email</field>" in body

    def test_yaml_renderer_serializes_yaml_response(self) -> None:
        request = self.factory.get("/api/errors/42", HTTP_ACCEPT="application/yaml")
        response = BaseErrorResponse(
            status_code=429,
            message="Too Many Requests",
            details="Retry later",
            request=request,
        )

        assert response["Content-Type"] == "application/yaml"
        body = response.content.decode()
        assert "error: \"Too Many Requests\"" in body
        assert "status: 429" in body

    def test_custom_renderer_can_be_registered(self) -> None:
        def custom_renderer(payload: dict[str, object], status_code: int) -> tuple[str, str]:
            return f"STATUS={status_code};ERROR={payload['error']}", "text/plain"

        register_renderer("plain-test", custom_renderer)

        request = self.factory.get("/api/errors/42")
        response = BaseErrorResponse(
            status_code=500,
            message="Server Error",
            request=request,
            renderer="plain-test",
        )

        assert get_renderer("plain-test") is custom_renderer
        assert response["Content-Type"] == "text/plain"
        assert response.content.decode() == "STATUS=500;ERROR=Server Error"