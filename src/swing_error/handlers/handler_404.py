from django.http import JsonResponse

def handle_404(request, exception):
    return JsonResponse({
        "error": "Not Found",
        "message": "The requested resource was not found."
    }, status=404)