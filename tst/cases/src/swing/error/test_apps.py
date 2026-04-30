from swing.error.apps import SwingErrorConfig


def test_app_config_values() -> None:
    assert SwingErrorConfig.name == "swing.error"
    assert SwingErrorConfig.label == "swing_error"
    assert SwingErrorConfig.default_auto_field == "django.db.models.BigAutoField"
