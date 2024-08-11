======
Errors
======

Errors is a Django app to ...

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "errors" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'errors',
    ]

2. Include the errors URLconf in your project urls.py like this::

    path('errors/', include('errors.urls')),

3. Run ``python manage.py migrate`` to create the errors models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/errors/ to participate in the poll.