from swing import error


def test_package_metadata_is_exposed() -> None:
    assert error.__author__ == "Lars van Vianen"
    assert error.__version__
    assert error.__status__ == "Alpha"
