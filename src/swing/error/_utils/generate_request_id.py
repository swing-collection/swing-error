# Import | Standard Library
import uuid


def generate_request_id() -> str:
    """Return a new UUID4 request identifier as a string."""
    return str(uuid.uuid4())
