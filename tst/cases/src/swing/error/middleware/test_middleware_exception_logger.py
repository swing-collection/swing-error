# Import | Standard Library
from unittest.mock import MagicMock

from swing.error.middleware.middleware_exception_logger import (
    ExceptionLoggerMiddleware,
)


def test_exception_logger_middleware_process_exception_logs_exception() -> (
    None
):
    middleware = ExceptionLoggerMiddleware(lambda request: None)
    middleware.logger = MagicMock()

    middleware.process_exception(MagicMock(), ValueError("boom"))

    middleware.logger.exception.assert_called_once()
