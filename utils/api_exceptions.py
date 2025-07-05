from rest_framework.exceptions import APIException
from rest_framework import status

class APIError(APIException):
    """Base API Exception class for handling all errors"""
    def __init__(self, en_message: str, ar_message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.en_message = en_message
        self.ar_message = ar_message
        self.status_code = status_code
        super().__init__(detail=None)

class BadRequestError(APIError):
    def __init__(self, en_message: str, ar_message: str):
        super().__init__(en_message=en_message, ar_message=ar_message, status_code=status.HTTP_400_BAD_REQUEST)

class AuthenticationError(APIError):
    def __init__(self, en_message: str = "Authentication failed", ar_message: str = "فشل المصادقة"):
        super().__init__(en_message=en_message, ar_message=ar_message, status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionError(APIError):
    def __init__(self, en_message: str = "Permission denied", ar_message: str = "تم رفض الإذن"):
        super().__init__(en_message=en_message, ar_message=ar_message, status_code=status.HTTP_403_FORBIDDEN)

class NotFoundError(APIError):
    def __init__(self, en_message: str = "Resource not found", ar_message: str = "المورد غير موجود"):
        super().__init__(en_message=en_message, ar_message=ar_message, status_code=status.HTTP_404_NOT_FOUND) 