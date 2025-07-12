from django.db import models
from books.models import Book
from myadmin.models import Admin

class Store(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        REJECTED = 'rejected', 'Rejected'
        PUBLIC = 'public', 'Public'
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='store_entries')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, related_name='store_books', null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.status}"
