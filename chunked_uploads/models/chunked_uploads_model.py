from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from chunked_upload.models import ChunkedUpload
from books.models import Book
from customer.models import Customer
from myadmin.models import Admin
import os

User = get_user_model()

def validate_chunked_upload_file(value):
    """
    Validate that uploaded file is either epub or txt
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.epub', '.txt']
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'Only {", ".join(valid_extensions)} files are allowed. '
            f'Uploaded file has extension: {ext}'
        )

class BookChunkedUpload(ChunkedUpload):
    """
    Custom chunked upload model for books with virus scanning
    """
    # Override the user field to use our custom User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Additional fields for book metadata
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Virus scanning fields
    is_scanned = models.BooleanField(default=False)
    is_clean = models.BooleanField(default=False)
    scan_result = models.TextField(blank=True)
    
    # Book relationship (after completion)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        abstract = False

    def delete(self, delete_file=True, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(BookChunkedUpload, self).delete(*args, **kwargs)
        if delete_file and self.file:
            try:
                storage.delete(path)
            except:
                pass

    def get_upload_path(self, filename):
        """Custom upload path for book files"""
        if hasattr(self.user, 'customer'):
            return f'chunked_uploads/customer_{self.user.customer.id}/{filename}'
        elif hasattr(self.user, 'admin'):
            return f'chunked_uploads/admin_{self.user.admin.id}/{filename}'

    def save(self, *args, **kwargs):
        if not self.upload_id:
            # Generate custom upload_id if needed
            import uuid
            self.upload_id = str(uuid.uuid4())
        super().save(*args, **kwargs)