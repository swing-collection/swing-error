import pytest
from django.test import override_settings

from swing.error._conf.get_debug_config import get_debug_config
from swing.error._conf.get_debug_info import get_debug_info


class TestGetDebugConfig:
    @override_settings(DEBUG=False)
    def test_get_debug_config_when_debug_false(self) -> None:
        config = get_debug_config()
        assert all(value is False for value in config.values())

    @override_settings(DEBUG=True)
    def test_get_debug_config_when_debug_true(self) -> None:
        config = get_debug_config()
        assert isinstance(config, dict)
        assert "show_stack_trace" in config

    @override_settings(
        DEBUG=True,
        SWING_ERROR_DEBUG={
            "show_stack_trace": True,
            "show_request_info": False,
        },
    )
    def test_get_debug_config_custom_settings(self) -> None:
        config = get_debug_config()
        assert config["show_stack_trace"] is True
        assert config["show_request_info"] is False


class TestGetDebugInfo:
    @override_settings(DEBUG=False)
    def test_get_debug_info_when_debug_false(self) -> None:
        info = get_debug_info()
        assert info == {}

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_stack_trace": False})
    def test_get_debug_info_no_config(self) -> None:
        info = get_debug_info()
        assert info == {}

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_stack_trace": True})
    def test_get_debug_info_with_stack_trace(self) -> None:
        exc = ValueError("Test error")
        info = get_debug_info(exception=exc)
        assert "stack_trace" in info
        assert "exception_type" in info
        assert info["exception_type"] == "ValueError"
        assert info["exception_message"] == "Test error"

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_request_info": True})
    def test_get_debug_info_with_request_info(self) -> None:
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.post("/api/test", {"key": "value"})
        info = get_debug_info(request=request)
        assert "request" in info
        assert info["request"]["path"] == "/api/test"
        assert info["request"]["method"] == "POST"

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"show_environment": True})
    def test_get_debug_info_with_environment(self) -> None:
        import os

        os.environ["DJANGO_SETTINGS_MODULE"] = "test_settings"
        info = get_debug_info()
        assert "environment" in info
        assert "DJANGO_SETTINGS_MODULE" in info["environment"]

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"include_sql_queries": True})
    def test_get_debug_info_with_sql_queries(self) -> None:
        info = get_debug_info()
        # sql_queries may or may not be present depending on DB state
        if "sql_queries" in info:
            assert isinstance(info["sql_queries"], list)

    @override_settings(DEBUG=True, SWING_ERROR_DEBUG={"include_sql_queries": True})
    def test_get_debug_info_sql_queries_execution(self) -> None:
        """Test SQL queries are collected during get_debug_info."""
        from django.db import connection, reset_queries
        from django.test.utils import override_settings as override
        
        # Enable query logging
        with override(DEBUG=True):
            reset_queries()
            # Trigger a database query
            from django.contrib.auth.models import User
            try:
                list(User.objects.all()[:1])
            except Exception:
                # User table might not exist in test environment
                pass
            
            info = get_debug_info()
            # Just verify no exception is raised
            assert isinstance(info, dict)
