from django.views.generic import TemplateView
from django.http import HttpResponseNotFound

class Handler404View(TemplateView):
    template_name = "errors/404.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Page Not Found",
            "header": "404 Error",
            "message": "Sorry, the requested page could not be found.",
            "redirect": generic,
        }
        return HttpResponseNotFound(self.render_to_string(context))

handler404 = 'myapp.views.Handler404View.as_view()'
