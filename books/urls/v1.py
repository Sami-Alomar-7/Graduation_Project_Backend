from django.urls import path
from books.views.book_upload_views import (
    AdminBookUploadView, 
    CustomerBookUploadView,
)
from books.views.book_list_views import (
    CustomerBookListView,
    CustomerBookDetailView,
    AdminBookListView,
    AdminBookDetailView,
    AdminAllBooksListView
)
from books.views.book_delete_views import (
    AdminBookDeleteView,
    CustomerBookDeleteView
)
from books.views.ai_processing_views import (
    process_book_with_ai,
    get_book_analysis_summary,
    delete_book_analysis,
    get_task_status
)

urlpatterns = [
    # Book upload endpoints
    path('customer/books/upload/', CustomerBookUploadView.as_view(), name='customer-book-upload'),
    path('admin/books/upload/', AdminBookUploadView.as_view(), name='admin-book-upload'),
    
    # Book list endpoints
    path('customer/books/', CustomerBookListView.as_view(), name='customer-book-list'),
    path('customer/books/<int:book_id>/', CustomerBookDetailView.as_view(), name='customer-book-detail'),
    path('admin/books/', AdminBookListView.as_view(), name='admin-book-list'),
    path('admin/books/<int:book_id>/', AdminBookDetailView.as_view(), name='admin-book-detail'),
    path('admin/all-books/', AdminAllBooksListView.as_view(), name='admin-all-books-list'),
    
    # Book deletion endpoints
    path('customer/books/<int:book_id>/delete/', CustomerBookDeleteView.as_view(), name='customer-book-delete'),
    path('admin/books/<int:book_id>/delete/', AdminBookDeleteView.as_view(), name='admin-book-delete'),
    
    # AI processing endpoints
    path('books/<int:book_id>/process-ai/', process_book_with_ai, name='process-book-with-ai'),
    path('books/<int:book_id>/analysis-summary/', get_book_analysis_summary, name='get-book-analysis-summary'),
    path('books/<int:book_id>/delete-analysis/', delete_book_analysis, name='delete-book-analysis'),
    path('tasks/<str:task_id>/status/', get_task_status, name='get-task-status'),
]