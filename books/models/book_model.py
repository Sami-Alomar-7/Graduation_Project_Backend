from django.db import models
from django.core.exceptions import ValidationError
from customer.models import Customer
from myadmin.models import Admin
import os

def validate_book_file(value):
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

def book_upload_path(instance, filename):
    if instance.customer:
        return f'books/customer_{instance.customer.id}/{filename}'
    elif instance.admin:
        return f'books/admin_{instance.admin.id}/{filename}'

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=book_upload_path, validators=[validate_book_file])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
