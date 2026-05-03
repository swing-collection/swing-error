from django.test import override_settings, RequestFactory, SimpleTestCase

from swing.error.responses import Http400Response
from swing.error.views.view_error_handler_base import BaseErrorView


class TestBaseErrorView(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        class InlineBaseView(BaseErrorView):
            error_type = "400"
            response_class = Http400Response

        self.view_class = InlineBaseView

    def test_get_returns_response_instance(self) -> None:
        response = self.view_class.as_view()(self.factory.get("/"))
        assert response.status_code == 400

    def test_default_message_comes_from_config(self) -> None:
        assert self.view_class().default_message == "Bad Request"

    def test_status_code_property_for_multiple_types(self) -> None:
        for status_code_str in [
            "400",
            "401",
            "403",
            "404",
            "405",
            "408",
            "410",
            "429",
            "500",
        ]:

            class TestView(BaseErrorView):
                error_type = status_code_str

            view = TestView()
            assert view.status_code == int(status_code_str)

    def test_get_template_names_returns_list(self) -> None:
        view = self.view_class()
        templates = view.get_template_names()
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert templates == ["swing_error/400.html"]

    @override_settings(ERROR_HANDLER_CONFIG={"400": {"template": "custom/400.html"}})
    def test_get_template_names_uses_template_override(self) -> None:
        view = self.view_class()
        assert view.get_template_names() == ["custom/400.html"]

    def test_default_details_property(self) -> None:
        view = self.view_class()
        details = view.default_details
        assert isinstance(details, dict)

    def test_default_context_property(self) -> None:
        view = self.view_class()
        context = view.default_context
        assert isinstance(context, dict)
        assert "title" in context or "message" in context

    def test_log_errors_property(self) -> None:
        view = self.view_class()
        assert view.log_errors is True

    def test_get_context_data(self) -> None:
        view = self.view_class()
        context = view.get_context_data()
        assert isinstance(context, dict)

    def test_get_with_request(self) -> None:
        request = self.factory.get("/test")
        response = self.view_class.as_view()(request)
        assert response.status_code == 400

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_request_info": True})
    def test_get_with_debug_enabled(self) -> None:
        request = self.factory.get("/test")
        response = self.view_class.as_view()(request)
        assert response.status_code == 400

    def test_log_error_method(self) -> None:
        view = self.view_class()
        request = self.factory.get("/test")
        view.log_error(request)
        # Just verify it doesn't raise

    def test_view_all_status_codes(self) -> None:
        for status in [
            "400",
            "401",
            "403",
            "404",
            "405",
            "408",
            "410",
            "429",
            "500",
        ]:

            class StatusView(BaseErrorView):
                error_type = status
                response_class = Http400Response

            view = StatusView()
            assert view.status_code == int(status)
