from django.test import RequestFactory, SimpleTestCase

from swing.error.utils import generate_request_id, get_request_id


class TestRequestTracking(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_generate_request_id_is_unique(self) -> None:
        assert generate_request_id() != generate_request_id()

    def test_get_request_id_uses_existing_header(self) -> None:
        request = self.factory.get("/", HTTP_X_REQUEST_ID="existing-id-123")
        assert get_request_id(request) == "existing-id-123"

    def test_get_request_id_generates_new_if_missing(self) -> None:
        request = self.factory.get("/")
        assert get_request_id(request)
