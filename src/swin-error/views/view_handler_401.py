# https://stackoverflow.com/questions/4356842/how-do-i-return-a-401-unauthorized-in-django

from django.views.generic import TemplateView
from django.http import HttpResponse

class Handler401View(TemplateView):
    template_name = "errors/401.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Unauthorized",
            "header": "401 Error",
            "message": "Authorization is required to access this page.",
            "redirect": generic,
        }
        return HttpResponse(self.render_to_string(context), status=401)

handler401 = 'myapp.views.Handler401View.as_view()'
