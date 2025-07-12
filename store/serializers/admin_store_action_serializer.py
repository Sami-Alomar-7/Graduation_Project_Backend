from rest_framework import serializers
from store.models import Store
from books.seializers.book_list_serializer import BookDetailSerializer

class AdminStoreActionSerializer(serializers.ModelSerializer):
    """
    Serializer for admin store actions (approve/reject)
    """
    book = BookDetailSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    customer_info = serializers.SerializerMethodField()
    admin_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'status', 'status_display', 'customer_info', 'admin_info', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_customer_info(self, obj):
        """Get customer information who requested the book"""
        if obj.book.customer and obj.book.customer.user:
            return {
                'id': obj.book.customer.id,
                'username': obj.book.customer.user.username,
                'email': obj.book.customer.user.email
            }
        return None
    
    def get_admin_info(self, obj):
        """Get admin information who processed the request"""
        if obj.admin and obj.admin.user:
            return {
                'id': obj.admin.id,
                'username': obj.admin.user.username,
                'email': obj.admin.user.email
            }
        return None 