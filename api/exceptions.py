from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the custom response format for AuthenticationFailed exceptions
    if isinstance(exc, AuthenticationFailed):
        custom_response_data = {
            "status": False,
            "message": str(exc.detail)
        }
        response.data = custom_response_data

    return response