# Swing Error Demo

This directory contains a Django demo application to test and showcase the `swing-error` package functionality.

## Quick Start

### 1. Install Dependencies

The demo uses the project's virtual environment. Make sure you're in the project root:

```bash
cd /path/to/swing-error
source .venv/bin/activate
```

### 2. Run the Django Development Server

From the project root, run:

```bash
python exe/manage.py runserver
```

Or specify a port:

```bash
python exe/manage.py runserver 8000
```

### 3. Open in Browser

Navigate to:
```
http://localhost:8000
```

## Demo Features

The demo provides interactive testing of various HTTP error responses:

### 4xx Client Error Tests
- **400 Bad Request** - Invalid request parameters
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Access denied
- **404 Not Found** - Resource not found
- **405 Method Not Allowed** - Method not supported
- **408 Request Timeout** - Request timeout
- **410 Gone** - Resource no longer available
- **429 Too Many Requests** - Rate limit exceeded

### 5xx Server Error Tests
- **500 Internal Server Error** - Server error response
- **Unhandled Exception** - Tests the exception middleware

### API Response Tests
- **JSON Error Response** - Tests JSON error formatting
- **JSON Success Response** - Tests successful JSON response

## What to Look For

### Browser Testing
1. Click on any error link to see the error response
2. Open Developer Tools (F12) to inspect:
   - Response headers (including CORS, security headers, etc.)
   - Response body (JSON format)
   - Status code

### Response Features
- **JSON Formatting**: All responses are formatted as JSON
- **CORS Headers**: Properly set CORS headers on responses
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, etc.
- **Error Details**: Error code, message, and optionally debug information
- **Request Tracking**: Request path, method, and user info in logs

### Testing with cURL

Test 400 Bad Request:
```bash
curl -v http://localhost:8000/test/400/
```

Test 429 with custom Retry-After header:
```bash
curl -v http://localhost:8000/test/429/
```

Test with JSON Accept header:
```bash
curl -H "Accept: application/json" http://localhost:8000/test/500/
```

## Configuration

The demo is configured via `demo/settings.py`:

### Error Handling Configuration

```python
SWING_ERROR_CORS = {
    "enabled": True,
    "allow_origins": ["*"],
    "allow_credentials": True,
}

SWING_ERROR_DEBUG = {
    "show_stack_trace": True,      # In DEBUG mode
    "show_request_info": True,
    "show_environment": True,
    "include_sql_queries": True,
}

SWING_ERROR_TRACKING = {
    "enabled": True,
    "capture_exceptions": True,
    "capture_messages": True,
}
```

### Middleware

The ExceptionMiddleware is configured in `MIDDLEWARE`:

```python
MIDDLEWARE = [
    # ... other middleware ...
    "swing.error.middleware.ExceptionMiddleware",
]
```

## Database

The demo uses SQLite for simplicity. Database file:
```
exe/db.sqlite3
```

To reset the database:
```bash
rm exe/db.sqlite3
python exe/manage.py migrate
```

## Admin Panel

Access Django admin at:
```
http://localhost:8000/admin/
```

Default admin credentials (if created):
- Username: `admin`
- Password: (run `python exe/manage.py createsuperuser` to create)

## Testing Error Responses

### View Response Headers

Using cURL with verbose output:
```bash
curl -v -H "Accept: application/json" http://localhost:8000/test/400/
```

Look for:
- `Access-Control-Allow-Origin`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Content-Type: application/json`

### Test Different Accept Types

HTML response:
```bash
curl -H "Accept: text/html" http://localhost:8000/test/400/
```

JSON response:
```bash
curl -H "Accept: application/json" http://localhost:8000/test/400/
```

## Development

To add more test cases:

1. Create a new view in `demo/views.py`
2. Add a URL pattern in `demo/urls.py`
3. Add a link to the home page
4. Restart the development server

Example:
```python
# In views.py
@require_http_methods(["GET"])
def test_custom_error(request):
    from swing.error.responses import Http400Response
    return Http400Response(request=request, message="Custom error message")

# In urls.py
path("test/custom/", views.test_custom_error, name="test_custom"),

# In templates/home.html
<a href="/test/custom/">Test Custom Error</a>
```

## Troubleshooting

### Error: "swing.error app not found"
Make sure the project is properly installed and the virtual environment is activated.

### Port already in use
Use a different port:
```bash
python exe/manage.py runserver 8001
```

### Database errors
Reset migrations:
```bash
rm exe/db.sqlite3
python exe/manage.py migrate
```

## Related Files

- `demo/settings.py` - Django settings configuration
- `demo/urls.py` - URL routing
- `demo/views.py` - View functions for error testing
- `demo/wsgi.py` - WSGI application entry point
- `manage.py` - Django management script

## Further Testing

For comprehensive testing, use the project's test suite:
```bash
python -m pytest tst --cov=src/swing/error
```

See the main project README for more information about running tests.
