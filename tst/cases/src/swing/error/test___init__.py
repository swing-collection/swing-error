from swing import error


def test_package_metadata_is_exposed() -> None:
    assert error.__author__ == "Lars van Vianen"
    assert error.__version__
    assert error.__status__ == "Alpha"
    assert error.__license__ == "Proprietary"


def test_package_public_api_is_curated() -> None:
    assert "ExceptionMiddleware" in error.__all__
    assert "BaseErrorResponse" in error.__all__
