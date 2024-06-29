from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
import logging

# generic = "Please return to our home page"

class Handler400View(TemplateView):
    """
    Handler400View
    ---------------

    A class-based view to handle HTTP 400 Bad Request errors.

    This view renders a custom template with error details and sets the 
    appropriate 400 status code in the response.

    """

    template_name = "errors/error.html"
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        """
        Extend the base context data with custom error information.
        """
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Bad Request",
            "header": "400 Error",
            "message": "Sorry, Bad Request",
            "redirect": "Please return to our home page",
        })
        return context

    def get(self, request, *args, **kwargs):
        """
        Handle the GET request by logging the error and rendering the response.
        """
        self.log_error(request)
        context = self.get_context_data(**kwargs)
        return HttpResponseBadRequest(self.render_to_string(context))

    def log_error(self, request):
        """
        Log the error details for debugging purposes.
        """
        self.logger.error(f"400 Bad Request at {request.path}")

# Usage in urls.py
# (Assuming you have defined this view in a file named views.py inside an app called 'myapp')
handler400 = 'myapp.views.Handler400View.as_view()'
