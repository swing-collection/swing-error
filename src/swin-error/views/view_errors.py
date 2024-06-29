# -*- coding: utf-8 -*-


# DocString
"""
Error Handler Views
===================


"""


# Built-In Modules


# Third-Party Modules
from django.shortcuts import render

# Local Modules


generic = "Please reurn to our home page"


def handler400(request, exception, template_name = "errors/error.html"):
    """
    handler400
    ----------

    A callable, or a string representing the full Python import path to the
    view that should be called if the HTTP client has sent a request that
    caused an error condition and a response with a status code of 400.

    By default, this is django.views.defaults.bad_request(). If you implement
    a custom view, be sure it accepts request and exception arguments and
    returns an HttpResponseBadRequest.

    https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.handler400
    https://docs.djangoproject.com/en/4.0/ref/urls/#django.conf.urls.handler400
    """

    response = render(request, template_name, {
        "title": "Bad Request",
        "header": "400 Error",
        "message": "Sorry, Bad Request",
        "redirect": generic,
    })

    response.status_code = 400

    return response


def handler403(request, exception, template_name = "errors/error.html"):
    """
    handler403
    ----------

    A callable, or a string representing the full Python import path to
    the view that should be called if the user doesn't have the permissions
    required to access a resource.

    By default, this is django.views.defaults.permission_denied(). If you
    implement a custom view, be sure it accepts request and exception
    arguments and returns an HttpResponseForbidden.

    https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.handler403
    https://docs.djangoproject.com/en/4.0/ref/urls/#django.conf.urls.handler403
    """

    response = render(request, template_name, {
        "title": "Forbidden",
        "header": "403 Error",
        "message": "Sorry, this is a Forbidden Page",
        "redirect": generic,
    })

    response.status_code = 403

    return response


def handler404(request, exception, template_name = "errors/error.html"):
    """
    handler404
    ----------

    A callable, or a string representing the full Python import path to
    the view that should be called if none of the URL patterns match.

    By default, this is django.views.defaults.page_not_found(). If you
    implement a custom view, be sure it accepts request and exception
    arguments and returns an HttpResponseNotFound.

    https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.handler404
    https://docs.djangoproject.com/en/4.0/ref/urls/#django.conf.urls.handler404
    """

    response = render(request, template_name, {
        "title": "Page not found",
        "header": "404 Error",
        "message": "Sorry, but the requested page could not be found.",
        "redirect": generic,
    })

    response.status_code = 404

    # The page you are looking for doesn't exist or has been removed.
    return response


def handler429(request, template_name = "errors/error.html"):
    """
    handler429
    ----------

    """

    response = render(request, template_name, {
        "title": "Too Many Requests",
        "header": "429 Error",
        "message": "Sorry, but there were too many requests.",
        "redirect": generic,
    })

    response.status_code = 429

    # return render(request, "429." +
    # app_settings.TEMPLATE_EXTENSION, status=429)
    return response


def handler500(request, template_name = "errors/error.html"):
    """
    handler500
    ----------

    A callable, or a string representing the full Python import path to
    the view that should be called in case of server errors. Server
    errors happen when you have runtime errors in view code.

    By default, this is django.views.defaults.server_error(). If you
    implement a custom view, be sure it accepts a request argument and
    returns an HttpResponseServerError.

    https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.handler500
    https://docs.djangoproject.com/en/4.0/ref/urls/#django.conf.urls.handler500
    """

    response = render(request, template_name, {
        "title": "Internal Server Error",
        "header": "500 Error",
        "message": "Sorry, we have run into an Internal Server Error",
        "redirect": generic,
    })

    # Oops something went wrong. Try to refresh this page or feel
    # free to contact us if the problem presists.

    response.status_code = 500

    return response

    # 503
    # Oops something went wrong. Try to refresh this page or feel free to
    # contact us if the problem presists.
