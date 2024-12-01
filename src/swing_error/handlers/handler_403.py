from django.http import JsonResponse

def handle_permission_denied(request, exception):
    return JsonResponse({
        "error": "Permission Denied",
        "message": "You do not have permission to perform this action."
    }, status=403)

