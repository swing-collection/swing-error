from django.http import JsonResponse

def handle_bad_request(request, exception):
    """
    """
    return JsonResponse(
        {
            "error": "Bad Request",
            "message": "The request cannot be fulfilled due to bad syntax."
        },
        status=400,
    )