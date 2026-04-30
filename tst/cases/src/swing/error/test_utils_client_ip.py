from django.test import RequestFactory, SimpleTestCase

from swing.error.utils import get_client_ip


class TestClientIP(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_get_client_ip_from_remote_addr(self) -> None:
        request = self.factory.get("/", REMOTE_ADDR="192.168.1.1")
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_from_x_forwarded_for(self) -> None:
        request = self.factory.get(
            "/",
            HTTP_X_FORWARDED_FOR="10.0.0.1, 192.168.1.1",
            REMOTE_ADDR="127.0.0.1",
        )
        assert get_client_ip(request) == "10.0.0.1"

    def test_get_client_ip_from_x_real_ip(self) -> None:
        request = self.factory.get(
            "/",
            HTTP_X_REAL_IP="10.0.0.2",
            REMOTE_ADDR="127.0.0.1",
        )
        assert get_client_ip(request) == "10.0.0.2"
