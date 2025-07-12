from rest_framework.views import APIView
from rest_framework import permissions
from utils.shortcuts import get_object_or_404
from books.models import Book
from books.seializers.book_list_serializer import (
    BookListSerializer,
    BookDetailSerializer
)
from customer.models import Customer
from myadmin.models import Admin
from customer.permissions.customer_permission import IsCustomer
from myadmin.permissions.admin_permissions import IsAdmin
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError

class CustomerBookListView(APIView):
    """
    View for customers to list their own books
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

        books = Book.objects.filter(
            customer=customer_instance,
            is_deleted=False
        ).order_by('-created_at')
        
        serializer = BookListSerializer(books, many=True, context={'request': request})
        
        return ResponseFormatter.success_response(
            en="Customer books retrieved successfully",
            ar="تم استرجاع كتب العميل بنجاح",
            data={
                'books': serializer.data,
                'total_count': books.count()
            }
        )

class CustomerBookDetailView(APIView):
    """
    View for customers to get details of their own book
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request, book_id):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        book = get_object_or_404(
            Book,
            id=book_id,
            customer=customer_instance,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        serializer = BookDetailSerializer(book, context={'request': request})
        return ResponseFormatter.success_response(
            en="Book details retrieved successfully",
            ar="تم استرجاع تفاصيل الكتاب بنجاح",
            data=serializer.data
        )

class AdminBookListView(APIView):
    """
    View for admins to list their own books
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
        books = Book.objects.filter(
            admin=admin_instance,
            is_deleted=False
        ).order_by('-created_at')
        
        serializer = BookListSerializer(books, many=True, context={'request': request})
        
        return ResponseFormatter.success_response(
            en="Admin books retrieved successfully",
            ar="تم استرجاع كتب المدير بنجاح",
            data={
                'books': serializer.data,
                'total_count': books.count()
            }
        )

class AdminBookDetailView(APIView):
    """
    View for admins to get details of their own book
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request, book_id):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )
        book = get_object_or_404(
            Book,
            id=book_id,
            admin=admin_instance,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        serializer = BookDetailSerializer(book, context={'request': request})
        return ResponseFormatter.success_response(
            en="Book details retrieved successfully",
            ar="تم استرجاع تفاصيل الكتاب بنجاح",
            data=serializer.data
        )

class AdminAllBooksListView(APIView):
    """
    View for admins to list all books (both customer and admin books)
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
        
        # Get all books (both customer and admin books)
        books = Book.objects.filter(
            is_deleted=False
        ).order_by('-created_at')
        
        serializer = BookListSerializer(books, many=True, context={'request': request})
        
        # Count books by owner type
        customer_books_count = books.filter(customer__isnull=False).count()
        admin_books_count = books.filter(admin__isnull=False).count()
        
        return ResponseFormatter.success_response(
            en="All books retrieved successfully",
            ar="تم استرجاع جميع الكتب بنجاح",
            data={
                'books': serializer.data,
                'total_count': books.count(),
                'customer_books_count': customer_books_count,
                'admin_books_count': admin_books_count
            }
        )