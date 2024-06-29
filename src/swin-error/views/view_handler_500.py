from django.views.generic import TemplateView
from django.http import HttpResponseServerError

class Handler500View(TemplateView):
    template_name = "errors/500.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Internal Server Error",
            "header": "500 Error",
            "message": "Sorry, something went wrong on our end.",
            "redirect": generic,
        }
        return HttpResponseServerError(self.render_to_string(context))

handler500 = 'myapp.views.Handler500View.as_view()'
