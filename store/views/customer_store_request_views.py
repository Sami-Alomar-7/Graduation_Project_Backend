from rest_framework.views import APIView
from rest_framework import permissions
from store.models import Store
from store.serializers.customer_store_request_serializer import (
    CustomerStoreRequestSerializer,
    CustomerStoreRequestListSerializer
)
from customer.models import Customer
from customer.permissions.customer_permission import IsCustomer
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError
from utils.shortcuts import get_object_or_404
from books.models import Book


class CustomerStoreRequestView(APIView):
    """
    View for customers to request their books to be added to the store
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def post(self, request, book_id):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        
        # Check if the book belongs to the customer
        book = get_object_or_404(
            Book,
            id=book_id,
            customer=customer_instance,
            is_deleted=False,
            en_message="Book not found",
            ar_message="لم يتم العثور على الكتاب"
        )
        
        # Check if the book is already in the store
        existing_store_entry = Store.objects.filter(book=book).first()
        if existing_store_entry:
            raise BadRequestError(
                en_message=f"Book is already in the store with status: {existing_store_entry.status}",
                ar_message=f"الكتاب موجود بالفعل في المتجر بحالة: {existing_store_entry.status}"
            )
        
        # Create store entry with PENDING status
        store_entry = Store.objects.create(
            book=book,
            status=Store.Status.PENDING
        )
        
        serializer = CustomerStoreRequestSerializer(store_entry, context={'request': request})
        
        return ResponseFormatter.success_response(
            en="Book request submitted successfully. Waiting for admin approval.",
            ar="تم تقديم طلب الكتاب بنجاح. في انتظار موافقة المدير.",
            data=serializer.data
        )

class CustomerStoreRequestListView(APIView):
    """
    View for customers to see their pending and rejected books in the store
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
        
        # Get store entries for customer's books with PENDING or REJECTED status
        store_entries = Store.objects.filter(
            book__customer=customer_instance,
            status__in=[Store.Status.PENDING, Store.Status.REJECTED]
        ).select_related('book', 'admin__user').order_by('-created_at')
        
        serializer = CustomerStoreRequestListSerializer(store_entries, many=True, context={'request': request})
        
        # Count by status
        pending_count = store_entries.filter(status=Store.Status.PENDING).count()
        rejected_count = store_entries.filter(status=Store.Status.REJECTED).count()
        
        return ResponseFormatter.success_response(
            en="Your store requests retrieved successfully",
            ar="تم استرجاع طلبات المتجر الخاصة بك بنجاح",
            data={
                'requests': serializer.data,
                'total_count': store_entries.count(),
                'pending_count': pending_count,
                'rejected_count': rejected_count
            }
        )

class CustomerStoreRequestByStatusView(APIView):
    """
    View for customers to filter their store requests by status
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request, status):
        try:
            customer_instance = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            raise NotFoundError(
                en_message="Customer profile not found",
                ar_message="لم يتم العثور على ملف العميل"
            )
        
        # Validate status
        valid_statuses = [Store.Status.PENDING, Store.Status.REJECTED]
        if status not in valid_statuses:
            raise BadRequestError(
                en_message=f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}",
                ar_message=f"حالة غير صالحة. الحالات الصالحة هي: {', '.join(valid_statuses)}",
            )
        
        # Get store entries for customer's books with specific status
        store_entries = Store.objects.filter(
            book__customer=customer_instance,
            status=status
        ).select_related('book', 'admin__user').order_by('-created_at')
        
        serializer = CustomerStoreRequestListSerializer(store_entries, many=True, context={'request': request})
        
        return ResponseFormatter.success_response(
            en=f"Your store requests with status '{status}' retrieved successfully",
            ar=f"تم استرجاع طلبات المتجر الخاصة بك بحالة '{status}' بنجاح",
            data={
                'requests': serializer.data,
                'total_count': store_entries.count(),
                'status': status
            }
        ) 