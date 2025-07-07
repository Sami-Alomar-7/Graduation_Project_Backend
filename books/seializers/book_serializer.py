from rest_framework import serializers
from books.models import Book
import os

def validate_file_extension(value):
    """
    Validate that uploaded file is either epub or txt
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.epub', '.txt']
    
    if ext not in valid_extensions:
        raise serializers.ValidationError(
            f'Only {", ".join(valid_extensions)} files are allowed. '
            f'Uploaded file has extension: {ext}'
        )
    return value

def validate_file_size(value):
    """
    Validate file size (max 50MB)
    """
    max_size = 50 * 1024 * 1024  # 50MB in bytes
    
    if value.size > max_size:
        raise serializers.ValidationError(
            f'File size must be no more than 50MB. '
            f'Uploaded file size: {value.size / (1024*1024):.2f}MB'
        )
    return value

class BookSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        validators=[validate_file_extension, validate_file_size]
    )
    
    class Meta:
        model = Book
        exclude = ['is_deleted']
        read_only_fields = ['admin', 'customer']