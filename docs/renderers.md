# Renderers

`swing.error` now uses a renderer registry for API-oriented error responses.

## Built-in renderers

- `json` -> `application/json`
- `problem+json` -> `application/problem+json`
- `xml` -> `application/xml`
- `yaml` -> `application/yaml`

The active renderer is negotiated from the request `Accept` header. HTML views continue to use templates; API responses use the registry.

## Custom renderer registration

Register a renderer at startup, for example in your Django app config:

```python
from swing.error.responses import register_renderer


def render_plain_text(payload: dict[str, object], status_code: int) -> tuple[str, str]:
    return f"STATUS={status_code};ERROR={payload['error']}", "text/plain"


register_renderer("plain", render_plain_text)
```

Then select it explicitly when constructing a response:

```python
from swing.error.responses import BaseErrorResponse


def error_view(request):
    return BaseErrorResponse(
        status_code=500,
        message="Server Error",
        request=request,
        renderer="plain",
    )
```

## Negotiation rules

- `text/html` keeps the HTML view path
- `application/problem+json` selects RFC 7807 output
- `application/xml` and `text/xml` select the XML renderer
- `application/yaml`, `application/x-yaml`, and `text/yaml` select the YAML renderer
- Unknown media types fall back to JSON