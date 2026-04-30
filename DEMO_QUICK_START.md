# 🚀 Swing Error Demo - Quick Reference Card

## ⚡ Start Demo in 10 Seconds

### macOS/Linux
```bash
cd exe && bash run_demo.sh
```

### Windows
```cmd
cd exe && run_demo.bat
```

### Manual (Any OS)
```bash
cd exe && python manage.py runserver
```

Then open: **http://localhost:8000**

---

## 🎯 Available Test Endpoints

| URL | Status | Description |
|-----|--------|-------------|
| `/` | 200 | Home page with all links |
| `/test/400/` | 400 | Bad Request demo |
| `/test/401/` | 401 | Unauthorized demo |
| `/test/403/` | 403 | Forbidden demo |
| `/test/404/` | 404 | Not Found demo |
| `/test/405/` | 405 | Method Not Allowed demo |
| `/test/408/` | 408 | Request Timeout demo |
| `/test/410/` | 410 | Gone demo |
| `/test/429/` | 429 | Rate Limit demo (with Retry-After) |
| `/test/500/` | 500 | Server Error demo |
| `/test/exception/` | 500 | Unhandled Exception demo |
| `/api/json-error/` | 400 | JSON API Error demo |
| `/api/success/` | 200 | JSON API Success demo |
| `/admin/` | 200 | Django Admin |

---

## 🧪 Test with cURL

```bash
# Test 400 error
curl http://localhost:8000/test/400/

# Test JSON response
curl -H "Accept: application/json" http://localhost:8000/test/400/

# Test with headers
curl -i http://localhost:8000/test/429/

# Test exception handling
curl http://localhost:8000/test/exception/
```

---

## 🔍 What to Check in Browser DevTools (F12)

### Network Tab
- ✅ Status code (400, 401, 404, 429, 500, etc.)
- ✅ Content-Type: application/json
- ✅ Response time

### Response Tab
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional details",
  "debug": { /* in DEBUG mode only */ }
}
```

### Headers Tab
- ✅ `Access-Control-Allow-Origin`
- ✅ `X-Content-Type-Options`
- ✅ `X-Frame-Options`
- ✅ `Referrer-Policy`
- ✅ `Retry-After` (for 429 responses)

---

## 📋 Configuration Files

| File | Purpose |
|------|---------|
| `exe/demo/settings.py` | Django settings + swing-error config |
| `exe/demo/urls.py` | URL routing for test endpoints |
| `exe/demo/views.py` | Test view functions |
| `exe/demo/wsgi.py` | WSGI application |
| `exe/manage.py` | Django management script |

---

## 🔧 Modify Settings

Edit `exe/demo/settings.py` to test different configurations:

```python
# Enable/disable CORS
SWING_ERROR_CORS = {"enabled": True, ...}

# Show debug info
SWING_ERROR_DEBUG = {"show_stack_trace": True, ...}

# Enable error tracking
SWING_ERROR_TRACKING = {"enabled": True, ...}
```

Then restart the server to see changes.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `python manage.py runserver 8001` |
| Virtual env not activated | `source ../.venv/bin/activate` |
| Import errors | Check virtual environment activation |
| Database errors | Delete `db.sqlite3` and restart |
| Permission denied on `.sh` | `chmod +x run_demo.sh` |

---

## 📚 Documentation

- **DEMO_SETUP.md** - Complete setup guide
- **exe/README_DEMO.md** - Detailed demo documentation
- **exe/README.md** - Original README

---

## ✨ Key Features Demonstrated

✅ JSON error response formatting
✅ CORS header handling
✅ Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
✅ Error code and message formatting
✅ Debug information display
✅ Exception middleware handling
✅ Retry-After header for 429 responses
✅ Request tracking and logging

---

## 🎓 Learning Path

1. Start the demo
2. Click through all error endpoints
3. Open DevTools (F12) to inspect responses
4. Check response headers and JSON format
5. Modify settings and restart to see changes
6. Test with cURL for different scenarios
7. Review the view code in `demo/views.py`

---

## 💡 Pro Tips

- Use **F12 DevTools** to see full response details
- Use **cURL with `-v`** for detailed request/response info
- Check **Browser Console** for any JavaScript errors
- Monitor **Network tab** for response headers
- Use **`curl -i`** to see status line and headers

---

**Happy Testing! 🎉**

For more details, see: **DEMO_SETUP.md** or **exe/README_DEMO.md**
