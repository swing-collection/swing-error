import pytest

from swing.error._conf.import_callback import import_callback


class TestImportCallback:
    def test_import_callback_valid_function(self) -> None:
        callback = import_callback("swing.error._conf.import_callback.import_callback")
        assert callable(callback)

    def test_import_callback_invalid_module(self) -> None:
        with pytest.raises(ImportError):
            import_callback("nonexistent.module.function")

    def test_import_callback_invalid_function(self) -> None:
        with pytest.raises(AttributeError):
            import_callback("swing.error._conf.import_callback.nonexistent_function")
