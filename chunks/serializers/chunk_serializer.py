from rest_framework import serializers
from chunks.models import Chunk
from books.models import Book


class ChunkSerializer(serializers.ModelSerializer):
    """Serializer for Chunk model"""
    
    book_title = serializers.CharField(source='book.title', read_only=True)
    chunk_size = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Chunk
        fields = [
            'id', 'book', 'book_title', 'chunk_index', 'chunk_text', 
            'chunk_size', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'chunk_size']


class ChunkListSerializer(serializers.ModelSerializer):
    """Serializer for listing chunks with minimal data"""
    
    book_title = serializers.CharField(source='book.title', read_only=True)
    chunk_size = serializers.IntegerField(read_only=True)
    profiles_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chunk
        fields = [
            'id', 'book', 'book_title', 'chunk_index', 'chunk_size', 
            'profiles_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'chunk_size', 'profiles_count']
    
    def get_profiles_count(self, obj):
        """Get the number of profiles for this chunk"""
        return obj.profiles.count() 