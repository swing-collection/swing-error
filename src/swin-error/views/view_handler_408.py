from django.views.generic import TemplateView
from django.http import HttpResponse

class Handler408View(TemplateView):
    template_name = "errors/408.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Request Timeout",
            "header": "408 Error",
            "message": "The server timed out waiting for the request.",
            "redirect": generic,
        }
        return HttpResponse(self.render_to_string(context), status=408)

handler408 = 'myapp.views.Handler408View.as_view()'
