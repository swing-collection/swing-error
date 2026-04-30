from swing.error import responses


def test_responses_package_exports_known_response_classes() -> None:
    assert responses.Http400Response.__name__ == "Http400Response"
    assert responses.Http500Response.__name__ == "Http500Response"
