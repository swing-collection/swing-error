from django.http import JsonResponse


def handle_500(request):
    return JsonResponse({
        "error": "Server Error",
        "message": "An internal server error occurred."
    }, status=500)

