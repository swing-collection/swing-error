from django.views.generic import TemplateView
from django.http import HttpResponseForbidden

class Handler403View(TemplateView):
    template_name = "errors/403.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Forbidden",
            "header": "403 Error",
            "message": "Sorry, you do not have permission to access this page.",
            "redirect": generic,
        }
        return HttpResponseForbidden(self.render_to_string(context))

handler403 = 'myapp.views.Handler403View.as_view()'
