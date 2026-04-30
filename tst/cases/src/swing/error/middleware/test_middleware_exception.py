# Import | Standard Library
import json

from django.test import RequestFactory, SimpleTestCase

from swing.error.middleware import ExceptionMiddleware
from swing.error.responses import (
    Http401Response,
    Http404Response,
    Http500Response,
)


class TestExceptionMiddleware(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        def get_response_ok(request):
            from django.http import HttpResponse

            return HttpResponse("OK", status=200)

        def get_response_error(request):
            raise ValueError("Test exception")

        self.middleware = ExceptionMiddleware(get_response_ok)
        self.middleware_error = ExceptionMiddleware(get_response_error)

    def test_middleware_returns_200_for_ok_response(self) -> None:
        request = self.factory.get("/")
        response = self.middleware(request)
        assert response.status_code == 200

    def test_middleware_handles_unhandled_exception(self) -> None:
        request = self.factory.get("/")
        response = self.middleware_error(request)
        assert response.status_code == 500

    def test_middleware_returns_json_for_exception(self) -> None:
        request = self.factory.get("/", HTTP_ACCEPT="application/json")
        response = self.middleware_error(request)
        assert "application/json" in response.get("Content-Type", "")
        content = json.loads(response.content)
        assert "error" in content

    def test_middleware_with_401_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http401Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 401

    def test_middleware_with_404_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http404Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 404

    def test_middleware_with_500_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http500Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 500
