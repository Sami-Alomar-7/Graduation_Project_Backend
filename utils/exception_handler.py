from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import APIException
from utils.messages import ResponseFormatter

def get_error_message(detail):
    """Extract readable error message from DRF error detail"""
    print(detail)
    if isinstance(detail, dict):
        # Get the first error message from the dict
        for field, errors in detail.items():
            if isinstance(errors, list):
                return str(errors[0])
            return str(errors)
    elif isinstance(detail, list):
        # Get the first error from the list
        return str(detail[0])
    return str(detail)

def get_error_details(detail):
    """Extract readable error message and field from DRF error detail"""
    print(detail)
    if isinstance(detail, dict):
        # Get the first error message from the dict
        for field, errors in detail.items():
            if isinstance(errors, list):
                return field, str(errors[0])
            return field, str(errors)
    elif isinstance(detail, list):
        # Get the first error from the list
        return None, str(detail[0])
    return None, str(detail)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all errors consistently
    """
    try:
        status_code = exc.status_code
    except AttributeError:
        status_code = 400

    if isinstance(exc, DjangoValidationError):
        print(exc)
        return ResponseFormatter.error_response(
            en="Validation error",
            ar="خطأ في التحقق",
            status_code=400
        )

    if isinstance(exc, APIException):
        if hasattr(exc, 'en_message') and hasattr(exc, 'ar_message'):
            # Our custom exceptions
            return ResponseFormatter.error_response(
                en=exc.en_message,
                ar=exc.ar_message,
                status_code=status_code
            )
        else:
            # DRF's built-in exceptions
            field, error_message = get_error_details(exc.detail)
            response_data = {
                "status": "error",
                "en": error_message,
                "ar": error_message,  # You might want to translate this
            }
            if field:
                response_data["field"] = field
            return Response(response_data, status=status_code)

    if exc is not None:
        print(exc)
        return ResponseFormatter.error_response(
            en="Internal server error",
            ar="خطأ في الخادم",
            status_code=500
        )

    return exception_handler(exc, context)