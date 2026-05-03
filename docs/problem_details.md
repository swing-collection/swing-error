# Problem Details

RFC 7807 problem details are supported as an opt-in API response format via `Accept: application/problem+json`.

## Example

```http
GET /api/resource HTTP/1.1
Accept: application/problem+json
```

Example response body:

```json
{
  "type": "about:blank",
  "title": "Validation failed",
  "status": 422,
  "detail": "Validation failed",
  "errors": {
    "field": "email"
  },
  "code": "validation_error",
  "instance": "/api/resource"
}
```

## Mapping

- `title` comes from the response message
- `status` comes from the HTTP status code
- `detail` is the string detail, or falls back to the message when structured details are present
- `errors` carries structured detail payloads when available
- `instance` is populated from `request.path`

This keeps the existing package API stable while offering a standards-based payload for API clients.