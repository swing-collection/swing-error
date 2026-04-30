"""Helper functions and fixtures for tests."""


def failing_callback(**kwargs):
    """A callback that always fails."""
    raise ValueError("Callback intentionally failed")


def working_callback(**kwargs):
    """A callback that works."""
    pass
