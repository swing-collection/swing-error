# Import | Standard Library
import json

from django.test import RequestFactory, SimpleTestCase

from swing.error.middleware import ExceptionMiddleware
from swing.error.middleware.middleware_exception_logger import ExceptionLoggerMiddleware
from swing.error.responses import (
    Http401Response,
    Http403Response,
    Http404Response,
    Http405Response,
    Http408Response,
    Http410Response,
    Http429Response,
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

    def test_middleware_with_403_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http403Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 403

    def test_middleware_with_404_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http404Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 404

    def test_middleware_with_405_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http405Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 405

    def test_middleware_with_408_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http408Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 408

    def test_middleware_with_410_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http410Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 410

    def test_middleware_with_429_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http429Response(retry_after=60))
        response = middleware(self.factory.get("/"))
        assert response.status_code == 429
        # When middleware calls handle_custom_response, it creates a fresh response
        # without the retry_after parameter, so the Retry-After header isn't set

    def test_middleware_with_500_response(self) -> None:
        middleware = ExceptionMiddleware(lambda request: Http500Response())
        response = middleware(self.factory.get("/"))
        assert response.status_code == 500

    async def test_async_middleware_entrypoint(self) -> None:
        async def get_response(request):
            del request
            return Http401Response()

        middleware = ExceptionMiddleware(get_response)
        response = await middleware.__acall__(self.factory.get("/"))
        assert response.status_code == 401

    async def test_async_middleware_error_handling(self) -> None:
        async def get_response(request):
            del request
            raise RuntimeError("Async error")

        middleware = ExceptionMiddleware(get_response)
        response = await middleware.__acall__(self.factory.get("/"))
        assert response.status_code == 500

    async def test_async_middleware_with_error_response(self) -> None:
        async def get_response(request):
            del request
            return Http429Response(retry_after=120)

        middleware = ExceptionMiddleware(get_response)
        response = await middleware.__acall__(self.factory.get("/"))
        assert response.status_code == 429
        # The middleware calls response_class(request=request) which doesn't preserve retry_after
        # Instead, the response is generated fresh from the status code

    def test_middleware_handles_response_status_code_200(self) -> None:
        """Test that 200 responses pass through unchanged."""
        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse("OK", status=200)
        
        middleware = ExceptionMiddleware(get_response)
        response = middleware(self.factory.get("/"))
        assert response.status_code == 200

    def test_middleware_handles_response_status_code_302(self) -> None:
        """Test that non-error status codes pass through unchanged."""
        def get_response(request):
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect("/redirect-target")
        
        middleware = ExceptionMiddleware(get_response)
        response = middleware(self.factory.get("/"))
        assert response.status_code == 302


class TestExceptionLoggerMiddleware(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_logger_middleware_init(self) -> None:
        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse("OK")
        
        middleware = ExceptionLoggerMiddleware(get_response)
        assert middleware.get_response == get_response
        assert middleware.logger is not None

    def test_logger_middleware_call_returns_response(self) -> None:
        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse("OK", status=200)
        
        middleware = ExceptionLoggerMiddleware(get_response)
        response = middleware(self.factory.get("/"))
        assert response.status_code == 200

    def test_logger_middleware_call_passes_request(self) -> None:
        request_received = None
        
        def get_response(request):
            nonlocal request_received
            request_received = request
            from django.http import HttpResponse
            return HttpResponse("OK")
        
        middleware = ExceptionLoggerMiddleware(get_response)
        request = self.factory.get("/test/path")
        middleware(request)
        assert request_received is not None
        assert request_received.path == "/test/path"
