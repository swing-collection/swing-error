# https://docs.djangoproject.com/en/2.1/topics/http/views/#testing-custom-error-views
# https://stackoverflow.com/questions/54124699/how-to-test-django-400-bad-request-error-for-custom-error-page

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.test import override_settings, SimpleTestCase
from django.urls import path


class CustomErrorHandlerModule:
    @staticmethod
    def response_error_handler(
        request: HttpRequest,
        exception: Exception | None = None,
    ) -> HttpResponse:
        del request, exception
        return HttpResponse("Error handler content", status=403)

    @staticmethod
    def permission_denied_view(request: HttpRequest) -> HttpResponse:
        del request
        raise PermissionDenied

    @override_settings(ROOT_URLCONF=__name__)
    class CustomErrorHandlerTests(SimpleTestCase):
        def test_handler_renders_template_response(self) -> None:
            response = self.client.get("/403/")
            self.assertContains(response, "Error handler content", status_code=403)


urlpatterns = [path("403/", CustomErrorHandlerModule.permission_denied_view)]
handler403 = CustomErrorHandlerModule.response_error_handler
CustomErrorHandlerTests = CustomErrorHandlerModule.CustomErrorHandlerTests
