from rest_framework import serializers
from store.models import Store
from books.seializers.book_list_serializer import BookDetailSerializer

class CustomerStoreRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for customer store request creation
    """
    book = BookDetailSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'status', 'status_display', 'created_at', 'updated_at']
        read_only_fields = fields

class CustomerStoreRequestListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer's store requests
    """
    book = BookDetailSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    admin_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'status', 'status_display', 'admin_info', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_admin_info(self, obj):
        """Get admin information who processed the request (for rejected books)"""
        if obj.admin and obj.admin.user:
            return {
                'id': obj.admin.id,
                'username': obj.admin.user.username,
                'email': obj.admin.user.email
            }
        return None 