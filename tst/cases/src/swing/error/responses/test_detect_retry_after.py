# Import | Standard Library
from types import SimpleNamespace

# Import | Libraries

from swing.error.responses.detect_retry_after import detect_retry_after


class TestDetectRetryAfter:
    def test_detect_retry_after_from_exception_attribute(self) -> None:
        exc = SimpleNamespace(retry_after=60)
        assert detect_retry_after(exception=exc) == 60  # type: ignore[arg-type]

    def test_detect_retry_after_from_exception_response(self) -> None:
        response = SimpleNamespace(headers={"Retry-After": "120"})
        exc = SimpleNamespace(response=response)
        assert detect_retry_after(exception=exc) == 120  # type: ignore[arg-type]

    def test_detect_retry_after_from_exception_detail(self) -> None:
        detail = SimpleNamespace(wait=90)
        exc = SimpleNamespace(detail=detail)
        assert detect_retry_after(exception=exc) == 90  # type: ignore[arg-type]

    def test_detect_retry_after_from_request_rate_limit_info_dict(
        self,
    ) -> None:
        request = SimpleNamespace(
            rate_limit=None, rate_limit_info={"retry_after": 300}
        )
        assert detect_retry_after(request=request) == 300

    def test_detect_retry_after_from_dict_candidate(self) -> None:
        exc = SimpleNamespace(retry_after=None)
        exc.some_dict = {"retry_after": 75}
        request = SimpleNamespace(
            rate_limit=None,
            rate_limit_info={"remaining": 0, "retry_after": 150},
        )
        assert detect_retry_after(exception=exc, request=request) == 150  # type: ignore[arg-type]

    def test_detect_retry_after_prefers_first_valid_value(self) -> None:
        exc = SimpleNamespace(
            retry_after=60,
            response=SimpleNamespace(headers={"Retry-After": "999"}),
        )
        assert detect_retry_after(exception=exc) == 60  # type: ignore[arg-type]

    def test_detect_retry_after_returns_none_when_not_found(self) -> None:
        assert detect_retry_after() is None

    def test_detect_retry_after_with_none_candidates(self) -> None:
        exc = SimpleNamespace(retry_after=None, response=None, detail=None)
        request = SimpleNamespace(rate_limit=None, rate_limit_info=None)
        assert detect_retry_after(exception=exc, request=request) is None  # type: ignore[arg-type]

    def test_detect_retry_after_invalid_header_value(self) -> None:
        response = SimpleNamespace(headers={"Retry-After": "invalid"})
        exc = SimpleNamespace(response=response)
        assert detect_retry_after(exception=exc) is None  # type: ignore[arg-type]

    def test_detect_retry_after_from_dict_candidate_wait(self) -> None:
        request = SimpleNamespace(
            rate_limit=None,
            rate_limit_info={"wait": 45},
        )
        assert detect_retry_after(request=request) == 45

    def test_detect_retry_after_from_dict_candidate_remaining(self) -> None:
        request = SimpleNamespace(
            rate_limit=None,
            rate_limit_info={"remaining": 30},
        )
        assert detect_retry_after(request=request) == 30

    def test_detect_retry_after_from_dict_candidate_time_left(self) -> None:
        request = SimpleNamespace(
            rate_limit=None,
            rate_limit_info={"time_left": 15},
        )
        assert detect_retry_after(request=request) == 15
