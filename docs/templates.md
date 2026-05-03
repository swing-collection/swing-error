# Templates

HTML error pages are rendered by the class-based error views and all built-in templates extend `swing_error/base_error.html`.

## Static stylesheet

The shared stylesheet now lives at `static/swing_error/css/error.css` and is loaded from the base template with Django's `{% static %}` tag.

## Per-status template overrides

Use `ERROR_HANDLER_CONFIG` to override the template for a specific status code:

```python
ERROR_HANDLER_CONFIG = {
    "404": {
        "template": "myapp/errors/404.html",
    },
    "500": {
        "template": "myapp/errors/500.html",
    },
}
```

The legacy key `template_name` is still accepted for backward compatibility, but `template` is the preferred key.

## Built-in defaults

- `400` -> `swing_error/400.html`
- `401` -> `swing_error/401.html`
- `403` -> `swing_error/403.html`
- `404` -> `swing_error/404.html`
- `405` -> `swing_error/405.html`
- `408` -> `swing_error/408.html`
- `410` -> `swing_error/410.html`
- `429` -> `swing_error/429.html`
- `500` -> `swing_error/500.html`

All built-in pages inherit the shared base template, so most custom branding can be handled by replacing the base stylesheet or overriding the per-status template.