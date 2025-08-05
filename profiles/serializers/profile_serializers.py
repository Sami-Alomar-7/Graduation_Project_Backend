from rest_framework import serializers
from profiles.models import Profile
from chunks.models import Chunk


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    
    book_title = serializers.CharField(source='chunk.book.title', read_only=True)
    chunk_index = serializers.IntegerField(source='chunk.chunk_index', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'chunk', 'chunk_index', 'book_title', 'name', 'hint', 'age', 'role',
            'personality', 'physical_characteristics', 'events', 'relationships', 
            'aliases', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_title', 'chunk_index']


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializer for listing profiles with minimal data"""
    
    book_title = serializers.CharField(source='chunk.book.title', read_only=True)
    chunk_index = serializers.IntegerField(source='chunk.chunk_index', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'chunk', 'chunk_index', 'book_title', 'name', 'hint', 'age', 'role',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'book_title', 'chunk_index']


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed profile view"""
    
    book_title = serializers.CharField(source='chunk.book.title', read_only=True)
    chunk_index = serializers.IntegerField(source='chunk.chunk_index', read_only=True)
    chunk_text_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'chunk', 'chunk_index', 'book_title', 'name', 'hint', 'age', 'role',
            'personality', 'physical_characteristics', 'events', 'relationships', 
            'aliases', 'chunk_text_preview', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_title', 'chunk_index', 'chunk_text_preview']
    
    def get_chunk_text_preview(self, obj):
        """Get a preview of the chunk text (first 200 characters)"""
        chunk_text = obj.chunk.chunk_text
        return chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text 