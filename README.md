<p align="center">
    <img src="https://github.com/scape-agency/swing.dj/blob/85830584264bca52c02e1f0dcfa3648f84783805/res/swing-logo.png" width="20%" height="20%" alt="Django Swing Logo">
</p>
<h1 align='center' style='border-bottom: none;'>Swing Error</h1>
<h3 align='center'>Django Swing Collection</h3>
<br/>

## Overview

**Swing Error** provides custom error handlers for various HTTP status codes in a Django application. Each error handler is designed to return a custom response with additional functionality and logging capabilities. The custom error handlers cover the following HTTP status codes:

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 Method Not Allowed
- 408 Request Timeout
- 410 Gone
- 429 Too Many Requests
- 500 Internal Server Error

## Installation

1. Clone the repository to your local machine.
2. Add the custom error handlers to your Django project.

## Setup

### Step 1: Define Custom Response Classes

Create a file named `responses.py` in your Django application directory and define custom response classes for each HTTP status code.

Example for HTTP 400:

```python
# responses.py
from django.http import HttpResponse
from typing import Any, Union
import logging

class Http400Response(HttpResponse):
    status_code = 400

    def __init__(self, content: Union[bytes, str] = b'', *args: Any, **kwargs: Any) -> None:
        super().__init__(content, *args, **kwargs)
        self.log_error()

    def log_error(self) -> None:
        logger = logging.getLogger(__name__)
        logger.error(f"400 Bad Request: Response initialized with content: {self.content}")
```

Repeat this for other status codes (401, 403, 404, 405, 408, 410, 429, 500) as shown in the initial setup.

### Step 2: Update URL Configuration

Update your `urls.py` file to include the custom error handlers.

```python
# urls.py
from django.urls import path
from django.conf.urls import handler400, handler401, handler403, handler404, handler405, handler408, handler410, handler429, handler500
from .responses import (
    Http400Response, Http401Response, Http403Response, Http404Response,
    Http405Response, Http408Response, Http410Response, Http429Response, Http500Response
)
from .views import home_view, another_view

urlpatterns = [
    path('', home_view, name='home'),
    path('another/', another_view, name='another'),
]

handler400 = lambda request, exception=None: Http400Response("Bad Request: Invalid request.")
handler401 = lambda request, exception=None: Http401Response("Unauthorized: Authentication is required.")
handler403 = lambda request, exception=None: Http403Response("Forbidden: You do not have permission to access this page.")
handler404 = lambda request, exception=None: Http404Response("Not Found: The requested resource was not found.")
handler405 = lambda request, exception=None: Http405Response("Method Not Allowed: This endpoint only supports certain methods.")
handler408 = lambda request, exception=None: Http408Response("Request Timeout: The server timed out waiting for the request.")
handler410 = lambda request, exception=None: Http410Response("Gone: The requested resource is no longer available.")
handler429 = lambda request, exception=None: Http429Response("Too Many Requests: You have exceeded your request limit.")
handler500 = lambda request: Http500Response("Internal Server Error: An unexpected error occurred.")
```

### Step 3: Create Custom Templates

Create custom templates for each error handler in your templates directory.

Example for 400 error (templates/errors/400.html):

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ header }}</h1>
    <p>{{ message }}</p>
    <a href="/">{{ redirect }}</a>
</body>
</html>
```

Repeat this for other status codes (401, 403, 404, 405, 408, 410, 429, 500) with appropriate content.

### Step 4: Test Custom Error Handlers

Ensure that the custom error handlers are invoked correctly by triggering the respective errors in your application. For example, you can test a 404 error by accessing a non-existent URL.

## Usage

In your views, you can use the custom response classes to return specific error responses as needed. For example:

```python
from django.shortcuts import render
from .responses import Http400Response, Http404Response

def some_view(request):
    if some_condition:
        return Http400Response("Bad Request: Invalid data.")
    if another_condition:
        return Http404Response("Not Found: The requested resource was not found.")
    return render(request, 'some_template.html')
```


---

## Colophon

Made with ❤️ by **[Scape Agency](https://www.scape.agency)**

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the BSD-3-Clause license. See the [LICENSE](LICENSE) file for details.

---




Error Handler App for Django

## Links

### Docs

- https://docs.djangoproject.com/en/3.0/howto/error-reporting/
- https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.handler400

### Templates

- https://codepen.io/akashrajendra/pen/JKKRvQ
- https://webartdevelopers.com/blog/category/500-error-page-html-templates/

- https://github.com/wooyek/django-error-views

