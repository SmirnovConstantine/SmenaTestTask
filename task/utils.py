from django.http import JsonResponse


class CommonUtils:
    def errorResponse(self, message: str):
        return JsonResponse({
            "error": message
        })

