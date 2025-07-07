from django.urls import path
from books.views import (
    AdminBookUploadView, 
    CustomerBookUploadView,
    CustomerBookDeleteView,
    AdminBookDeleteView,
    AdminStoreBookDeleteView
)

urlpatterns = [
    path('customer/books/upload/', CustomerBookUploadView.as_view(), name='customer-book-upload'),
    path('admin/books/upload/', AdminBookUploadView.as_view(), name='admin-book-upload'),
    
    # Book deletion endpoints
    path('customer/books/<int:book_id>/delete/', CustomerBookDeleteView.as_view(), name='customer-book-delete'),
    path('admin/books/<int:book_id>/delete/', AdminBookDeleteView.as_view(), name='admin-book-delete'),
    path('admin/store/books/<int:book_id>/delete/', AdminStoreBookDeleteView.as_view(), name='admin-store-book-delete'),
]