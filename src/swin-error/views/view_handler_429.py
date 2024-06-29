# https://django-ratelimit.readthedocs.io/en/latest/cookbook/429.html

from django.views.generic import TemplateView
from django.http import HttpResponse

class Handler429View(TemplateView):
    template_name = "errors/429.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Too Many Requests",
            "header": "429 Error",
            "message": "You have sent too many requests in a given amount of time.",
            "redirect": generic,
        }
        return HttpResponse(self.render_to_string(context), status=429)

handler429 = "myapp.views.Handler429View.as_view()"
