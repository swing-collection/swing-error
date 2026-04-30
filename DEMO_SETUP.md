# Swing Error Demo Setup - Summary

## ✅ Demo Successfully Created

A complete Django demo application has been set up in the `exe/` directory to test and showcase swing-error functionality.

## 📁 Files Created/Modified

### New Files:
1. **exe/demo/views.py** - Demo views for testing all error responses
2. **exe/run_demo.sh** - Quick start script for macOS/Linux
3. **exe/run_demo.bat** - Quick start script for Windows
4. **exe/README_DEMO.md** - Comprehensive demo documentation

### Modified Files:
1. **exe/demo/settings.py** 
   - Added `ExceptionMiddleware` to `MIDDLEWARE`
   - Added swing-error configuration (CORS, DEBUG, TRACKING)

2. **exe/demo/urls.py**
   - Added import for demo views
   - Created URL patterns for all test endpoints
   - Organized routes by category (4xx, 5xx, API tests)

## 🎯 Features

### Error Response Tests (20+ endpoints)
- **4xx Errors**: 400, 401, 403, 404, 405, 408, 410, 429
- **5xx Errors**: 500, unhandled exceptions
- **API Tests**: JSON error and success responses
- **Home Page**: Interactive dashboard with links to all tests

### Key Testing Areas
1. **JSON Response Formatting** - All errors return proper JSON
2. **CORS Headers** - Correctly set on all responses
3. **Security Headers** - X-Content-Type-Options, X-Frame-Options, etc.
4. **Error Codes & Messages** - Properly formatted error information
5. **Debug Information** - Stack traces in DEBUG mode
6. **Exception Handling** - Middleware catches and formats exceptions

## 🚀 Quick Start

### Option 1: Using Shell Script (macOS/Linux)
```bash
cd exe
bash run_demo.sh
```

### Option 2: Using Batch Script (Windows)
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
Open your browser to: **http://localhost:8000**

## 📊 Test Endpoints

| Endpoint | Status | Test Purpose |
|----------|--------|--------------|
| `/` | 200 | Home page / link dashboard |
| `/test/400/` | 400 | Bad Request |
| `/test/401/` | 401 | Unauthorized |
| `/test/403/` | 403 | Forbidden |
| `/test/404/` | 404 | Not Found |
| `/test/405/` | 405 | Method Not Allowed |
| `/test/408/` | 408 | Request Timeout |
| `/test/410/` | 410 | Gone |
| `/test/429/` | 429 | Too Many Requests (with Retry-After) |
| `/test/500/` | 500 | Internal Server Error |
| `/test/exception/` | 500 | Unhandled Exception |
| `/api/json-error/` | 400 | JSON Error Response |
| `/api/success/` | 200 | JSON Success Response |
| `/admin/` | 200 | Django Admin |

## 🔧 Configuration

### Swing Error Settings (demo/settings.py)

```python
SWING_ERROR_CORS = {
    "enabled": True,
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
}

SWING_ERROR_DEBUG = {
    "show_stack_trace": DEBUG,        # Show traces in DEBUG mode
    "show_request_info": DEBUG,       # Show request details
    "show_environment": DEBUG,        # Show environment variables
    "include_sql_queries": DEBUG,     # Include SQL queries
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
    "swing.error.middleware.ExceptionMiddleware",  # Error handling
]
```

## 🧪 Testing with cURL

### Test JSON 400 Error:
```bash
curl -H "Accept: application/json" http://localhost:8000/test/400/
```

### Test with Retry-After Header:
```bash
curl -i http://localhost:8000/test/429/
```

### Test Exception Handling:
```bash
curl -v http://localhost:8000/test/exception/
```

## 📝 Browser DevTools Testing

1. Open http://localhost:8000
2. Press **F12** to open Developer Tools
3. Click on any error test link
4. In DevTools, inspect:
   - **Network** tab: Status code, response headers
   - **Response** tab: JSON payload
   - **Headers** tab: CORS and security headers

### Headers to Check
- `Access-Control-Allow-Origin` - CORS origin
- `X-Content-Type-Options` - Prevents MIME sniffing
- `X-Frame-Options` - Prevents clickjacking
- `Referrer-Policy` - Referrer behavior
- `Content-Type` - Always `application/json`

## 📚 Documentation Files

- **exe/README.md** - Original demo readme
- **exe/README_DEMO.md** - Comprehensive demo guide
- **exe/demo/settings.py** - Django configuration with comments
- **exe/demo/urls.py** - URL routing with documentation
- **exe/demo/views.py** - View functions with docstrings

## 🎓 What to Learn

By using this demo, you'll understand:
1. How swing-error handles different HTTP status codes
2. How JSON error responses are formatted
3. How CORS headers are applied to error responses
4. How security headers protect error responses
5. How the exception middleware catches and formats exceptions
6. How debug information is included in development mode
7. How retry-after headers work with 429 responses

## 🔗 Related Project Files

- Project tests: `tst/` - 183 tests with 94.12% coverage
- Main error app: `src/swing/error/`
- Configuration: `pyproject.toml`

## ✨ Demo Highlights

✅ **Complete Error Testing** - Test all HTTP error codes
✅ **Interactive UI** - Beautiful home page with clickable links
✅ **JSON Responses** - All errors return proper JSON
✅ **Security Headers** - CORS and security headers tested
✅ **Debug Mode** - See detailed error information
✅ **Exception Handling** - Middleware catches all exceptions
✅ **API Responses** - Test both errors and success responses
✅ **Easy to Run** - One-command startup scripts

## 🚨 Troubleshooting

### Port 8000 already in use:
```bash
python manage.py runserver 8001
```

### Import errors:
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
```

### Database errors:
```bash
rm exe/db.sqlite3
python exe/manage.py migrate
```

## 📞 Next Steps

1. Run the demo: `bash exe/run_demo.sh` or `python exe/manage.py runserver`
2. Open http://localhost:8000 in your browser
3. Click on error endpoints to test responses
4. Open DevTools (F12) to inspect headers and payloads
5. Review the response JSON format and headers
6. Modify settings in `exe/demo/settings.py` to test different configurations

Happy testing! 🎉
