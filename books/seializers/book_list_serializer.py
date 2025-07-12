from rest_framework import serializers
from books.models import Book
import os

class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying books in lists
    """
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'file_size', 'file_extension', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_file_size(self, obj):
        """Get file size in MB"""
        if obj.file and hasattr(obj.file, 'size'):
            return f"{obj.file.size / (1024*1024):.2f} MB"
        return "N/A"
    
    def get_file_extension(self, obj):
        """Get file extension"""
        if obj.file:
            return os.path.splitext(obj.file.name)[1].lower()
        return "N/A"

class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed book information
    """
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    owner_type = serializers.SerializerMethodField()
    owner_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'file', 'file_url', 'file_size', 'file_extension', 'owner_type', 'owner_info', 'created_at', 'updated_at']
        read_only_fields = fields
    
    def get_file_size(self, obj):
        """Get file size in MB"""
        if obj.file and hasattr(obj.file, 'size'):
            return f"{obj.file.size / (1024*1024):.2f} MB"
        return "N/A"
    
    def get_file_extension(self, obj):
        """Get file extension"""
        if obj.file:
            return os.path.splitext(obj.file.name)[1].lower()
        return "N/A"
    
    def get_file_url(self, obj):
        """Get file download URL"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_owner_type(self, obj):
        """Get owner type (customer or admin)"""
        if obj.customer:
            return "customer"
        elif obj.admin:
            return "admin"
        return "unknown"
    
    def get_owner_info(self, obj):
        """Get owner information"""
        if obj.customer:
            return {
                'id': obj.customer.id,
                'email': obj.customer.user.email,
                'username': obj.customer.user.username
            }
        elif obj.admin:
            return {
                'id': obj.admin.id,
                'email': obj.admin.user.email,
                'username': obj.admin.user.username
            }
        return None