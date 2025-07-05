from typing import Any, Dict
from rest_framework.response import Response
from rest_framework import status
class ResponseFormatter:
    
    @staticmethod
    def format_error(en: str, ar: str) -> dict:
        return {
            "status": "error",
            "en": str(en),
            "ar": str(ar)
        }

    @staticmethod
    def format_success(data: any = None) -> dict:
        response = {
            "status": "success",
        }
        if data is not None:
            response["data"] = data
        return response

    @classmethod
    def error_response(cls, en: str, ar: str, status_code: int = 400) -> Response:
        return Response(
            cls.format_error(en=en, ar=ar),
            status=status_code
        )

    @classmethod
    def success_response(cls, data: any = None, status_code: int = 200) -> Response:
        return Response(
            cls.format_success(data),
            status=status_code
        )

SEARCH_MESSAGES = {
    'no_results': {
        'en': 'No products found matching your search criteria.',
        'ar': 'لم يتم العثور على منتجات تطابق معايير البحث.'
    },
    'invalid_search': {
        'en': 'Invalid search parameters provided.',
        'ar': 'معايير البحث غير صالحة.'
    }
}