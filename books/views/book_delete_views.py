from rest_framework.views import APIView
from rest_framework import permissions
from books.models import Book
from store.models import Store
from customer.models import Customer
from myadmin.models import Admin
from customer.permissions.customer_permission import IsCustomer
from myadmin.permissions.admin_permissions import IsAdmin
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError
from utils.shortcuts import get_object_or_404
import os

class CustomerBookDeleteView(APIView):
    """
    Customer-specific book deletion view
    - Can only delete their own books
    - If book is published (in store), soft delete (set is_deleted=True)
    - If book is not published, hard delete (remove from database)
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def delete(self, request, book_id):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        # Get the book and check ownership
        book = get_object_or_404(
            Book,
            id=book_id,
            customer=customer_instance,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        # Check if book is published (exists in store with PUBLIC status)
        is_published = Store.objects.filter(
            book=book, 
            status=Store.Status.PUBLIC
        ).exists()
        if is_published:
            # Soft delete - set is_deleted=True
            book.is_deleted = True
            book.save()
            return ResponseFormatter.success_response(
                en="Book deleted successfully (soft delete - book remains in store)",
                ar="تم حذف الكتاب بنجاح (حذف ناعم - الكتاب يبقى في المتجر)",
                data={'book_id': book_id, 'deletion_type': 'soft'}
            )
        else:
            # Hard delete - remove from database
            # Delete the file from storage
            if book.file and os.path.exists(book.file.path):
                os.remove(book.file.path)
            book.delete()
            return ResponseFormatter.success_response(
                en="Book deleted completely from database",
                ar="تم حذف الكتاب بالكامل من قاعدة البيانات",
                data={'book_id': book_id, 'deletion_type': 'hard'}
            )

class AdminBookDeleteView(APIView):
    """
    Admin-specific book deletion view
    - Can delete any book from the store
    - Can delete admin books (own or other admins') completely from book table
    - CANNOT delete customer books from book table (only from store)
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
        # Get the book (can be any book)
        book = get_object_or_404(
            Book,
            id=book_id,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        # Check if book is in store
        store_entries = Store.objects.filter(book=book)
        is_in_store = store_entries.exists()
        # Check if it's an admin book (own or other admin's)
        is_admin_book = book.admin is not None
        # Delete from store first if it exists
        if is_in_store:
            store_entries.delete()
        if is_admin_book:
            # Can delete admin books completely (own or other admins')
            # Delete the file from storage
            if book.file and os.path.exists(book.file.path):
                os.remove(book.file.path)
            # Hard delete the book completely
            book.delete()
            response_data = {
                'book_id': book_id,
                'deletion_type': 'hard',
                'was_in_store': is_in_store,
                'book_owner': 'admin'
            }
            if is_in_store:
                return ResponseFormatter.success_response(
                    en="Admin book deleted completely from database and store",
                    ar="تم حذف كتاب المدير بالكامل من قاعدة البيانات والمتجر",
                    data=response_data
                )
            else:
                return ResponseFormatter.success_response(
                    en="Admin book deleted completely from database",
                    ar="تم حذف كتاب المدير بالكامل من قاعدة البيانات",
                    data=response_data
                )
        else:
            # Customer book - can only remove from store, not from book table
            if is_in_store:
                return ResponseFormatter.success_response(
                    en="Customer book removed from store successfully (book preserved)",
                    ar="تم إزالة كتاب العميل من المتجر بنجاح (الكتاب محفوظ)",
                    data={
                        'book_id': book_id,
                        'deletion_type': 'store_only',
                        'was_in_store': True,
                        'book_owner': 'customer'
                    }
                )
            else:
                raise BadRequestError(
                    en_message="Cannot delete customer book from database",
                    ar_message="لا يمكن حذف كتاب العميل من قاعدة البيانات"
                )