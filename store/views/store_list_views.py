from rest_framework.views import APIView
from rest_framework import permissions
from store.models import Store
from store.serializers.store_list_serializer import (
    StoreBookListSerializer,
    StoreBookDetailSerializer,
    AdminStoreBookListSerializer
)
from customer.models import Customer
from myadmin.models import Admin
from customer.permissions.customer_permission import IsCustomer
from myadmin.permissions.admin_permissions import IsAdmin
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError
from utils.shortcuts import get_object_or_404

class CustomerStoreBookListView(APIView):
    """
    View for customers to browse books in the store (only PUBLIC books)
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        
        # Get only PUBLIC books from store
        store_books = Store.objects.filter(
            status=Store.Status.PUBLIC
        ).select_related('book', 'admin__user').order_by('-created_at')
        
        serializer = StoreBookListSerializer(store_books, many=True, context={'request': request})
        
        # Count books by type
        admin_books_count = store_books.filter(book__admin__isnull=False).count()
        customer_books_count = store_books.filter(book__customer__isnull=False).count()
        
        return ResponseFormatter.success_response(
            en="Store books retrieved successfully",
            ar="تم استرجاع كتب المتجر بنجاح",
            data={
                'books': serializer.data,
                'total_count': store_books.count(),
                'admin_books_count': admin_books_count,
                'customer_books_count': customer_books_count
            }
        )

class CustomerStoreBookDetailView(APIView):
    """
    View for customers to get details of a book in the store
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request, store_book_id):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        store_book = get_object_or_404(
            Store,
            id=store_book_id,
            status=Store.Status.PUBLIC,
            en_message="Store entry not found",
            ar_message="لم يتم العثور على هذا الكتاب في المتجر"
        )
        serializer = StoreBookDetailSerializer(store_book, context={'request': request})
        return ResponseFormatter.success_response(
            en="Store book details retrieved successfully",
            ar="تم استرجاع تفاصيل كتاب المتجر بنجاح",
            data=serializer.data
        )

class AdminStoreBookListView(APIView):
    """
    View for admins to browse all books in the store (all statuses)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )

        # Get all books from store (all statuses)
        store_books = Store.objects.all().select_related(
            'book', 'book__customer__user', 'book__admin__user', 'admin__user'
        ).order_by('-created_at')
        
        serializer = AdminStoreBookListSerializer(store_books, many=True, context={'request': request})
        
        # Count books by status
        public_count = store_books.filter(status=Store.Status.PUBLIC).count()
        pending_count = store_books.filter(status=Store.Status.PENDING).count()
        rejected_count = store_books.filter(status=Store.Status.REJECTED).count()
        
        # Count books by owner type
        admin_books_count = store_books.filter(book__admin__isnull=False).count()
        customer_books_count = store_books.filter(book__customer__isnull=False).count()
        
        return ResponseFormatter.success_response(
            en="Store books retrieved successfully",
            ar="تم استرجاع كتب المتجر بنجاح",
            data={
                'books': serializer.data,
                'total_count': store_books.count(),
                'status_counts': {
                    'public': public_count,
                    'pending': pending_count,
                    'rejected': rejected_count
                },
                'owner_counts': {
                    'admin_books': admin_books_count,
                    'customer_books': customer_books_count
                }
            }
        )

class AdminStoreBookDetailView(APIView):
    """
    View for admins to get details of any book in the store
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request, store_book_id):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )
        store_book = get_object_or_404(
            Store,
            id=store_book_id,
            en_message="Store entry not found",
            ar_message="لم يتم العثور على هذا الكتاب في المتجر"
        )
        serializer = StoreBookDetailSerializer(store_book, context={'request': request})
        return ResponseFormatter.success_response(
            en="Store book details retrieved successfully",
            ar="تم استرجاع تفاصيل كتاب المتجر بنجاح",
            data=serializer.data
        )

class AdminStoreBookByStatusView(APIView):
    """
    View for admins to filter books by status
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request, status):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )
        
        # Validate status
        valid_statuses = [choice[0] for choice in Store.Status.choices]
        if status not in valid_statuses:
            raise BadRequestError(
                en_message=f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}",
                ar_message=f"حالة غير صالحة. الحالات الصالحة هي: {', '.join(valid_statuses)}",
            )
        
        # Get books by status
        store_books = Store.objects.filter(
            status=status
        ).select_related(
            'book', 'book__customer__user', 'book__admin__user', 'admin__user'
        ).order_by('-created_at')
        
        serializer = AdminStoreBookListSerializer(store_books, many=True, context={'request': request})
        
        return ResponseFormatter.success_response(
            en=f"Store books with status '{status}' retrieved successfully",
            ar=f"تم استرجاع كتب المتجر بحالة '{status}' بنجاح",
            data={
                'books': serializer.data,
                'total_count': store_books.count(),
                'status': status
            }
        )