from rest_framework.views import APIView
from rest_framework import permissions
from utils.shortcuts import get_object_or_404
from store.models import Store
from books.models import Book
from myadmin.models import Admin
from myadmin.permissions.admin_permissions import IsAdmin
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError
from utils.api_exceptions import NotFoundError, BadRequestError
import os

class AdminStoreBookDeleteView(APIView):
    """
    Admin-specific store book deletion view
    - Can remove any book from the store
    - For admin books: remove from store AND delete from book table
    - For customer books: remove from store ONLY (preserve book)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def delete(self, request, book_id):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )
        
        # Get the book
        book = get_object_or_404(
            Book,
            id=book_id,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        
        # Check if book is in store
        store_entries = Store.objects.filter(book=book)
        
        if not store_entries.exists():
            raise BadRequestError(
                en_message="Book is not in the store",
                ar_message="الكتاب غير موجود في المتجر"
            )
        
        # Check if it's an admin book (own or other admin's)
        is_admin_book = book.admin is not None
        
        # Remove from store
        store_entries.delete()
        
        if is_admin_book:
            # For admin books: remove from store AND delete from book table
            # Delete the file from storage
            if book.file and os.path.exists(book.file.path):
                os.remove(book.file.path)
            
            # Hard delete the book completely
            book.delete()
            
            return ResponseFormatter.success_response(
                en="Admin book removed from store and deleted from database",
                ar="تم إزالة كتاب المدير من المتجر وحذفه من قاعدة البيانات",
                data={
                    'book_id': book_id,
                    'action': 'removed_from_store_and_deleted',
                    'book_still_exists': False,
                    'book_owner': 'admin'
                }
            )
        else:
            # For customer books: remove from store ONLY
            return ResponseFormatter.success_response(
                en="Customer book removed from store successfully (book preserved)",
                ar="تم إزالة كتاب العميل من المتجر بنجاح (الكتاب محفوظ)",
                data={
                    'book_id': book_id,
                    'action': 'removed_from_store_only',
                    'book_still_exists': True,
                    'book_owner': 'customer'
                }
            )