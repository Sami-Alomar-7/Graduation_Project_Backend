from rest_framework.views import APIView
from rest_framework import permissions
from store.models import Store
from store.serializers.admin_store_action_serializer import AdminStoreActionSerializer
from myadmin.models import Admin
from myadmin.permissions.admin_permissions import IsAdmin
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError
from utils.shortcuts import get_object_or_404

class AdminStoreActionView(APIView):
    """
    View for admins to approve or reject customer book requests
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def patch(self, request, store_book_id):
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            raise NotFoundError(
                en_message="Admin profile not found",
                ar_message="لم يتم العثور على ملف المدير"
            )
        
        # Get the store entry
        store_entry = get_object_or_404(
            Store,
            id=store_book_id,
            status=Store.Status.PENDING,
            en_message="Pending store request not found",
            ar_message="لم يتم العثور على طلب المتجر المعلق"
        )
        
        # Validate action
        action = request.data.get('action')
        if action not in ['approve', 'reject']:
            raise BadRequestError(
                en_message="Invalid action. Must be 'approve' or 'reject'",
                ar_message="إجراء غير صالح. يجب أن يكون 'approve' أو 'reject'"
            )
        
        # Update status based on action
        if action == 'approve':
            store_entry.status = Store.Status.PUBLIC
            message_en = "Book request approved successfully"
            message_ar = "تمت الموافقة على طلب الكتاب بنجاح"
        else:  # reject
            store_entry.status = Store.Status.REJECTED
            message_en = "Book request rejected successfully"
            message_ar = "تم رفض طلب الكتاب بنجاح"
        
        # Set the admin who processed the request
        store_entry.admin = admin_instance
        store_entry.save()
        
        serializer = AdminStoreActionSerializer(store_entry, context={'request': request})
        
        return ResponseFormatter.success_response(
            en=message_en,
            ar=message_ar,
            data=serializer.data
        )

class AdminPendingRequestsView(APIView):
    """
    View for admins to see all pending customer book requests
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
        
        # Get all pending requests
        pending_requests = Store.objects.filter(
            status=Store.Status.PENDING
        ).select_related(
            'book', 'book__customer__user'
        ).order_by('-created_at')
        
        serializer = AdminStoreActionSerializer(pending_requests, many=True, context={'request': request})
        
        return ResponseFormatter.success_response(
            en="Pending requests retrieved successfully",
            ar="تم استرجاع الطلبات المعلقة بنجاح",
            data={
                'pending_requests': serializer.data,
                'total_count': pending_requests.count()
            }
        ) 