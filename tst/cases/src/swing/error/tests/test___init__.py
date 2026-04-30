import swing.error.tests as tests_package


def test_legacy_tests_package_still_imports() -> None:
    assert tests_package is not None
