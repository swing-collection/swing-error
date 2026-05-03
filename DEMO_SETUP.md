# Swing Error Demo Setup Summary

## Demo Successfully Created

A complete Django demo application has been set up in the `exe/` directory to test and showcase swing-error functionality.

## Files Created and Modified

### New Files

1. `exe/demo/views.py`: Demo views for testing all error responses
2. `exe/run_demo.sh`: Quick start script for macOS and Linux
3. `exe/run_demo.bat`: Quick start script for Windows
4. `exe/README_DEMO.md`: Comprehensive demo documentation

### Modified Files

1. `exe/demo/settings.py`
2. `exe/demo/urls.py`

Updates made in `exe/demo/settings.py`:

- Added `ExceptionMiddleware` to `MIDDLEWARE`
- Added swing-error configuration for CORS, debug, and tracking

Updates made in `exe/demo/urls.py`:

- Added imports for demo views
- Created URL patterns for all test endpoints
- Organized routes by category for `4xx`, `5xx`, and API tests

## Features

### Error Response Tests

- `4xx` errors: `400`, `401`, `403`, `404`, `405`, `408`, `410`, `429`
- `5xx` errors: `500` and unhandled exceptions
- API tests: JSON error and success responses
- Home page: interactive dashboard with links to all tests

### Key Testing Areas

1. JSON response formatting
2. CORS headers
3. Security headers
4. Error codes and messages
5. Debug information in development mode
6. Exception handling through middleware

## Quick Start

### Option 1: Shell Script (macOS/Linux)

```bash
cd exe
bash run_demo.sh
```

### Option 2: Batch Script (Windows)

```cmd
cd exe
run_demo.bat
```

### Option 3: Manual Start

```bash
cd exe
python manage.py runserver
```

### Access the Demo

Open your browser at <http://localhost:8000>.

## Test Endpoints

| Endpoint | Status | Test Purpose |
| --- | --- | --- |
| `/` | 200 | Home page and link dashboard |
| `/test/400/` | 400 | Bad Request |
| `/test/401/` | 401 | Unauthorized |
| `/test/403/` | 403 | Forbidden |
| `/test/404/` | 404 | Not Found |
| `/test/405/` | 405 | Method Not Allowed |
| `/test/408/` | 408 | Request Timeout |
| `/test/410/` | 410 | Gone |
| `/test/429/` | 429 | Too Many Requests with `Retry-After` |
| `/test/500/` | 500 | Internal Server Error |
| `/test/exception/` | 500 | Unhandled exception |
| `/api/json-error/` | 400 | JSON error response |
| `/api/success/` | 200 | JSON success response |
| `/admin/` | 200 | Django admin |

## Configuration

### Swing Error Settings (`demo/settings.py`)

```python
SWING_ERROR_CORS = {
    "enabled": True,
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
}

SWING_ERROR_DEBUG = {
    "show_stack_trace": DEBUG,
    "show_request_info": DEBUG,
    "show_environment": DEBUG,
    "include_sql_queries": DEBUG,
}

SWING_ERROR_TRACKING = {
    "enabled": True,
    "capture_exceptions": True,
    "capture_messages": True,
}
```

### Middleware Configuration

```python
MIDDLEWARE = [
    # ... other middleware ...
    "swing.error.middleware.ExceptionMiddleware",
]
```

## Testing with cURL

### Test JSON `400` Error

```bash
curl -H "Accept: application/json" http://localhost:8000/test/400/
```

### Test `Retry-After` Header

```bash
curl -i http://localhost:8000/test/429/
```

### Test Exception Handling

```bash
curl -v http://localhost:8000/test/exception/
```

## Browser DevTools Testing

1. Open <http://localhost:8000>.
2. Press `F12` to open Developer Tools.
3. Click any error test link.
4. Inspect the following panels:

- Network: status code and response headers
- Response: JSON payload
- Headers: CORS and security headers

### Headers to Check

- `Access-Control-Allow-Origin`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Content-Type: application/json`

## Documentation Files

- `exe/README.md`: Original demo readme
- `exe/README_DEMO.md`: Comprehensive demo guide
- `exe/demo/settings.py`: Django configuration with comments
- `exe/demo/urls.py`: URL routing with documentation
- `exe/demo/views.py`: View functions with docstrings

## What to Learn

By using this demo, you can understand:

1. How swing-error handles different HTTP status codes
2. How JSON error responses are formatted
3. How CORS headers are applied to error responses
4. How security headers protect error responses
5. How the exception middleware catches and formats exceptions
6. How debug information is included in development mode
7. How `Retry-After` headers work with `429` responses

## Related Project Files

- Project tests: `tst/` with `183` tests and `94.12%` coverage
- Main error app: `src/swing/error/`
- Configuration: `pyproject.toml`

## Demo Highlights

- Complete error testing across the main HTTP error codes
- Interactive UI with clickable links
- JSON responses for errors and success cases
- CORS and security header coverage
- Debug mode inspection
- Exception middleware behavior
- Easy startup scripts

## Troubleshooting

### Port `8000` Already in Use

```bash
python manage.py runserver 8001
```

### Import Errors

```bash
source .venv/bin/activate
```

### Database Errors

```bash
rm exe/db.sqlite3
python exe/manage.py migrate
```

## Next Steps

1. Run the demo with `bash exe/run_demo.sh` or `python exe/manage.py runserver`.
2. Open <http://localhost:8000> in your browser.
3. Click error endpoints to inspect responses.
4. Open DevTools (`F12`) to inspect headers and payloads.
5. Modify `exe/demo/settings.py` to test different configurations.
