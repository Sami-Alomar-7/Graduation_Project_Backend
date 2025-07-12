from rest_framework import serializers
from store.models import Store
from books.seializers.book_list_serializer import BookDetailSerializer

class StoreBookListSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying books in the store (for customers)
    """
    book = BookDetailSerializer(read_only=True)
    admin_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'admin_name', 'status', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_admin_name(self, obj):
        """Get admin name who added the book to store"""
        if obj.admin and obj.admin.user:
            return obj.admin.user.username
        return "Unknown"

class StoreBookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed store book information
    """
    book = BookDetailSerializer(read_only=True)
    admin_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'admin_info', 'status', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_admin_info(self, obj):
        """Get admin information who added the book to store"""
        if obj.admin and obj.admin.user:
            return {
                'id': obj.admin.id,
                'username': obj.admin.user.username,
                'email': obj.admin.user.email
            }
        return None

class AdminStoreBookListSerializer(serializers.ModelSerializer):
    """
    Serializer for admins to view all books in store with additional info
    """
    book = BookDetailSerializer(read_only=True)
    admin_name = serializers.SerializerMethodField()
    customer_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = ['id', 'book', 'admin_name', 'customer_info', 'status', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_admin_name(self, obj):
        """Get admin name who added the book to store"""
        if obj.admin and obj.admin.user:
            return obj.admin.user.username
        return "Unknown"
    
    def get_customer_info(self, obj):
        """Get customer information if the book belongs to a customer"""
        if obj.book.customer and obj.book.customer.user:
            return {
                'id': obj.book.customer.id,
                'username': obj.book.customer.user.username,
                'email': obj.book.customer.user.email
            }
        return None 