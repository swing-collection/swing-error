from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest

generic = "Please return to our home page"

class Handler400View(TemplateView):
    """
    Handler400View
    ---------------

    A class-based view to handle HTTP 400 Bad Request errors.

    This view renders a custom template with error details and sets the 
    appropriate 400 status code in the response.
    """

    template_name = "errors/error.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, Bad Request",
            "redirect": generic,
        }
        return self.render_to_response(context, status=400)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return HttpResponseBadRequest(self.get_template_names(), context, **response_kwargs)

# Usage in urls.py
# (Assuming you have defined this view in a file named views.py inside an app called 'myapp')
handler400 = 'myapp.views.Handler400View.as_view()'
