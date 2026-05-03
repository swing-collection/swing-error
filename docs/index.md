## swing.error

Reusable Django error handling with structured responses, configurable error pages, and optional integrations for tracking and debugging.

### What is included

- Status-specific response classes for `400`, `401`, `403`, `404`, `405`, `408`, `410`, `429`, and `500`
- Middleware for automatic exception capture and error response generation
- Class-based error views with per-status template overrides
- Pluggable response renderers for JSON, XML, YAML, and RFC 7807 problem details
- Optional CORS headers, debug payloads, and tracking hooks

### Documentation map

- Use [quick_start.md](quick_start.md) to wire the package into a Django project.
- Use [templates.md](templates.md) to customize HTML error pages and CSS.
- Use [renderers.md](renderers.md) to configure JSON, XML, YAML, and custom renderers.
- Use [problem_details.md](problem_details.md) to opt into `application/problem+json`.
- Use [api_reference.md](api_reference.md) for generated API reference pages.
