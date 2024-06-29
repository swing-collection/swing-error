# https://stackoverflow.com/questions/49162214/why-django-doesnt-have-error-page-handler-for-405-method-not-allowed

from django.views.generic import TemplateView
from django.http import HttpResponse

class Handler405View(TemplateView):
    template_name = "errors/405.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Method Not Allowed",
            "header": "405 Error",
            "message": "This method is not allowed for the requested URL.",
            "redirect": generic,
        }
        return HttpResponse(self.render_to_string(context), status=405)

handler405 = 'myapp.views.Handler405View.as_view()'
